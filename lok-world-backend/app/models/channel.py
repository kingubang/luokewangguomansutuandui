from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ChannelMessage(Base):
    """世界频道消息"""
    __tablename__ = "channel_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    content = Column(Text, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now(), index=True)
    
    # 关系
    user = relationship("User", back_populates="messages")
