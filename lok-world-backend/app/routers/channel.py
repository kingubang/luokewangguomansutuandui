from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.channel import ChannelMessage
from app.schemas.channel import MessageResponse
from typing import List
import redis
from app.core.config import settings

router = APIRouter()

# Redis客户端
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


@router.get("/history", response_model=List[MessageResponse])
async def get_history(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """获取历史消息"""
    messages = db.query(ChannelMessage).order_by(
        ChannelMessage.created_at.desc()
    ).limit(limit).all()
    
    result = []
    for msg in reversed(messages):
        result.append({
            "id": msg.id,
            "user_id": msg.user_id,
            "user": msg.user.to_dict() if msg.user else {},
            "content": msg.content,
            "created_at": msg.created_at.isoformat() if msg.created_at else None
        })
    
    return result


@router.post("/send", response_model=MessageResponse)
async def send_message(
    content: str = Query(..., min_length=1, max_length=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """发送消息"""
    # 检查发言频率限制（60秒1条）
    rate_key = f"channel:rate:{current_user.id}"
    if redis_client.get(rate_key):
        raise HTTPException(status_code=429, detail="发言太频繁，请稍后再试")
    
    # 设置限速
    redis_client.setex(rate_key, 60, "1")
    
    # 过滤敏感词（简化处理）
    # 实际项目中需要更完善的敏感词过滤
    forbidden_words = ["test", "测试"]
    for word in forbidden_words:
        if word in content:
            raise HTTPException(status_code=400, detail="内容包含敏感词")
    
    # 保存消息
    message = ChannelMessage(
        user_id=current_user.id,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # 缓存最近消息到Redis
    cache_key = "channel:latest"
    redis_client.lpush(cache_key, message.id)
    redis_client.ltrim(cache_key, 0, 99)  # 保留最近100条
    
    return {
        "id": message.id,
        "user_id": message.user_id,
        "user": current_user.to_dict(),
        "content": message.content,
        "created_at": message.created_at.isoformat() if message.created_at else None
    }
