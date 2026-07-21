"""指标体系与权重 —— 基于项目实际AHP层次分析结果

数据来源：
- 生态产品价值实现成效评价指标体系（11项指标，3个准则层）
- 乡村振兴水平评价指标体系（15项指标，5个准则层）
- 组合权重来自AHP专家打分
"""
from typing import Dict, Any, Tuple

# 生态产品价值实现成效评价指标体系（11项指标，3个准则层）
ECO_INDICATORS = {
    # 生态效益（3项）
    "重要生态功能保护区面积（公顷）": {"weight": 0.1283, "subsystem": "生态效益"},
    "主要水体水质断面达标率（%）": {"weight": 0.0074, "subsystem": "生态效益"},
    "空气环境质量优良率（%）": {"weight": 0.0889, "subsystem": "生态效益"},
    # 经济效益（3项）
    "地区生产总值（万元）": {"weight": 0.2676, "subsystem": "经济效益"},
    "全区粮食播种面积（公顷）": {"weight": 0.1978, "subsystem": "经济效益"},
    "农产品产出（吨）": {"weight": 0.1738, "subsystem": "经济效益"},
    # 社会效益（5项）
    "常住人口城镇化率（%）": {"weight": 0.0066, "subsystem": "社会效益"},
    "新增就业人数（人）": {"weight": 0.0486, "subsystem": "社会效益"},
    "农村居民人均可支配收入（元）": {"weight": 0.0346, "subsystem": "社会效益"},
    "城乡低保标准（元/月）": {"weight": 0.0161, "subsystem": "社会效益"},
    "一般公共服务支出（万元）": {"weight": 0.0304, "subsystem": "社会效益"},
}

# 乡村振兴水平评价指标体系（15项指标，5个准则层）
RURAL_INDICATORS = {
    # 产业兴旺（3项）
    "粮食总产量（吨）": {"weight": 0.2140, "dim": "产业兴旺"},
    "农业机械总动力/农作物播种面积（千瓦/亩）": {"weight": 0.0288, "dim": "产业兴旺"},
    "农林牧渔业总产值（万元）": {"weight": 0.1868, "dim": "产业兴旺"},
    # 生态宜居（3项）
    "森林覆盖率（%）": {"weight": 0.0416, "dim": "生态宜居"},
    "污水处理厂集中处理率（%）": {"weight": 0.0211, "dim": "生态宜居"},
    "农村卫生厕所普及率（%）": {"weight": 0.0091, "dim": "生态宜居"},
    # 乡风文明（3项）
    "普通中学专任教师数/在校学生数（%）": {"weight": 0.0355, "dim": "乡风文明"},
    "图书馆个数（个）": {"weight": 0.0428, "dim": "乡风文明"},
    "固定互联网宽带接入用户（户）": {"weight": 0.0274, "dim": "乡风文明"},
    # 治理有效（3项）
    "农林水事务支出占比（%）": {"weight": 0.0545, "dim": "治理有效"},
    "卫生室/卫生机构数量（个）": {"weight": 0.0217, "dim": "治理有效"},
    "三种专利申请授权量（件）": {"weight": 0.1352, "dim": "治理有效"},
    # 生活富裕（3项）
    "农村人均可支配收入（元）": {"weight": 0.1012, "dim": "生活富裕"},
    "农村人均消费支出（元）": {"weight": 0.0378, "dim": "生活富裕"},
    "人均道路面积（平方米）": {"weight": 0.0424, "dim": "生活富裕"},
}

# 指标参考阈值（用于 min-max 归一化，基于10个样本区县2020-2024年实际数据范围设定）
REFERENCE_RANGES = {
    # 生态产品价值实现指标
    "重要生态功能保护区面积（公顷）": (0, 200000),
    "主要水体水质断面达标率（%）": (0, 100),
    "空气环境质量优良率（%）": (0, 100),
    "地区生产总值（万元）": (0, 30000000),
    "全区粮食播种面积（公顷）": (0, 200000),
    "农产品产出（吨）": (0, 1500000),
    "常住人口城镇化率（%）": (0, 100),
    "新增就业人数（人）": (0, 50000),
    "农村居民人均可支配收入（元）": (0, 60000),
    "城乡低保标准（元/月）": (0, 2000),
    "一般公共服务支出（万元）": (0, 500000),
    # 乡村振兴指标
    "粮食总产量（吨）": (0, 1000000),
    "农业机械总动力/农作物播种面积（千瓦/亩）": (0, 5),
    "农林牧渔业总产值（万元）": (0, 2000000),
    "森林覆盖率（%）": (0, 80),
    "污水处理厂集中处理率（%）": (0, 100),
    "农村卫生厕所普及率（%）": (0, 100),
    "普通中学专任教师数/在校学生数（%）": (0, 20),
    "图书馆个数（个）": (0, 50),
    "固定互联网宽带接入用户（户）": (0, 500000),
    "农林水事务支出占比（%）": (0, 30),
    "卫生室/卫生机构数量（个）": (0, 500),
    "三种专利申请授权量（件）": (0, 20000),
    "农村人均可支配收入（元）": (0, 60000),
    "农村人均消费支出（元）": (0, 40000),
    "人均道路面积（平方米）": (0, 30),
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
