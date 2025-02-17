from fastapi import FastAPI, Query
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.datetime import DatetimeOutputParser
from datetime import datetime

app = FastAPI()

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

output_parser = DatetimeOutputParser()

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You always reply to questions only in datetime patterns",
        ),
        (
            "human",
            "{request} \n {format_instructions}",
        ),
    ]
)

chain = chat_prompt | llm | output_parser


@app.get("/ask")
async def ask_question(question: str = Query(..., title="User Question")):
    """
    Endpoint to ask a question to the language model.

    Args:
        question (str): The question to ask.  Passed as a query parameter.

    Returns:
        str: The language model's response, formatted as a datetime string.
    """
    ai_msg = chain.invoke(
        {
            "request": question,
            "format_instructions": output_parser.get_format_instructions()
        }
    )

    # Format the datetime object to string
    return ai_msg.strftime("%Y-%m-%d %H:%M:%S") # Or any other format you prefer