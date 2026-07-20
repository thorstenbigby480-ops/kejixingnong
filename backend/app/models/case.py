"""案例模型"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Case(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    region = Column(String(128), nullable=True)
    mode_type = Column(String(64), nullable=False)  # 五种模式之一
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    image_url = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
