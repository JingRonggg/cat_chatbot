from fastapi import FastAPI
import re

from models import ChatRequest
from chat_services import chat_completion

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/v1/chat")
async def chat(request: ChatRequest):
    message_history = chat_completion(
        prompt=request.prompt, 
        user_name=request.user_name, 
    )
    print(message_history)
    if message_history == 'requires_action':
        return {"message_history": "Could you repeat yourself?"}
    latest_assistant_msg = next((msg['content'] for msg in reversed(message_history) if msg['role'] == 'assistant'), None)
    link = re.search(r'\((https?://[^\)]+)\)', latest_assistant_msg)
    if link:
        return {"message_history": link.group(1)}
    return {"message_history": latest_assistant_msg}
