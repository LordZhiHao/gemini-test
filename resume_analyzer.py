import os
from io import BytesIO
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from pydantic import BaseModel, Field
from pypdf import PdfReader

app = FastAPI()
load_dotenv()
llm = GoogleGenerativeAI(
    model='gemini-1.5-flash',
    temperature=0,
    api_key=os.getenv('GEMINI_API_KEY')
)

# Add CORS middleware with specific origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def read_pdf_file(file_contents: BytesIO):
    try:
        pdf_reader = PdfReader(file_contents)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

class ResumeReport(BaseModel):
    name: str = Field(description="Name of the employee")
    address: str = Field(description="Address of the employee")
    skills: List[str] = Field(description="List of skills")
    education: List[str] = Field(description="Education details of the employee")
    experience: List[str] = Field(description="Experience details of the employee")

@app.post("/summarize_resume")
async def summarize_resume(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        contents = await file.read()
        file_contents = BytesIO(contents)
        text = read_pdf_file(file_contents)

        prompt = """
        Extract information from the resume delimited by triple backquotes and return it as JSON with the following fields:
        - name: The full name of the person
        - address: Their current address
        - skills: A list of their technical and professional skills
        - education: A list of their educational qualifications
        - experience: A list of their work experiences or internship and include all details without changing the original contexts.

        ```{text}```
        """

        prompt_template = PromptTemplate(template=prompt, input_variables=["text"])
        output_parser = JsonOutputParser(pydantic_object=ResumeReport)
        
        # Create the chain correctly
        chain = (
            prompt_template 
            | llm 
            | output_parser
        )
        
        # Invoke chain with the text
        response = chain.invoke({"text": text})
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
