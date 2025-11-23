"""Chatbot API Routes"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import get_logger
from models.database import get_db
from services.ai_service import process_query

logger = get_logger(__name__)
router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chatbot", response_model=None)
async def chatbot(req: ChatRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    """Process a user query via the AI chatbot."""
    logger.info(f"Chatbot query: {req.question}")
    return await process_query(req.question, db)
