import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY )

df = pd.read_csv("students.csv")

agent = create_pandas_dataframe_agent(
    llm = llm,
    df = df,
    verbose=True,
    max_iterations=5,
    allow_dangerous_code=True
)

res = agent.invoke("What is the lowest math, reading and writing score")
print(res["output"])