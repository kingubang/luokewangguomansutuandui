from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=True)  # 第三方登录时为空
    avatar = Column(String(500), default="/images/default-avatar.png")
    bio = Column(String(200), default="")
    vip_level = Column(Integer, default=0)
    vip_expire_at = Column(DateTime, nullable=True)
    
    # 第三方登录
    wechat_openid = Column(String(100), unique=True, nullable=True, index=True)
    wechat_unionid = Column(String(100), nullable=True, index=True)
    qq_openid = Column(String(100), unique=True, nullable=True, index=True)
    
    # 统计
    posts_count = Column(Integer, default=0)
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关系
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    teams = relationship("Team", back_populates="user")
    messages = relationship("ChannelMessage", back_populates="user")
    
    def to_dict(self, include_sensitive=False):
        data = {
            "id": self.id,
            "username": self.username,
            "avatar": self.avatar,
            "vip_level": self.vip_level,
            "vip_expire_at": self.vip_expire_at.isoformat() if self.vip_expire_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        return data


class UserFollow(Base):
    __tablename__ = "user_follows"
    
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, index=True)
    following_id = Column(Integer, index=True)
    created_at = Column(DateTime, server_default=func.now())
