import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
from dotenv import load_dotenv
import json

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)

client = MongoClient(os.getenv("MONGODB_ATLAS_CLUSTER_URI"))

DB_NAME = "test_db"
COLLECTION_NAME = "test_collection_json"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "test-index-json"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]
MONGODB_COLLECTION.delete_many({})

vector_store = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=embeddings,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)

def format_item_with_keys(item):
    """
    Formats a dictionary item into a string with keys in brackets
    Example: [name] John [age] 30 [city] New York
    """
    formatted_parts = []
    for key, value in item.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value)  # Convert complex objects to string
        formatted_parts.append(f"[{key}] {value}")
    return " ".join(formatted_parts)

def load_json_as_documents(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        documents = []
        
        if isinstance(json_data, list):
            for item in json_data:
                # Format the content with keys in brackets
                page_content = format_item_with_keys(item)
                # Keep the original item as metadata
                metadata = item
                documents.append(Document(page_content=page_content, metadata=metadata))
                
        return documents

# Load and process the documents
docs = load_json_as_documents('your_file.json')
vector_store.add_documents(docs)

print("Documents Added!")

client.close()