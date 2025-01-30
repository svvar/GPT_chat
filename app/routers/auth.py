from fastapi import APIRouter, Depends, status, HTTPException, Body
from fastapi.responses import JSONResponse

from app.utils.security import verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.schemas.user import UserAuth
from app.storage.crud.user_crud import check_user_exists, get_user_by_login, create_user
from app.storage.session import get_db

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK, response_class=JSONResponse)
async def login_user(
    user: UserAuth = Body(...),
    db = Depends(get_db)
):
    if not await check_user_exists(db, user.login):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Користувач не існує")

    user_in_db = await get_user_by_login(db, user.login)
    if not verify_password(user.password, user_in_db.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильний пароль")

    token = create_access_token(data={"login": user_in_db.login, "id": user_in_db.id})
    response = JSONResponse(content={"token": token}, status_code=status.HTTP_200_OK)
    response.set_cookie(key="access_token", value=f'Bearer {token}', max_age=ACCESS_TOKEN_EXPIRE_MINUTES)

    return response


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserAuth = Body(...),
    db = Depends(get_db)
):
    if await check_user_exists(db, user.login):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такий користувач вже існує")

    await create_user(db, user)
    return JSONResponse(content={"message": "Користувач успішно створений"}, status_code=status.HTTP_201_CREATED)


@router.post("/logout", status_code=status.HTTP_205_RESET_CONTENT)
async def logout_user():
    response = JSONResponse(content={"message": "Користувач вийшов з облікового запису"})
    response.delete_cookie(key="access_token")

    return response