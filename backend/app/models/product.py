"""商品 & 订单模型"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    category = Column(String(64), nullable=False)  # 粮食/果蔬/茶叶/特产/畜禽/加工品
    origin = Column(String(128), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    image_url = Column(String(512), nullable=True)
    eco_cert = Column(String(256), nullable=True)
    description = Column(Text, nullable=True)
    merchant_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, default=0)
    status = Column(String(32), default="pending")  # pending/paid/shipped/done/cancelled
    address = Column(String(256), nullable=True)
    phone = Column(String(32), nullable=True)
    items = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
