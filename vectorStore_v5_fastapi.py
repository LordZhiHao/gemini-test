import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Create a Pydantic model for the request body
class Question(BaseModel):
    question: str

# Initialize the chain (moved outside the endpoint to avoid reinitializing on every request)
def initialize_chain():
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    llm_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)
    
    client = MongoClient(os.getenv("MONGODB_ATLAS_CLUSTER_URI"))
    
    DB_NAME = "test_db"
    COLLECTION_NAME = "test_collection_pdf"
    ATLAS_VECTOR_SEARCH_INDEX_NAME = "test-index-pdf"
    
    MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]
    
    vector_store = MongoDBAtlasVectorSearch(
        collection=MONGODB_COLLECTION,
        embedding=embeddings,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
        relevance_score_fn="cosine",
    )
    
    retriever = vector_store.as_retriever()
    
    chain = RetrievalQA.from_chain_type(
        llm=llm_model,
        retriever=retriever,
        chain_type="stuff"
    )
    
    return chain, client

# Initialize the chain and MongoDB client
qa_chain, mongo_client = initialize_chain()

# Create the endpoint
@app.post("/ask")
async def ask_question(question: Question):
    try:
        # Get the response from the chain
        response = qa_chain.invoke(question.question)
        
        # Return the response
        return {"answer": response["result"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Cleanup when shutting down
@app.on_event("shutdown")
def shutdown_event():
    mongo_client.close()

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, port=8001)