from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    api_key=os.getenv("GEMINI_API_KEY")
)

prompt_template = """
Let me show you how I solve math problems step by step:

Question: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls.
How many tennis balls does he have now?

Answer: Let me solve this step by step:
1. Roger starts with 5 tennis balls
2. He buys 2 cans of tennis balls
3. Each can has 3 tennis balls, so:
   2 cans * 3 balls = 6 new tennis balls
4. Total tennis balls = Initial balls + New balls
   5 + 6 = 11 tennis balls

Therefore, Roger has 11 tennis balls in total.

Now, solve this new problem using the same step-by-step approach:
Question: {question}

Answer:
"""

prompt = PromptTemplate(
    input_variables=["question"],
    template=prompt_template
)

chain = prompt | llm

def solve_math_problem(problem):
    try:
        response = chain.invoke({"question": problem})
        print(f"Problem: {problem}\n")
        print(f"Solution:\n{response.content}\n")
        print("-" * 50 + "\n")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    new_problem = """The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, 
how many apples do they have?"""
    solve_math_problem(new_problem)