import os
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langserve import add_routes
import uvicorn
from pydantic import BaseModel

# Load environment
load_dotenv()

class TranslationRequest(BaseModel):
    language: str
    text: str

app = FastAPI(title="Translation Service")

# Configure OpenRouter
llm = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo"),
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.3,
    model_kwargs={
        "headers": {
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Translation Service"
        }
    }
)

# Create chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate to {language}:"),
    ("user", "{text}")
])
chain = prompt | llm | StrOutputParser()

# Add route
add_routes(
    app,
    chain,
    path="/translate",
    input_type=TranslationRequest
)

@app.get("/")
def health_check():
    return {"status": "running"}

if __name__ == "__main__":
    print("Starting server at http://localhost:8000")
    uvicorn.run(
        app,
        host="127.0.0.1",  # Explicit localhost
        port=8000,
        log_level="debug"  # More verbose logging
    )