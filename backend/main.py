from fastapi import FastAPI
from typing import List, Dict

from models import ChatRequest
from chat_services import chat_completion

app = FastAPI()

message_history: List[Dict[str, str]] = []

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/v1/chat")
async def chat(request: ChatRequest):
    global message_history
    message_history = chat_completion(
        prompt=request.prompt, 
        user_name=request.user_name, 
        message_history=message_history
    )
    latest_assistant_msg = next((msg['content'] for msg in reversed(message_history) if msg['role'] == 'assistant'), None)
    return {"message_history": latest_assistant_msg}
