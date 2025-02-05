from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

def call_gemini(input_language, output_language, text_input):
    # load llm
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY)

    # create prompt
    prompt = ChatPromptTemplate.from_messages(
        [
        (
            "system",
            "You are a helpful assistant that translates {input_language} to {output_language}. Translate the use sentence.",
        ),
        (
            "human",
            "{text_input}",
        ),
    ]
    )

    # create chain
    chain = prompt | llm

    # invoke chain
    ai_msg = chain.invoke(
        {
            'input_language': input_language,
            'output_language': output_language,
            'text_input': text_input,
        }
    )

    # return llm output
    return ai_msg.content

# example call
print(call_gemini('English', 'German', 'I like programming'))