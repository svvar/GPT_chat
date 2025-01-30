from pydantic import BaseModel

class UserAuth(BaseModel):
    login: str
    password: str

class UserPublic(BaseModel):
    id: int
    login: str