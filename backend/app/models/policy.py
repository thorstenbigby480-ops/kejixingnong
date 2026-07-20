"""政策模型"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    category = Column(String(64), nullable=False)  # 生态产品价值实现 / 乡村振兴
    level = Column(String(32), nullable=False)     # 国家级 / 省级 / 地市级
    region = Column(String(128), nullable=True)
    publish_date = Column(DateTime(timezone=True), nullable=True)
    source = Column(String(128), nullable=True)
    url = Column(String(512), nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
