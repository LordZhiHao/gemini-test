import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)

client = MongoClient(os.getenv("MONGODB_ATLAS_CLUSTER_URI"))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

DB_NAME = "test_db"
COLLECTION_NAME = "test_collection"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "test-index-1"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

vector_store = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=embeddings,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)

vector_store.create_vector_search_index(dimensions=768)

print("Vector Store Created!")
client.close()