"""智能分析中心 —— 核心模块：评估 + AI 模式识别 + PDF 报告"""
import json
from fastapi import APIRouter, Depends, HTTPException, Form, Header
from typing import Optional
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database import get_db
from app.models.user import User
from app.models.assessment import Assessment
from app.core.indicators import load_template, validate_data, compute_scores
from app.core.ccd_model import compute_coupling_coordination
from app.core.obstacle import compute_obstacles
from app.core.ai_advisor import recognize_mode_and_advise
from app.pdf.report import generate_report
from app.config import settings

router = APIRouter()


def _get_current_user_optional(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """可选鉴权：带了token就解析用户，没带就返回 None（匿名）"""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        uid = payload.get("uid")
        if uid is None:
            return None
        return db.query(User).filter(User.id == uid).first()
    except JWTError:
        return None


@router.get("/template")
def get_template():
    """返回数据模版结构说明（前端据此生成下载）"""
    return load_template()


@router.post("/assess")
async def assess(
    region_name: str = Form(...),
    year: Optional[int] = Form(None),
    data: str = Form(...),  # JSON 字符串
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(_get_current_user_optional),
):
    try:
        raw = json.loads(data)
    except Exception:
        raise HTTPException(400, "数据格式错误，应为 JSON 字符串")

    validated = validate_data(raw)
    eco_score, eco_dim_scores = compute_scores(validated, "eco")
    rural_score, rural_dim_scores = compute_scores(validated, "rural")
    coupling, d_value, level = compute_coupling_coordination(eco_score, rural_score)
    obstacles = compute_obstacles(validated, eco_dim_scores, rural_dim_scores)
    mode_type, mode_reason, advice = await recognize_mode_and_advise(
        region_name=region_name,
        eco_score=eco_score,
        rural_score=rural_score,
        coupling_d=d_value,
        obstacles=obstacles,
        raw_data=validated,
    )

    record = Assessment(
        user_id=current_user.id if current_user else None,
        region_name=region_name,
        year=year,
        raw_data=raw,
        eco_score=eco_score,
        rural_score=rural_score,
        coupling_d=d_value,
        coordination_level=level,
        obstacles=obstacles,
        mode_type=mode_type,
        mode_reason=mode_reason,
        advice=advice,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "region_name": record.region_name,
        "year": record.year,
        "eco_score": eco_score,
        "rural_score": rural_score,
        "eco_dim_scores": eco_dim_scores,
        "rural_dim_scores": rural_dim_scores,
        "coupling": coupling,
        "coupling_d": d_value,
        "coordination_level": level,
        "obstacles": obstacles,
        "mode_type": mode_type,
        "mode_reason": mode_reason,
        "advice": advice,
    }


@router.get("/history")
def history(
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(_get_current_user_optional),
):
    """评估历史：登录用户只看自己的记录；匿名用户看全部公开记录"""
    q = db.query(Assessment)
    # 登录用户只看自己的评估记录
    if current_user:
        q = q.filter(Assessment.user_id == current_user.id)
    q = q.order_by(Assessment.created_at.desc())
    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": items}


@router.get("/{assessment_id}")
def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    """获取单条评估记录详情"""
    a = db.get(Assessment, assessment_id)
    if not a:
        raise HTTPException(404, "评估记录不存在")
    return {
        "id": a.id,
        "user_id": a.user_id,
        "region_name": a.region_name,
        "year": a.year,
        "raw_data": a.raw_data,
        "eco_score": a.eco_score,
        "rural_score": a.rural_score,
        "coupling_d": a.coupling_d,
        "coordination_level": a.coordination_level,
        "obstacles": a.obstacles,
        "mode_type": a.mode_type,
        "mode_reason": a.mode_reason,
        "advice": a.advice,
        "pdf_path": a.pdf_path,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }


@router.get("/{assessment_id}/report")
def download_report(assessment_id: int, db: Session = Depends(get_db)):
    a = db.get(Assessment, assessment_id)
    if not a:
        raise HTTPException(404, "评估记录不存在")
    out_path = f"uploads/report_{a.id}.pdf"
    generate_report(a, out_path)
    a.pdf_path = out_path
    db.commit()
    return {"url": f"/uploads/report_{a.id}.pdf"}
