from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, get_password_hash, verify_password
from app.models.user import User, UserFollow
from app.schemas.user import UserResponse, UserUpdate, FollowResponse
from typing import List
import os
import uuid

router = APIRouter()


@router.get("/info", response_model=UserResponse)
async def get_user_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    return current_user.to_dict()


@router.put("/info", response_model=UserResponse)
async def update_user_info(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新用户信息"""
    if data.username:
        # 检查用户名是否已被占用
        existing = db.query(User).filter(
            User.username == data.username,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="用户名已被占用")
        current_user.username = data.username
    
    if data.bio is not None:
        current_user.bio = data.bio
    
    db.commit()
    db.refresh(current_user)
    return current_user.to_dict()


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传头像"""
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="不支持的图片格式")
    
    # 保存文件
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join("uploads", "avatars", filename)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # 更新用户头像
    current_user.avatar = f"/uploads/avatars/{filename}"
    db.commit()
    
    return {"avatar_url": current_user.avatar}


@router.post("/follow/{user_id}", response_model=FollowResponse)
async def follow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """关注用户"""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能关注自己")
    
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 检查是否已关注
    existing = db.query(UserFollow).filter(
        UserFollow.follower_id == current_user.id,
        UserFollow.following_id == user_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="已关注")
    
    # 创建关注关系
    follow = UserFollow(follower_id=current_user.id, following_id=user_id)
    db.add(follow)
    
    # 更新统计
    current_user.following_count += 1
    target_user.followers_count += 1
    
    db.commit()
    
    return {"is_following": True}


@router.delete("/follow/{user_id}", response_model=FollowResponse)
async def unfollow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """取消关注"""
    follow = db.query(UserFollow).filter(
        UserFollow.follower_id == current_user.id,
        UserFollow.following_id == user_id
    ).first()
    
    if not follow:
        raise HTTPException(status_code=400, detail="未关注")
    
    target_user = db.query(User).filter(User.id == user_id).first()
    
    db.delete(follow)
    
    # 更新统计
    current_user.following_count = max(0, current_user.following_count - 1)
    if target_user:
        target_user.followers_count = max(0, target_user.followers_count - 1)
    
    db.commit()
    
    return {"is_following": False}
