from fastapi import FastAPI
from app.routers import html, auth, chat

app = FastAPI()
app.include_router(html.router, tags=["html pages"])
app.include_router(auth.router, tags=["auth"])
app.include_router(chat.router, tags=["chat"])



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
