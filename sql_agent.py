import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY )

conn_string = 'postgresql://postgres:postgres@localhost/books_db'
engine = create_engine(conn_string)

db = SQLDatabase.from_uri(conn_string)
toolkit = SQLDatabaseToolkit(db=db, llm = llm)

sql_agent = create_sql_agent(
    toolkit = toolkit,
    llm = llm,
    verbose = True,
    max_iterations=5,
    allow_dangerous_code=False
)

QUESTION = """Provide the list of all books"""

res = sql_agent.invoke(QUESTION)

print(res["output"])