from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, auth, pet, forum, channel
from app.core.database import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="洛克世界频道 API",
    description="洛克王国非官方论坛后端API",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(user.router, prefix="/api/user", tags=["用户"])
app.include_router(pet.router, prefix="/api/pets", tags=["宠物"])
app.include_router(forum.router, prefix="/api/posts", tags=["论坛"])
app.include_router(channel.router, prefix="/api/channel", tags=["世界频道"])


@app.get("/")
async def root():
    return {"message": "洛克世界频道 API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}
