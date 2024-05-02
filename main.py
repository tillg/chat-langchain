"""Main entrypoint for the app."""
import logging
from typing import List, Optional, Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langsmith import Client
from backend import ollamaWrapper
import os
from dotenv import load_dotenv

from backend.messages import Message
import backend.chain 

from backend.constants import DEFAULT_MODEL

load_dotenv()

api_key = os.environ.get("LANGCHAIN_API_KEY")
print("API KEY: ", api_key)
client = Client(api_key=api_key)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.post("/chat/{model}")
def chat(model: str, chat_history: List[Message] | None, question: str):
    logger = logging.getLogger(__name__)
    logger.info(f"Model: {model}, question: {question}")
    try:
        answer = backend.chain.chat(
            llm_model=model, chat_history=None, question=question)
        logger.info(f"Answer: {answer}")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting answer")
    return {"answer": answer}

@app.get("/models")
async def get_models():
    logger = logging.getLogger(__name__)
    logger.info("Getting models")
    try:
        models = ollamaWrapper.get_models()
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error getting models")
    return_val = {"models": models}
    if DEFAULT_MODEL in models:
        return_val["default_model"] = DEFAULT_MODEL
    return return_val

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
