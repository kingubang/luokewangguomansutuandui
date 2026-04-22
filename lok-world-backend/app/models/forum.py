from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Board(Base):
    """版块"""
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    icon = Column(String(50))
    sort_order = Column(Integer, default=0)
    post_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())


class Post(Base):
    """帖子"""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    images = Column(JSON, default=[])  # 图片列表
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    board_id = Column(Integer, ForeignKey("boards.id"), index=True)
    
    # 统计数据
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    
    # 软删除
    is_deleted = Column(Integer, default=0)
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="posts")
    board = relationship("Board")
    team = relationship("Team", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):
    """评论"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)  # 楼中楼
    content = Column(Text, nullable=False)
    likes_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, server_default=func.now())
    
    # 关系
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")


class Team(Base):
    """阵容"""
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    name = Column(String(100), nullable=False)
    pets = Column(JSON, default=[])  # 宠物ID列表
    description = Column(Text)
    
    created_at = Column(DateTime, server_default=func.now())
    
    # 关系
    user = relationship("User", back_populates="teams")
    posts = relationship("Post", back_populates="team")


class PostLike(Base):
    """帖子点赞"""
    __tablename__ = "post_likes"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), index=True)
    created_at = Column(DateTime, server_default=func.now())
    
    __table_args__ = (
        # 联合唯一索引，防止重复点赞
        {"mysql_charset": "utf8mb4"},
    )


class PostCollect(Base):
    """帖子收藏"""
    __tablename__ = "post_collects"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), index=True)
    created_at = Column(DateTime, server_default=func.now())
