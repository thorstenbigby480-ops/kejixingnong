"""障碍度模型 —— 识别制约因素

简化版：基于指标归一化后的偏离度 * 权重，排序取 top N
"""
from typing import Dict, List
from app.core.indicators import ECO_INDICATORS, RURAL_INDICATORS, _min_max


def compute_obstacles(
    validated: Dict[str, float],
    eco_dim: Dict[str, float],
    rural_dim: Dict[str, float],
    top_n: int = 10,
) -> Dict[str, float]:
    obstacles: Dict[str, float] = {}
    for k, meta in {**ECO_INDICATORS, **RURAL_INDICATORS}.items():
        v_norm = _min_max(k, validated.get(k, 0.0))
        deviation = max(0.0, 1.0 - v_norm)  # 指标偏离目标程度
        obstacles[k] = round(deviation * meta["weight"], 4)
    # 排序取 top_n
    sorted_obs = dict(sorted(obstacles.items(), key=lambda x: -x[1])[:top_n])
    return sorted_obs
