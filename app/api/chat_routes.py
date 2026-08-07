from fastapi import APIRouter

from app.rag.llm import ask_llm
from app.rag.vector_store import search_documents
from app.schemas.chat_schema import ChatRequest

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/")
async def chat(chat_request: ChatRequest):

    context = search_documents(
        chat_request.question
    )

    answer = ask_llm(
        chat_request.question,
        context,
    )

    return {
        "question": chat_request.question,
        "answer": answer,
    }