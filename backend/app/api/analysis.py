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
from app.core.ccd_model import compute_coupling_coordination, COORDINATION_LEVELS
from app.core.obstacle import compute_obstacles
from app.core.ai_advisor import recognize_mode_and_advise
from app.core.mode_data import (
    MODE_CRITERIA, MODE_SUGGESTIONS, AHP_WEIGHTS,
    CLUSTER_RESULTS, COORDINATION_LEVELS as D_LEVELS,
    get_mode_criteria, get_mode_suggestions,
)
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
        "mode_criteria": MODE_CRITERIA.get(mode_type, {}),
        "structured_suggestions": get_mode_suggestions(mode_type) if mode_type else [],
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


@router.get("/mode-criteria")
def mode_criteria(mode_type: Optional[str] = None):
    """获取五种模式的量化识别标准（阈值、特征、核心要素）"""
    return get_mode_criteria(mode_type)


@router.get("/mode-suggestions/{mode_type}")
def mode_suggestions(mode_type: str):
    """获取指定模式的路径优化建议（5-6条结构化建议）"""
    suggestions = get_mode_suggestions(mode_type)
    if not suggestions:
        raise HTTPException(404, f"未找到模式 '{mode_type}' 的优化建议")
    return {"mode_type": mode_type, "count": len(suggestions), "suggestions": suggestions}


@router.get("/ahp-weights")
def ahp_weights():
    """获取 AHP 层次分析法组合权重数据"""
    return AHP_WEIGHTS


@router.get("/cluster-results")
def cluster_results():
    """获取层次聚类分析结果（含PC1/PC2主成分坐标，用于散点图）"""
    return {"count": len(CLUSTER_RESULTS), "items": CLUSTER_RESULTS}


@router.get("/coordination-levels")
def coordination_levels():
    """获取耦合协调度等级划分标准（10级）"""
    return {"levels": D_LEVELS}


@router.get("/coupling-calculate")
def coupling_calculate(u1: float, u2: float, alpha: float = 0.5, beta: float = 0.5):
    """独立耦合协调度计算工具：输入两个系统得分，返回耦合度C、协调度D、协调等级"""
    coupling, d_value, level = compute_coupling_coordination(u1, u2, alpha, beta)
    # 找到对应的等级颜色
    level_color = "#666"
    for lv in D_LEVELS:
        range_parts = lv["range"].split("-")
        lo, hi = float(range_parts[0]), float(range_parts[1])
        if lo <= d_value < hi:
            level_color = lv["color"]
            break
    return {
        "u1": u1,
        "u2": u2,
        "coupling_c": coupling,
        "coordination_t": round(alpha * (u1 / 100 if u1 > 1 else u1) + beta * (u2 / 100 if u2 > 1 else u2), 4),
        "coordination_d": d_value,
        "level": level,
        "level_color": level_color,
    }


@router.post("/obstacle-diagnose")
def obstacle_diagnose(data: str = Form(...)):
    """独立障碍因子诊断工具：输入指标JSON，返回各指标障碍度排名"""
    try:
        raw = json.loads(data)
    except Exception:
        raise HTTPException(400, "数据格式错误，应为 JSON 字符串")
    validated = validate_data(raw)
    eco_score, eco_dim_scores = compute_scores(validated, "eco")
    rural_score, rural_dim_scores = compute_scores(validated, "rural")
    obstacles = compute_obstacles(validated, eco_dim_scores, rural_dim_scores, top_n=15)
    # 添加指标中文名称
    from app.core.indicators import ECO_INDICATORS, RURAL_INDICATORS
    all_indicators = {**ECO_INDICATORS, **RURAL_INDICATORS}
    result = []
    for k, v in obstacles.items():
        meta = all_indicators.get(k, {})
        result.append({
            "key": k,
            "name": meta.get("name", k),
            "obstacle_degree": v,
            "weight": meta.get("weight", 0),
        })
    return {
        "eco_score": eco_score,
        "rural_score": rural_score,
        "obstacles": result,
    }


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
