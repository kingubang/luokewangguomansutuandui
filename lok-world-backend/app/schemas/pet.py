from pydantic import BaseModel
from typing import List, Optional


class PetResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    image_url: Optional[str] = None
    bloodline: Optional[str] = None
    stats: dict = {}
    recommended_nature: List[str] = []
    recommended_talent: List[str] = []
    recommended_skills: List[str] = []
    capture_location: Optional[str] = None
    capture_condition: Optional[str] = None
    capture_time: Optional[str] = None
    can_evolve: bool = False
    evolution_forms: List[dict] = []
    has_albinism: bool = False
    albinism_image: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class PetListResponse(BaseModel):
    list: List[PetResponse]
    total: int
    page: int
    page_size: int
