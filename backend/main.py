from fastapi import FastAPI
from typing import List, Dict

from models import ChatRequest
from chat_services import chat_completion

app = FastAPI()

message_history: List[Dict[str, str]] = []

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/chat")
async def chat(request: ChatRequest):
    global message_history

    message_history = chat_completion(
        topic=request.topic, 
        user_name=request.user_name, 
        message_history=message_history
    )

    return {"message_history": message_history}
