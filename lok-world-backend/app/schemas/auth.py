from pydantic import BaseModel
from app.schemas.user import UserResponse


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse


class WechatLoginRequest(BaseModel):
    code: str


class QQLoginRequest(BaseModel):
    code: str
