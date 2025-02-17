from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, validator
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WikipediaLoader

app = FastAPI()

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant.",
        ),
        (
            "human",
            "Answer this question:\n{question}\n Here is some extra context:\n{context}",
        )
    ]
)


class WikiQuery(BaseModel):
    topic: str
    question: str

    @validator("topic")
    def topic_must_be_valid(cls, topic):
        """
        Validates that the topic is a non-empty string.
        You can add more complex validation logic here if needed,
        such as checking against a list of allowed topics or
        performing more sophisticated sanitization.
        """
        if not topic:
            raise ValueError("Topic cannot be empty")
        return topic

    @validator("question")
    def question_must_be_valid(cls, question):
        """
        Validates that the question is a non-empty string.
        Consider adding validation to prevent potentially harmful
        questions (e.g., prompt injection).
        """
        if not question:
            raise ValueError("Question cannot be empty")
        return question


@app.get("/wiki/{topic}")
async def ask_wiki(topic: str = Path(..., title="Wikipedia Topic"), question: str = Query(..., title="User Question")):
    """
    Endpoint to ask a question about a Wikipedia topic.

    Args:
        topic (str): The Wikipedia topic to search for. Passed as a path parameter.
        question (str): The question to ask. Passed as a query parameter.

    Returns:
        str: The language model's response.
    """
    try:
        query_data = WikiQuery(topic=topic, question=question)  # Validate inputs

        loader = WikipediaLoader(query=query_data.topic, load_max_docs=1)
        try:
            context_text = loader.load()[0].page_content
        except IndexError:
            return f"Could not find Wikipedia page for topic: {query_data.topic}"

        chain = prompt | llm

        ai_msg = chain.invoke(
            {
                "question": query_data.question,
                "context": context_text,
            }
        )

        return ai_msg.content

    except ValueError as e:
        return {"error": str(e)}