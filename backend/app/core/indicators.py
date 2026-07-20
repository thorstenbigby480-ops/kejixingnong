"""指标体系与权重 —— 按文献标准初版，后续可调

注：以下权重和指标体系为文献标准近似值，后续团队可调。
参考《生态产品价值实现成效评价》《乡村振兴水平评价指标体系》。
"""
from typing import Dict, Any, Tuple

# 生态产品价值实现成效评价指标体系
ECO_INDICATORS = {
    "重要生态功能保护区面积（公顷）": {"weight": 0.15, "subsystem": "ecological"},
    "主要水体水质断面达标率（%）": {"weight": 0.12, "subsystem": "ecological"},
    "空气环境质量优良率（%）": {"weight": 0.10, "subsystem": "ecological"},
    "森林覆盖率（%）": {"weight": 0.13, "subsystem": "ecological"},
    "地区生产总值（万元）": {"weight": 0.10, "subsystem": "economic"},
    "农林牧渔业总产值（万元）": {"weight": 0.10, "subsystem": "economic"},
    "粮食总产量（吨）": {"weight": 0.10, "subsystem": "economic"},
    "新增就业人数（人）": {"weight": 0.08, "subsystem": "social"},
    "农村居民人均可支配收入（元）": {"weight": 0.12, "subsystem": "social"},
}

# 乡村振兴水平评价指标体系（按产业/生态/乡风/治理/生活五维）
RURAL_INDICATORS = {
    "粮食播种面积（公顷）": {"weight": 0.10, "dim": "产业兴旺"},
    "农产品产出（吨）": {"weight": 0.10, "dim": "产业兴旺"},
    "农业机械总动力/农作物播种面积（千瓦/亩）": {"weight": 0.05, "dim": "产业兴旺"},
    "森林覆盖率（%）": {"weight": 0.10, "dim": "生态宜居"},
    "污水处理厂集中处理率（%）": {"weight": 0.10, "dim": "生态宜居"},
    "农村卫生厕所普及率（%）": {"weight": 0.05, "dim": "生态宜居"},
    "普通中学专任教师数/在校学生数（%）": {"weight": 0.08, "dim": "乡风文明"},
    "图书馆个数（个）": {"weight": 0.07, "dim": "乡风文明"},
    "一般公共服务支出（万元）": {"weight": 0.08, "dim": "治理有效"},
    "农林水事务支出占比（%）": {"weight": 0.07, "dim": "治理有效"},
    "卫生机构数量（个）": {"weight": 0.05, "dim": "治理有效"},
    "三种专利申请授权量（件）": {"weight": 0.05, "dim": "治理有效"},
    "常住人口城镇化率（%）": {"weight": 0.05, "dim": "生活富裕"},
    "城乡低保标准（元/月）": {"weight": 0.05, "dim": "生活富裕"},
    "农村人均可支配收入（元）": {"weight": 0.05, "dim": "生活富裕"},
    "农村人均消费支出（元）": {"weight": 0.03, "dim": "生活富裕"},
    "人均道路面积（平方米）": {"weight": 0.02, "dim": "生活富裕"},
    "固定互联网宽带接入用户（户）": {"weight": 0.05, "dim": "生活富裕"},
}

# 指标参考阈值（用于 min-max 归一化，可后续用全国/全省统计年鉴替换）
REFERENCE_RANGES = {
    "重要生态功能保护区面积（公顷）": (0, 50000),
    "主要水体水质断面达标率（%）": (0, 100),
    "空气环境质量优良率（%）": (0, 100),
    "森林覆盖率（%）": (0, 80),
    "地区生产总值（万元）": (0, 1000000),
    "农林牧渔业总产值（万元）": (0, 200000),
    "粮食总产量（吨）": (0, 50000),
    "新增就业人数（人）": (0, 10000),
    "农村居民人均可支配收入（元）": (0, 50000),
    "粮食播种面积（公顷）": (0, 50000),
    "农产品产出（吨）": (0, 50000),
    "农业机械总动力/农作物播种面积（千瓦/亩）": (0, 5),
    "污水处理厂集中处理率（%）": (0, 100),
    "农村卫生厕所普及率（%）": (0, 100),
    "普通中学专任教师数/在校学生数（%）": (0, 20),
    "图书馆个数（个）": (0, 50),
    "一般公共服务支出（万元）": (0, 50000),
    "农林水事务支出占比（%）": (0, 30),
    "卫生机构数量（个）": (0, 100),
    "三种专利申请授权量（件）": (0, 1000),
    "常住人口城镇化率（%）": (0, 100),
    "城乡低保标准（元/月）": (0, 3000),
    "农村人均可支配收入（元）": (0, 50000),
    "农村人均消费支出（元）": (0, 40000),
    "人均道路面积（平方米）": (0, 30),
    "固定互联网宽带接入用户（户）": (0, 10000),
}


def load_template() -> dict:
    return {
        "eco_indicators": list(ECO_INDICATORS.keys()),
        "rural_indicators": list(RURAL_INDICATORS.keys()),
        "reference_ranges": REFERENCE_RANGES,
        "fields": ["地区", "年份"] + list(ECO_INDICATORS.keys()) + list(RURAL_INDICATORS.keys()),
    }


def validate_data(raw: Dict[str, Any]) -> Dict[str, float]:
    """把任意输入转换为 float"""
    out = {}
    for k, v in raw.items():
        try:
            out[k] = float(v)
        except (TypeError, ValueError):
            out[k] = 0.0
    return out


def _min_max(name: str, value: float) -> float:
    vmin, vmax = REFERENCE_RANGES.get(name, (0, 1))
    if vmax - vmin == 0:
        return 0.5
    norm = (value - vmin) / (vmax - vmin)
    return max(0.0, min(1.0, norm))


def compute_scores(validated: Dict[str, float], kind: str) -> Tuple[float, Dict[str, float]]:
    """加权综合评分（0-100）
    kind: "eco" 或 "rural"
    """
    table = ECO_INDICATORS if kind == "eco" else RURAL_INDICATORS
    total = 0.0
    dim_scores: Dict[str, float] = {}
    dim_weights: Dict[str, float] = {}

    for k, meta in table.items():
        v = _min_max(k, validated.get(k, 0.0))
        w = meta["weight"]
        total += v * w
        dim = meta.get("dim") or meta.get("subsystem", "综合")
        dim_scores[dim] = dim_scores.get(dim, 0.0) + v * w
        dim_weights[dim] = dim_weights.get(dim, 0.0) + w

    for d in dim_scores:
        if dim_weights[d] > 0:
            dim_scores[d] = round(dim_scores[d] / dim_weights[d] * 100, 2)

    return round(total * 100, 2), dim_scores
