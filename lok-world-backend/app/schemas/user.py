from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    avatar: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    avatar: str
    vip_level: int
    vip_expire_at: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None


class FollowResponse(BaseModel):
    is_following: bool
