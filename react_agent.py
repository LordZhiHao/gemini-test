import os
from typing import Dict
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Question Answering API", description="API for answering questions using LangChain and Gemini")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize LLM and tools
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.0, api_key=GEMINI_API_KEY)
tools = load_tools(["llm-math", "arxiv", "pubmed"], llm=llm)

# Create prompt template
prompt = PromptTemplate.from_template(
    """
Answer the following questions as best you can. You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""
)

# Create agent and executor
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

# Define retry logic
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry_error_callback=lambda retry_state: print(f"\nFailed after performing {retry_state.attempt_number} attempts")
)
def execute_with_retry(question: str) -> str:
    response = agent_executor.invoke({"input": question})
    return response['output']

# Define request and response models
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

# Store for ongoing tasks
tasks_store: Dict[str, Dict] = {}

# API endpoints
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(question_request: QuestionRequest):
    """
    Process a question and return the answer
    """
    try:
        result = execute_with_retry(question_request.question)
        return AnswerResponse(answer=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

# @app.post("/ask-async/{task_id}")
# async def ask_question_async(task_id: str, question_request: QuestionRequest, background_tasks: BackgroundTasks):
#     """
#     Process a question asynchronously and store the result
#     """
#     tasks_store[task_id] = {"status": "processing", "result": None}
    
#     def process_question():
#         try:
#             result = execute_with_retry(question_request.question)
#             tasks_store[task_id] = {"status": "completed", "result": result}
#         except Exception as e:
#             tasks_store[task_id] = {"status": "failed", "result": str(e)}
    
#     background_tasks.add_task(process_question)
#     return {"task_id": task_id, "status": "processing"}

# @app.get("/result/{task_id}")
# async def get_result(task_id: str):
#     """
#     Get the result of an asynchronous task
#     """
#     if task_id not in tasks_store:
#         raise HTTPException(status_code=404, detail="Task not found")
    
#     return tasks_store[task_id]

# @app.get("/health")
# async def health_check():
#     """
#     Health check endpoint
#     """
#     return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)