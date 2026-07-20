"""认证路由 —— 注册/登录/JWT"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
import bcrypt
from app.database import get_db
from app.models.user import User
from app.config import settings

router = APIRouter()


def hash_password(plain: str) -> str:
    """用 bcrypt 直接哈希密码（passlib 在新版 bcrypt 上有兼容性问题）"""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """验证密码"""
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    phone: str | None = None
    role: str = "user"


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    phone: str | None
    role: str

    class Config:
        from_attributes = True


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first():
        raise HTTPException(400, "用户名或邮箱已存在")
    u = User(
        username=payload.username,
        email=payload.email,
        phone=payload.phone,
        role=payload.role if payload.role in ("user", "merchant", "admin") else "user",
        hashed_password=hash_password(payload.password),
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.username == payload.username).first()
    if not u or not verify_password(payload.password, u.hashed_password):
        raise HTTPException(401, "用户名或密码错误")
    token = create_access_token({"sub": u.username, "uid": u.id, "role": u.role})
    return {"access_token": token, "token_type": "bearer", "user": UserOut.model_validate(u).model_dump()}
