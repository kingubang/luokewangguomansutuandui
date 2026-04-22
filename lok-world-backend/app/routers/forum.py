from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forum import Post, Comment, Board, Team, PostLike, PostCollect
from app.models.pet import Pet
from app.schemas.forum import (
    PostCreate, PostResponse, PostListResponse,
    CommentCreate, CommentResponse,
    TeamCreate, TeamResponse
)
from typing import List, Optional

router = APIRouter()


# ============ 版块 ============
@router.get("/boards")
async def get_boards(db: Session = Depends(get_db)):
    """获取所有版块"""
    boards = db.query(Board).order_by(Board.sort_order).all()
    return {"list": [{"id": b.id, "name": b.name} for b in boards]}


# ============ 帖子 ============
@router.get("", response_model=PostListResponse)
async def get_post_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    board_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取帖子列表"""
    query = db.query(Post).filter(Post.is_deleted == 0)
    
    if board_id:
        query = query.filter(Post.board_id == board_id)
    if user_id:
        query = query.filter(Post.user_id == user_id)
    
    total = query.count()
    posts = query.order_by(Post.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    result = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "user_id": post.user_id,
            "user": post.user.to_dict() if post.user else {},
            "title": post.title,
            "content": post.content,
            "images": post.images or [],
            "team_id": post.team_id,
            "board_id": post.board_id,
            "board_name": post.board.name if post.board else "",
            "likes_count": post.likes_count,
            "comments_count": post.comments_count,
            "is_liked": db.query(PostLike).filter(
                PostLike.post_id == post.id,
                PostLike.user_id == current_user.id
            ).first() is not None,
            "is_collected": db.query(PostCollect).filter(
                PostCollect.post_id == post.id,
                PostCollect.user_id == current_user.id
            ).first() is not None,
            "created_at": post.created_at.isoformat() if post.created_at else None
        }
        
        # 获取阵容详情
        if post.team:
            team_pets = []
            for pet_id in (post.team.pets or []):
                pet = db.query(Pet).filter(Pet.id == pet_id).first()
                if pet:
                    team_pets.append(pet.to_dict())
            post_dict["team"] = {
                "id": post.team.id,
                "name": post.team.name,
                "pets": team_pets,
                "description": post.team.description
            }
        
        result.append(post_dict)
    
    return {
        "list": result,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{post_id}", response_model=PostResponse)
async def get_post_detail(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取帖子详情"""
    post = db.query(Post).filter(Post.id == post_id, Post.is_deleted == 0).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    
    # 更新浏览数
    post.views_count += 1
    db.commit()
    
    is_liked = db.query(PostLike).filter(
        PostLike.post_id == post.id,
        PostLike.user_id == current_user.id
    ).first() is not None
    
    is_collected = db.query(PostCollect).filter(
        PostCollect.post_id == post.id,
        PostCollect.user_id == current_user.id
    ).first() is not None
    
    return {
        "id": post.id,
        "user_id": post.user_id,
        "user": post.user.to_dict() if post.user else {},
        "title": post.title,
        "content": post.content,
        "images": post.images or [],
        "team_id": post.team_id,
        "board_id": post.board_id,
        "board_name": post.board.name if post.board else "",
        "likes_count": post.likes_count,
        "comments_count": post.comments_count,
        "views_count": post.views_count,
        "is_liked": is_liked,
        "is_collected": is_collected,
        "created_at": post.created_at.isoformat() if post.created_at else None,
        "team": {
            "id": post.team.id,
            "name": post.team.name,
            "pets": [db.query(Pet).filter(Pet.id == pid).first().to_dict() for pid in (post.team.pets or []) if db.query(Pet).filter(Pet.id == pid).first()],
            "description": post.team.description
        } if post.team else None
    }


@router.post("", response_model=PostResponse)
async def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建帖子"""
    if not data.title or not data.content:
        raise HTTPException(status_code=400, detail="标题和内容不能为空")
    
    post = Post(
        user_id=current_user.id,
        title=data.title,
        content=data.content,
        images=data.images or [],
        team_id=data.team_id,
        board_id=data.board_id
    )
    db.add(post)
    
    # 更新用户发帖数
    current_user.posts_count += 1
    
    db.commit()
    db.refresh(post)
    
    return {
        "id": post.id,
        "user_id": post.user_id,
        "user": current_user.to_dict(),
        "title": post.title,
        "content": post.content,
        "images": post.images or [],
        "team_id": post.team_id,
        "board_id": post.board_id,
        "likes_count": 0,
        "comments_count": 0,
        "is_liked": False,
        "is_collected": False,
        "created_at": post.created_at.isoformat() if post.created_at else None
    }


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除帖子"""
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == current_user.id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在或无权删除")
    
    post.is_deleted = 1
    current_user.posts_count = max(0, current_user.posts_count - 1)
    
    db.commit()
    
    return {"message": "删除成功"}


@router.post("/{post_id}/like")
async def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """点赞帖子"""
    post = db.query(Post).filter(Post.id == post_id, Post.is_deleted == 0).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    
    existing = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == current_user.id
    ).first()
    
    if existing:
        # 取消点赞
        db.delete(existing)
        post.likes_count = max(0, post.likes_count - 1)
        liked = False
    else:
        # 点赞
        like = PostLike(post_id=post_id, user_id=current_user.id)
        db.add(like)
        post.likes_count += 1
        liked = True
    
    db.commit()
    
    return {"liked": liked, "count": post.likes_count}


@router.post("/{post_id}/collect")
async def collect_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """收藏帖子"""
    post = db.query(Post).filter(Post.id == post_id, Post.is_deleted == 0).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    
    existing = db.query(PostCollect).filter(
        PostCollect.post_id == post_id,
        PostCollect.user_id == current_user.id
    ).first()
    
    if existing:
        db.delete(existing)
        collected = False
    else:
        collect = PostCollect(post_id=post_id, user_id=current_user.id)
        db.add(collect)
        collected = True
    
    db.commit()
    
    return {"collected": collected}


# ============ 评论 ============
@router.get("/{post_id}/comments")
async def get_comments(
    post_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取评论列表"""
    query = db.query(Comment).filter(Comment.post_id == post_id, Comment.parent_id == None)
    
    total = query.count()
    comments = query.order_by(Comment.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    result = []
    for comment in comments:
        comment_dict = {
            "id": comment.id,
            "post_id": comment.post_id,
            "user_id": comment.user_id,
            "user": comment.user.to_dict() if comment.user else {},
            "content": comment.content,
            "parent_id": comment.parent_id,
            "likes_count": comment.likes_count,
            "created_at": comment.created_at.isoformat() if comment.created_at else None
        }
        
        # 获取父评论
        if comment.parent:
            comment_dict["parent"] = {
                "id": comment.parent.id,
                "user_id": comment.parent.user_id,
                "user": comment.parent.user.to_dict() if comment.parent.user else {},
                "content": comment.parent.content
            }
        
        result.append(comment_dict)
    
    return {"list": result, "total": total}


@router.post("/{post_id}/comments", response_model=CommentResponse)
async def create_comment(
    post_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """发表评论"""
    post = db.query(Post).filter(Post.id == post_id, Post.is_deleted == 0).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    
    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        parent_id=data.parent_id,
        content=data.content
    )
    db.add(comment)
    
    # 更新评论数
    post.comments_count += 1
    
    db.commit()
    db.refresh(comment)
    
    return {
        "id": comment.id,
        "post_id": comment.post_id,
        "user_id": comment.user_id,
        "user": current_user.to_dict(),
        "content": comment.content,
        "parent_id": comment.parent_id,
        "likes_count": 0,
        "created_at": comment.created_at.isoformat() if comment.created_at else None
    }


# ============ 阵容 ============
@router.get("/teams/mine")
async def get_my_teams(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取我的阵容"""
    teams = db.query(Team).filter(Team.user_id == current_user.id).all()
    
    result = []
    for team in teams:
        team_pets = []
        for pet_id in (team.pets or []):
            pet = db.query(Pet).filter(Pet.id == pet_id).first()
            if pet:
                team_pets.append(pet.to_dict())
        
        result.append({
            "id": team.id,
            "user_id": team.user_id,
            "name": team.name,
            "pets": team_pets,
            "description": team.description,
            "created_at": team.created_at.isoformat() if team.created_at else None
        })
    
    return result


@router.post("/teams", response_model=TeamResponse)
async def create_team(
    data: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建阵容"""
    if len(data.pets) > 6:
        raise HTTPException(status_code=400, detail="最多选择6只宠物")
    
    team = Team(
        user_id=current_user.id,
        name=data.name,
        pets=data.pets,
        description=data.description
    )
    db.add(team)
    db.commit()
    db.refresh(team)
    
    team_pets = []
    for pet_id in team.pets:
        pet = db.query(Pet).filter(Pet.id == pet_id).first()
        if pet:
            team_pets.append(pet.to_dict())
    
    return {
        "id": team.id,
        "user_id": team.user_id,
        "name": team.name,
        "pets": team_pets,
        "description": team.description,
        "created_at": team.created_at.isoformat() if team.created_at else None
    }
