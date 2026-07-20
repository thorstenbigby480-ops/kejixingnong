"""评估记录模型"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    region_name = Column(String(128), nullable=False)
    year = Column(Integer, nullable=True)
    raw_data = Column(JSON, nullable=True)
    eco_score = Column(Float, nullable=True)
    rural_score = Column(Float, nullable=True)
    coupling_d = Column(Float, nullable=True)
    coordination_level = Column(String(32), nullable=True)
    obstacles = Column(JSON, nullable=True)
    mode_type = Column(String(64), nullable=True)
    mode_reason = Column(Text, nullable=True)
    advice = Column(Text, nullable=True)
    pdf_path = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
