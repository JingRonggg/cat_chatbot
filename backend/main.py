from fastapi import FastAPI
from typing import List, Dict
import re

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
    print(message_history)
    latest_assistant_msg = next((msg['content'] for msg in reversed(message_history) if msg['role'] == 'assistant'), None)
    link = re.search(r'\((https?://[^\)]+)\)', latest_assistant_msg)
    if link:
        return {"message_history": link.group(1)}
    return {"message_history": latest_assistant_msg}
