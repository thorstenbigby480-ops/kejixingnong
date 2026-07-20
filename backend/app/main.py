"""FastAPI 入口"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import Base, engine
from app.api import auth, policy, analysis, mall, case

# 启动时创建表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=f"{settings.APP_NAME} API",
    version=settings.APP_VERSION,
    description="生态产品价值实现赋能乡村振兴的一体化智能系统",
)

# CORS（开发期放开；生产可通过 CORS_ORIGINS 环境变量限定）
cors_origins = os.getenv("CORS_ORIGINS", "*")
if cors_origins == "*":
    allow_origins = ["*"]
else:
    allow_origins = [o.strip() for o in cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件（上传目录，自动创建避免部署时报错）
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(policy.router, prefix="/api/policies", tags=["政策中心"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["智能分析"])
app.include_router(mall.router, prefix="/api/mall", tags=["商城"])
app.include_router(case.router, prefix="/api/cases", tags=["案例中心"])


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
