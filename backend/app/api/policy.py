"""政策中心路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.policy import Policy

router = APIRouter()


@router.get("/")
def list_policies(
    category: Optional[str] = None,
    level: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    q = db.query(Policy)
    if category:
        q = q.filter(Policy.category == category)
    if level:
        q = q.filter(Policy.level == level)
    if keyword:
        q = q.filter(Policy.title.contains(keyword))
    total = q.count()
    items = q.order_by(Policy.publish_date.desc().nullslast()).offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": items}


@router.get("/{policy_id}")
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    p = db.get(Policy, policy_id)
    if not p:
        raise HTTPException(404, "政策不存在")
    return p
