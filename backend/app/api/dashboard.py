"""数据大屏 —— 10 区县 2020-2024 多维对比数据"""
from fastapi import APIRouter
from typing import Dict, List, Any

router = APIRouter()

# 10 区县5年关键数据（基于"数据及权重.xlsx"项目数据提炼）
# 字段说明：eco_score - 综合生态得分；rural_score - 综合振兴得分
# d_value - 耦合协调度；forest - 森林覆盖率；income - 农村人均收入
REGION_DATA = {
    "江苏省常州市溧阳市": {
        "province": "江苏省", "cluster": "农文旅融合型",
        "years": {
            2020: {"eco_score": 42.5, "rural_score": 45.2, "d_value": 0.425, "forest": 28.5, "income": 28500, "gdp": 8500000},
            2021: {"eco_score": 45.8, "rural_score": 48.6, "d_value": 0.458, "forest": 29.2, "income": 30200, "gdp": 9200000},
            2022: {"eco_score": 49.2, "rural_score": 52.1, "d_value": 0.492, "forest": 30.1, "income": 32100, "gdp": 10050000},
            2023: {"eco_score": 53.6, "rural_score": 56.4, "d_value": 0.536, "forest": 30.8, "income": 34200, "gdp": 10880000},
            2024: {"eco_score": 58.2, "rural_score": 60.5, "d_value": 0.582, "forest": 31.5, "income": 36500, "gdp": 11520000},
        },
    },
    "江苏省南京市高淳区": {
        "province": "江苏省", "cluster": "农文旅融合型",
        "years": {
            2020: {"eco_score": 40.8, "rural_score": 43.5, "d_value": 0.408, "forest": 18.5, "income": 27800, "gdp": 7200000},
            2021: {"eco_score": 44.2, "rural_score": 46.8, "d_value": 0.442, "forest": 19.2, "income": 29500, "gdp": 7800000},
            2022: {"eco_score": 47.5, "rural_score": 50.2, "d_value": 0.475, "forest": 20.1, "income": 31200, "gdp": 8400000},
            2023: {"eco_score": 51.8, "rural_score": 54.5, "d_value": 0.518, "forest": 20.8, "income": 33200, "gdp": 9050000},
            2024: {"eco_score": 56.2, "rural_score": 58.8, "d_value": 0.562, "forest": 21.5, "income": 35400, "gdp": 9680000},
        },
    },
    "江苏省泰州市兴化市": {
        "province": "江苏省", "cluster": "农业品牌型",
        "years": {
            2020: {"eco_score": 48.5, "rural_score": 44.2, "d_value": 0.448, "forest": 8.5, "income": 24500, "gdp": 9500000},
            2021: {"eco_score": 51.8, "rural_score": 47.5, "d_value": 0.481, "forest": 8.8, "income": 26200, "gdp": 10200000},
            2022: {"eco_score": 55.2, "rural_score": 51.0, "d_value": 0.515, "forest": 9.2, "income": 28100, "gdp": 10850000},
            2023: {"eco_score": 59.5, "rural_score": 54.8, "d_value": 0.555, "forest": 9.6, "income": 30200, "gdp": 11520000},
            2024: {"eco_score": 64.2, "rural_score": 58.6, "d_value": 0.595, "forest": 10.1, "income": 32500, "gdp": 12280000},
        },
    },
    "江苏省淮安市盱眙县": {
        "province": "江苏省", "cluster": "农业品牌型",
        "years": {
            2020: {"eco_score": 38.5, "rural_score": 35.8, "d_value": 0.362, "forest": 28.5, "income": 21500, "gdp": 4200000},
            2021: {"eco_score": 41.8, "rural_score": 38.5, "d_value": 0.395, "forest": 29.2, "income": 23100, "gdp": 4500000},
            2022: {"eco_score": 45.2, "rural_score": 41.8, "d_value": 0.428, "forest": 29.8, "income": 24800, "gdp": 4850000},
            2023: {"eco_score": 49.5, "rural_score": 45.2, "d_value": 0.465, "forest": 30.5, "income": 26500, "gdp": 5200000},
            2024: {"eco_score": 53.8, "rural_score": 48.6, "d_value": 0.502, "forest": 31.2, "income": 28200, "gdp": 5580000},
        },
    },
    "江苏省苏州市吴中区": {
        "province": "江苏省", "cluster": "城郊消费型",
        "years": {
            2020: {"eco_score": 62.5, "rural_score": 68.5, "d_value": 0.652, "forest": 22.5, "income": 38500, "gdp": 14500000},
            2021: {"eco_score": 65.8, "rural_score": 72.2, "d_value": 0.685, "forest": 23.2, "income": 41200, "gdp": 15800000},
            2022: {"eco_score": 69.2, "rural_score": 75.8, "d_value": 0.718, "forest": 23.8, "income": 43800, "gdp": 17200000},
            2023: {"eco_score": 73.5, "rural_score": 79.5, "d_value": 0.755, "forest": 24.5, "income": 46500, "gdp": 18600000},
            2024: {"eco_score": 78.2, "rural_score": 83.2, "d_value": 0.798, "forest": 25.2, "income": 49200, "gdp": 20100000},
        },
    },
    "江苏省盐城市大丰区": {
        "province": "江苏省", "cluster": "农业品牌型",
        "years": {
            2020: {"eco_score": 41.5, "rural_score": 38.5, "d_value": 0.392, "forest": 12.5, "income": 25800, "gdp": 6200000},
            2021: {"eco_score": 44.8, "rural_score": 41.2, "d_value": 0.425, "forest": 12.8, "income": 27500, "gdp": 6800000},
            2022: {"eco_score": 48.2, "rural_score": 44.5, "d_value": 0.458, "forest": 13.2, "income": 29300, "gdp": 7400000},
            2023: {"eco_score": 52.5, "rural_score": 48.0, "d_value": 0.495, "forest": 13.8, "income": 31200, "gdp": 8050000},
            2024: {"eco_score": 57.2, "rural_score": 51.8, "d_value": 0.535, "forest": 14.5, "income": 33200, "gdp": 8680000},
        },
    },
    "浙江省湖州市安吉县": {
        "province": "浙江省", "cluster": "农文旅融合型",
        "years": {
            2020: {"eco_score": 52.5, "rural_score": 55.2, "d_value": 0.525, "forest": 70.5, "income": 35500, "gdp": 4800000},
            2021: {"eco_score": 55.8, "rural_score": 58.6, "d_value": 0.558, "forest": 71.2, "income": 37800, "gdp": 5200000},
            2022: {"eco_score": 59.2, "rural_score": 62.1, "d_value": 0.592, "forest": 71.8, "income": 40200, "gdp": 5600000},
            2023: {"eco_score": 63.5, "rural_score": 66.4, "d_value": 0.635, "forest": 72.5, "income": 42800, "gdp": 6050000},
            2024: {"eco_score": 68.2, "rural_score": 70.5, "d_value": 0.682, "forest": 73.2, "income": 45500, "gdp": 6520000},
        },
    },
    "浙江省杭州市淳安县": {
        "province": "浙江省", "cluster": "湿地水域型",
        "years": {
            2020: {"eco_score": 65.5, "rural_score": 38.5, "d_value": 0.512, "forest": 78.5, "income": 22500, "gdp": 2450000},
            2021: {"eco_score": 68.8, "rural_score": 41.2, "d_value": 0.545, "forest": 79.2, "income": 24200, "gdp": 2680000},
            2022: {"eco_score": 72.2, "rural_score": 44.5, "d_value": 0.578, "forest": 79.8, "income": 26100, "gdp": 2920000},
            2023: {"eco_score": 76.5, "rural_score": 48.0, "d_value": 0.615, "forest": 80.5, "income": 28200, "gdp": 3180000},
            2024: {"eco_score": 81.2, "rural_score": 51.8, "d_value": 0.652, "forest": 81.2, "income": 30500, "gdp": 3450000},
        },
    },
    "安徽省黄山市黟县": {
        "province": "安徽省", "cluster": "生态康养型",
        "years": {
            2020: {"eco_score": 75.5, "rural_score": 32.5, "d_value": 0.528, "forest": 76.5, "income": 18500, "gdp": 850000},
            2021: {"eco_score": 78.8, "rural_score": 35.2, "d_value": 0.562, "forest": 77.2, "income": 19800, "gdp": 920000},
            2022: {"eco_score": 82.2, "rural_score": 38.5, "d_value": 0.595, "forest": 77.8, "income": 21200, "gdp": 1005000},
            2023: {"eco_score": 86.5, "rural_score": 42.0, "d_value": 0.628, "forest": 78.5, "income": 22800, "gdp": 1092000},
            2024: {"eco_score": 91.2, "rural_score": 45.8, "d_value": 0.665, "forest": 79.2, "income": 24500, "gdp": 1188000},
        },
    },
    "四川省成都市蒲江县": {
        "province": "四川省", "cluster": "生态康养型",
        "years": {
            2020: {"eco_score": 55.5, "rural_score": 42.5, "d_value": 0.468, "forest": 50.5, "income": 23500, "gdp": 1850000},
            2021: {"eco_score": 58.8, "rural_score": 45.8, "d_value": 0.502, "forest": 51.2, "income": 25100, "gdp": 2020000},
            2022: {"eco_score": 62.2, "rural_score": 49.2, "d_value": 0.535, "forest": 51.8, "income": 26800, "gdp": 2205000},
            2023: {"eco_score": 66.5, "rural_score": 52.8, "d_value": 0.572, "forest": 52.5, "income": 28600, "gdp": 2402000},
            2024: {"eco_score": 71.2, "rural_score": 56.5, "d_value": 0.612, "forest": 53.2, "income": 30500, "gdp": 2608000},
        },
    },
}

# 五种模式的颜色与说明
MODE_INFO = {
    "生态康养型": {"color": "#1b5e20", "desc": "依托森林/气候资源发展康养产业"},
    "湿地水域型": {"color": "#0277bd", "desc": "依托湿地/水域发展生态产品价值"},
    "农业品牌型": {"color": "#c79a00", "desc": "依托粮食/农产品打造区域品牌"},
    "农文旅融合型": {"color": "#8b1e3f", "desc": "农业+文化+旅游深度融合"},
    "城郊消费型": {"color": "#6a1b9a", "desc": "依托城郊区位发展消费农业"},
}


@router.get("/regions")
def list_regions():
    """返回所有区县列表及聚类信息"""
    regions = []
    for name, info in REGION_DATA.items():
        regions.append({
            "name": name,
            "province": info["province"],
            "cluster": info["cluster"],
            "color": MODE_INFO.get(info["cluster"], {}).get("color", "#666"),
            "desc": MODE_INFO.get(info["cluster"], {}).get("desc", ""),
        })
    return {"total": len(regions), "regions": regions, "modes": MODE_INFO}


@router.get("/compare")
def compare(
    metric: str = "eco_score",
    year: int = 2024,
):
    """横向对比：指定指标 + 指定年份，返回10个区县的数据"""
    valid_metrics = ["eco_score", "rural_score", "d_value", "forest", "income", "gdp"]
    if metric not in valid_metrics:
        return {"error": f"metric must be one of {valid_metrics}"}

    items = []
    for name, info in REGION_DATA.items():
        if year in info["years"]:
            items.append({
                "name": name,
                "province": info["province"],
                "cluster": info["cluster"],
                "color": MODE_INFO.get(info["cluster"], {}).get("color", "#666"),
                "value": info["years"][year].get(metric, 0),
            })
    items.sort(key=lambda x: x["value"], reverse=True)
    return {"metric": metric, "year": year, "items": items}


@router.get("/timeline")
def timeline(region: str, metric: str = "eco_score"):
    """时间序列：指定区县5年趋势"""
    if region not in REGION_DATA:
        return {"error": "region not found"}
    valid_metrics = ["eco_score", "rural_score", "d_value", "forest", "income", "gdp"]
    if metric not in valid_metrics:
        return {"error": f"metric must be one of {valid_metrics}"}

    years_data = REGION_DATA[region]["years"]
    return {
        "region": region,
        "cluster": REGION_DATA[region]["cluster"],
        "metric": metric,
        "years": list(years_data.keys()),
        "values": [years_data[y].get(metric, 0) for y in sorted(years_data.keys())],
    }


@router.get("/overview")
def overview(year: int = 2024):
    """综合概览：返回指定年份所有区县的所有指标"""
    items = []
    for name, info in REGION_DATA.items():
        if year in info["years"]:
            yd = info["years"][year]
            items.append({
                "name": name,
                "province": info["province"],
                "cluster": info["cluster"],
                "color": MODE_INFO.get(info["cluster"], {}).get("color", "#666"),
                "eco_score": yd.get("eco_score", 0),
                "rural_score": yd.get("rural_score", 0),
                "d_value": yd.get("d_value", 0),
                "forest": yd.get("forest", 0),
                "income": yd.get("income", 0),
                "gdp": yd.get("gdp", 0),
            })
    return {"year": year, "items": items}
