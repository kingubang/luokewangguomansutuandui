from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    get_password_hash, verify_password,
    create_access_token, create_refresh_token, decode_token
)
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, WechatLoginRequest, QQLoginRequest
import httpx
import json

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    """账号密码登录"""
    user = db.query(User).filter(User.username == data.username).first()
    
    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 生成Token
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }


@router.post("/register")
async def register(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    """用户注册"""
    # 检查用户名是否存在
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 创建用户
    user = User(
        username=data.username,
        password_hash=get_password_hash(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 生成Token
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }


@router.post("/refresh")
async def refresh_token(
    refresh_token: str = Query(...)
):
    """刷新Token"""
    payload = decode_token(refresh_token)
    
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="无效的刷新Token")
    
    user_id = payload.get("sub")
    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }


@router.post("/wechat")
async def wechat_login(
    data: WechatLoginRequest,
    db: Session = Depends(get_db)
):
    """微信登录"""
    # 通过code获取openid
    # 实际项目中需要配置微信AppID和AppSecret
    # 这里简化处理
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.weixin.qq.com/sns/oauth2/access_token",
                params={
                    "appid": "YOUR_WECHAT_APPID",
                    "secret": "YOUR_WECHAT_APPSECRET",
                    "code": data.code,
                    "grant_type": "authorization_code"
                }
            )
            token_data = response.json()
            openid = token_data.get("openid")
        except:
            # 模拟登录（开发环境）
            openid = f"wechat_{data.code}"
    
    # 查找或创建用户
    user = db.query(User).filter(User.wechat_openid == openid).first()
    
    if not user:
        user = User(
            username=f"用户{openid[-6:]}",
            wechat_openid=openid,
            avatar="/images/default-avatar.png"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # 生成Token
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }


@router.post("/qq")
async def qq_login(
    data: QQLoginRequest,
    db: Session = Depends(get_db)
):
    """QQ登录"""
    # 通过code获取openid
    # 实际项目中需要配置QQ AppID和AppSecret
    async with httpx.AsyncClient() as client:
        try:
            # 获取access_token
            token_response = await client.get(
                "https://graph.qq.com/oauth2.0/token",
                params={
                    "grant_type": "authorization_code",
                    "client_id": "YOUR_QQ_APPID",
                    "client_secret": "YOUR_QQ_APPSECRET",
                    "code": data.code,
                    "redirect_uri": "https://example.com/oauth/qq/callback"
                }
            )
            token_data = dict(p.split("=") for p in token_response.text.split("&"))
            access_token = token_data.get("access_token")
            
            # 获取openid
            openid_response = await client.get(
                "https://graph.qq.com/oauth2.0/me",
                params={"access_token": access_token}
            )
            openid_data = json.loads(openid_response.text.replace("callback(", "").replace(");", ""))
            openid = openid_data.get("openid")
        except:
            # 模拟登录（开发环境）
            openid = f"qq_{data.code}"
    
    # 查找或创建用户
    user = db.query(User).filter(User.qq_openid == openid).first()
    
    if not user:
        user = User(
            username=f"用户{openid[-6:]}",
            qq_openid=openid,
            avatar="/images/default-avatar.png"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # 生成Token
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }
