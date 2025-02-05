from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Import the CORSMiddleware class from fastapi.middleware.cors for enabling CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080",
                   "http://localhost:5173"],  # Vue.js default dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a Pydantic model for the request body
class TranslationRequest(BaseModel):
    input_language: str
    output_language: str
    text_input: str

# Create a Pydantic model for the response
class TranslationResponse(BaseModel):
    translated_text: str

def call_gemini(input_language: str, output_language: str, text_input: str) -> str:
    try:
        # load llm
        load_dotenv()
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY)

        # create prompt
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful assistant that translates {input_language} to {output_language}. Translate the use sentence.",
            ),
            (
                "human",
                "{text_input}",
            ),
        ])

        # create chain
        chain = prompt | llm

        # invoke chain
        ai_msg = chain.invoke({
            'input_language': input_language,
            'output_language': output_language,
            'text_input': text_input,
        })

        # return llm output
        return ai_msg.content

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate/", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    try:
        translated_text = call_gemini(
            request.input_language,
            request.output_language,
            request.text_input
        )
        return TranslationResponse(translated_text=translated_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the Translation API"}