from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str
    user_name: str