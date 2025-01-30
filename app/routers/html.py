from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.utils.security import get_current_user
from app.schemas.user import UserPublic

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def chat(
    request: Request,
    user: UserPublic = Depends(get_current_user)
):
    if not user:
        return RedirectResponse(url="/login")

    return templates.TemplateResponse("chat.html", {"request": request, "user": user})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "title": "Реєстрація"})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Вхід"})
