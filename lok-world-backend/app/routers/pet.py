from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.pet import Pet
from app.schemas.pet import PetResponse, PetListResponse
from typing import List, Optional

router = APIRouter()


@router.get("", response_model=PetListResponse)
async def get_pet_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取宠物列表"""
    query = db.query(Pet)
    
    if category:
        query = query.filter(Pet.category == category)
    
    if keyword:
        query = query.filter(Pet.name.like(f"%{keyword}%"))
    
    total = query.count()
    pets = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "list": [pet.to_dict() for pet in pets],
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/search", response_model=List[PetResponse])
async def search_pets(
    keyword: str = Query(...),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """搜索宠物"""
    pets = db.query(Pet).filter(
        Pet.name.like(f"%{keyword}%")
    ).limit(limit).all()
    
    return [pet.to_dict() for pet in pets]


@router.get("/{pet_id}", response_model=PetResponse)
async def get_pet_detail(
    pet_id: int,
    db: Session = Depends(get_db)
):
    """获取宠物详情"""
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    
    if not pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    
    return pet.to_dict()


@router.post("/compare")
async def compare_pets(
    ids: List[int] = Query(..., min_length=2, max_length=2),
    db: Session = Depends(get_db)
):
    """对比宠物"""
    if len(ids) != 2:
        raise HTTPException(status_code=400, detail="需要选择2只宠物")
    
    pets = db.query(Pet).filter(Pet.id.in_(ids)).all()
    
    if len(pets) != 2:
        raise HTTPException(status_code=404, detail="宠物不存在")
    
    return {"pets": [pet.to_dict() for pet in pets]}


@router.get("/categories/list")
async def get_categories(
    db: Session = Depends(get_db)
):
    """获取所有系别"""
    categories = db.query(Pet.category).distinct().all()
    return {"list": [c[0] for c in categories if c[0]]}
