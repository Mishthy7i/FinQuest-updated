from fastapi import APIRouter, Depends
from models.chatbot import ChatRequest, ChatResponse
from controllers.chatbot_controller import ask_chatbot
from utils.auth_utils import jwt_bearer

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/ask", response_model=ChatResponse)
def chatbot_ask(
    payload: ChatRequest,
    user_id: int = Depends(jwt_bearer)
):
    return ask_chatbot(user_id, payload.question)