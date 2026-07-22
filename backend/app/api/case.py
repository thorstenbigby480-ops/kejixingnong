"""案例中心路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.case import Case
from app.core.mode_data import get_mode_suggestions, get_mode_criteria, MODE_CRITERIA

router = APIRouter()


@router.get("/")
def list_cases(
    mode_type: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    q = db.query(Case)
    if mode_type:
        q = q.filter(Case.mode_type == mode_type)
    if keyword:
        q = q.filter(Case.title.contains(keyword))
    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": items}


@router.get("/mode-criteria")
def case_mode_criteria():
    """获取所有模式的识别标准（用于案例中心展示模式说明）"""
    return MODE_CRITERIA


@router.get("/{case_id}")
def get_case(case_id: int, db: Session = Depends(get_db)):
    c = db.get(Case, case_id)
    if not c:
        raise HTTPException(404, "案例不存在")
    return c


@router.get("/{case_id}/suggestions")
def get_case_suggestions(case_id: int, db: Session = Depends(get_db)):
    """获取案例所属模式的路径优化建议和识别标准"""
    c = db.get(Case, case_id)
    if not c:
        raise HTTPException(404, "案例不存在")
    suggestions = get_mode_suggestions(c.mode_type)
    criteria = get_mode_criteria(c.mode_type)
    return {
        "mode_type": c.mode_type,
        "suggestions": suggestions,
        "criteria": criteria.get(c.mode_type, {}),
    }
