from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, RedirectResponse

from app.storage.session import get_db
from app.utils.security import get_current_user
from app.utils.gpt_tools import process_message, clear_memory
from app.schemas.chat import ChatMessage
from app.schemas.user import UserPublic

router = APIRouter()

@router.post("/ask-gpt")
async def ask_gpt(
    message: ChatMessage,
    user: UserPublic = Depends(get_current_user),
    db = Depends(get_db)
):
    if not user:
        return RedirectResponse(url="/login")

    response_text = await process_message(db, user.id, message.message)
    return JSONResponse(content={"response": response_text}, status_code=status.HTTP_200_OK)

@router.post("/clear-memories", status_code=status.HTTP_200_OK)
async def clear_memories(
    user: UserPublic = Depends(get_current_user),
    db = Depends(get_db)
):
    if not user:
        return

    await clear_memory(db, user.id)

