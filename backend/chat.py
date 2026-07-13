from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .ollama_client import OllamaClient

router = APIRouter()
ollama_client = OllamaClient()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    try:
        response = ollama_client.send_message(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
