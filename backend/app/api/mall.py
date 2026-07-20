"""商城路由 —— 商品 + 购物车 + 订单（支付先用模拟）"""
import json
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_db
from app.models.product import Product, Order

router = APIRouter()


# ============= 商品 =============
@router.get("/products")
def list_products(
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    q = db.query(Product).filter(Product.is_approved == True)  # noqa: E712
    if category:
        q = q.filter(Product.category == category)
    if keyword:
        q = q.filter(Product.name.contains(keyword))
    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": items}


@router.get("/products/{pid}")
def get_product(pid: int, db: Session = Depends(get_db)):
    p = db.get(Product, pid)
    if not p:
        raise HTTPException(404, "商品不存在")
    return p


@router.post("/products")
def create_product(payload: dict, db: Session = Depends(get_db)):
    p = Product(
        name=payload["name"],
        category=payload["category"],
        origin=payload.get("origin"),
        price=payload["price"],
        stock=payload.get("stock", 0),
        image_url=payload.get("image_url"),
        eco_cert=payload.get("eco_cert"),
        description=payload.get("description"),
        merchant_id=payload.get("merchant_id"),
        is_approved=payload.get("is_approved", False),
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


# ============= 订单 =============
class OrderItem(BaseModel):
    product_id: int
    name: str
    price: float
    qty: int
    image_url: Optional[str] = None


class OrderCreate(BaseModel):
    buyer_id: Optional[int] = None
    items: List[OrderItem]
    address: Optional[str] = None
    phone: Optional[str] = None
    remark: Optional[str] = None


def _get_current_user(request: Request) -> dict:
    """从 Authorization header 解析 JWT，返回用户信息"""
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return {}
    try:
        from jose import jwt as _jwt
        from app.config import settings
        token = auth.split(" ", 1)[1]
        payload = _jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return {"uid": payload.get("uid"), "username": payload.get("sub"), "role": payload.get("role")}
    except Exception:
        return {}


@router.post("/orders")
def create_order(payload: OrderCreate, request: Request, db: Session = Depends(get_db)):
    """创建订单：自动计算总价，扣减库存"""
    user = _get_current_user(request)
    buyer_id = payload.buyer_id or user.get("uid")
    if not buyer_id:
        raise HTTPException(401, "请先登录后下单")

    if not payload.items:
        raise HTTPException(400, "订单不能为空")

    # 校验商品 & 计算总价 & 扣库存
    total = 0.0
    items_snapshot = []
    for it in payload.items:
        p = db.get(Product, it.product_id)
        if not p:
            raise HTTPException(404, f"商品不存在: id={it.product_id}")
        if p.stock < it.qty:
            raise HTTPException(400, f"库存不足: {p.name} 仅剩 {p.stock}")
        # 扣减库存
        p.stock -= it.qty
        # 用数据库实际价格为准
        line_total = round(p.price * it.qty, 2)
        total += line_total
        items_snapshot.append({
            "product_id": p.id,
            "name": p.name,
            "price": p.price,
            "qty": it.qty,
            "image_url": p.image_url,
            "line_total": line_total,
        })

    total = round(total, 2)
    o = Order(
        buyer_id=buyer_id,
        total_amount=total,
        status="pending",
        address=payload.address,
        phone=payload.phone,
        items=json.dumps(items_snapshot, ensure_ascii=False),
    )
    db.add(o)
    db.commit()
    db.refresh(o)
    return {
        "id": o.id,
        "buyer_id": o.buyer_id,
        "total_amount": o.total_amount,
        "status": o.status,
        "address": o.address,
        "phone": o.phone,
        "items": items_snapshot,
        "created_at": o.created_at.isoformat() if o.created_at else None,
    }


@router.get("/orders")
def list_my_orders(request: Request, db: Session = Depends(get_db)):
    """查询当前用户订单列表"""
    user = _get_current_user(request)
    if not user.get("uid"):
        raise HTTPException(401, "请先登录")
    orders = db.query(Order).filter(Order.buyer_id == user["uid"]).order_by(Order.created_at.desc()).all()
    result = []
    for o in orders:
        try:
            items = json.loads(o.items) if o.items else []
        except Exception:
            items = []
        result.append({
            "id": o.id,
            "buyer_id": o.buyer_id,
            "total_amount": o.total_amount,
            "status": o.status,
            "address": o.address,
            "phone": o.phone,
            "items": items,
            "created_at": o.created_at.isoformat() if o.created_at else None,
        })
    return {"total": len(result), "items": result}


@router.get("/orders/{order_id}")
def get_order(order_id: int, request: Request, db: Session = Depends(get_db)):
    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(404, "订单不存在")
    try:
        items = json.loads(o.items) if o.items else []
    except Exception:
        items = []
    return {
        "id": o.id,
        "buyer_id": o.buyer_id,
        "total_amount": o.total_amount,
        "status": o.status,
        "address": o.address,
        "phone": o.phone,
        "items": items,
        "created_at": o.created_at.isoformat() if o.created_at else None,
    }


@router.post("/orders/{order_id}/pay")
def pay_order(order_id: int, request: Request, db: Session = Depends(get_db)):
    """模拟支付：直接把订单置为已支付"""
    user = _get_current_user(request)
    if not user.get("uid"):
        raise HTTPException(401, "请先登录")
    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(404, "订单不存在")
    if o.buyer_id != user["uid"]:
        raise HTTPException(403, "无权操作他人订单")
    if o.status != "pending":
        raise HTTPException(400, f"订单状态异常：{o.status}")
    o.status = "paid"
    db.commit()
    return {"status": o.status, "message": "支付成功（模拟）", "order_id": o.id}


@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: int, request: Request, db: Session = Depends(get_db)):
    """取消订单：恢复库存"""
    user = _get_current_user(request)
    if not user.get("uid"):
        raise HTTPException(401, "请先登录")
    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(404, "订单不存在")
    if o.buyer_id != user["uid"]:
        raise HTTPException(403, "无权操作他人订单")
    if o.status not in ("pending",):
        raise HTTPException(400, f"订单已 {o.status}，无法取消")
    # 恢复库存
    try:
        items = json.loads(o.items) if o.items else []
        for it in items:
            p = db.get(Product, it.get("product_id"))
            if p:
                p.stock += it.get("qty", 0)
    except Exception:
        pass
    o.status = "cancelled"
    db.commit()
    return {"status": o.status, "message": "订单已取消", "order_id": o.id}
