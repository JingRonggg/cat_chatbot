from pydantic import BaseModel

class ChatRequest(BaseModel):
    topic: str
    user_name: str