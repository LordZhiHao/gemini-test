import os
from fastapi import FastAPI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Create FastAPI app
app = FastAPI()

# Load environment variables and initialize components
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY)

# Database connection
conn_string = 'postgresql://postgres:postgres@localhost/books_db'
engine = create_engine(conn_string)
db = SQLDatabase.from_uri(conn_string)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Create SQL agent
sql_agent = create_sql_agent(
    toolkit=toolkit,
    llm=llm,
    verbose=True,
    max_iterations=5,
    allow_dangerous_code=False
)

@app.get("/query")
async def query_database(question: str):
    try:
        result = sql_agent.invoke(question)
        return {"response": result["output"]}
    except Exception as e:
        return {"error": str(e)}

# Optional: Add a root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Database Query API"}

# To run the app, use:
# uvicorn your_file_name:app --reload