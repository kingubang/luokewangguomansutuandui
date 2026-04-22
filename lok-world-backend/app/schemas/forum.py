from pydantic import BaseModel
from typing import List, Optional
from app.schemas.user import UserResponse


class PostCreate(BaseModel):
    title: str
    content: str
    images: Optional[List[str]] = []
    team_id: Optional[int] = None
    board_id: Optional[int] = None


class PostResponse(BaseModel):
    id: int
    user_id: int
    user: dict
    title: str
    content: str
    images: List[str] = []
    team_id: Optional[int] = None
    team: Optional[dict] = None
    board_id: Optional[int] = None
    board_name: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0
    is_liked: bool = False
    is_collected: bool = False
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    list: List[PostResponse]
    total: int
    page: int
    page_size: int


class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None


class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    user: dict
    content: str
    parent_id: Optional[int] = None
    parent: Optional[dict] = None
    likes_count: int = 0
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class TeamCreate(BaseModel):
    name: str
    pets: List[int]
    description: Optional[str] = None


class TeamResponse(BaseModel):
    id: int
    user_id: int
    name: str
    pets: List[dict]
    description: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
