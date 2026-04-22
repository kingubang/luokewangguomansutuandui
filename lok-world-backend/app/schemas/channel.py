from pydantic import BaseModel


class MessageResponse(BaseModel):
    id: int
    user_id: int
    user: dict
    content: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


from typing import Optional
