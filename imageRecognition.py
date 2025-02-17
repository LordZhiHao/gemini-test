import os, base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from typing import Dict

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def encode_image(image_content: bytes) -> str:
    return base64.b64encode(image_content).decode()

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)) -> Dict[str, str]:
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, detail="Invalid file type. Only JPEG and PNG are allowed.")
    
    if file.size > 5_000_000:
        raise HTTPException(400, detail="File too large. Maximum size is 5MB.")
    
    try:
        contents = await file.read()
        image = encode_image(contents)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a nutrition expert capable of analyzing food images and providing detailed nutritional advice."),
            ("human", [
                """Analyze the image and provide a detailed nutritional analysis of the food in the image.""",
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image}",
                        "detail": "high",
                    },
                },
            ]),
        ])
        
        chain = prompt | llm
        res = await chain.ainvoke({"image": image})
        return {"analysis": res.content}
    except Exception as e:
        raise HTTPException(500, detail=f"An error occurred while processing the image, {e}")