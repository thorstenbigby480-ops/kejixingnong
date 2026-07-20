"""AI 模式识别与路径建议

策略：
1. 先用规则兜底判定模式（保证无 API Key 也能演示）
2. 若配置了 DEEPSEEK_API_KEY，则调用大模型生成 500-800 字建议
3. 若调用失败，返回规则版建议
"""
from typing import Tuple, Dict
import httpx
from app.config import settings

FIVE_MODES = [
    "生态康养型", "湿地水域型", "农业品牌型", "农文旅融合型", "城郊消费型"
]

ADVICE_TEMPLATES = {
    "生态康养型": """1. 科学规划康养功能分区，差异化布局生态康养产品。依据资源禀赋与生态承载力，划定保护性康养区、一般利用区及限制开发区，实施分级分类管控。
2. 创新土地经营机制，保障康养项目长期稳定运营。借鉴农村土地"三权分置"改革经验，通过出租、入股、合作等方式集中流转土地经营权。
3. 丰富康养业态产品体系，提升生态产品的体验价值。构建多层次、复合型的康养产品谱系，包括森林浴、疗养舱等静态康养和徒步、马术等动态康养。
4. 建立多元化投融资机制，吸引社会资本参与。构建"财政奖补+社会资本+合作经营"的多元投入体系。
5. 强化科技赋能，建立森林环境实时监测系统。运用物联网、大数据等技术发布负氧离子浓度等康养环境指标。
6. 完善利益联结机制，构建"企业+村集体+农户"的利益共同体，通过土地流转租金、合作社分红等方式惠及当地居民。""",
    "湿地水域型": """1. 完善湿地生态产品价值核算体系，建立 GEP 核算制度。通过对湿地水质净化效果的长期监测，明确关键生态效益数据。
2. 健全多元化市场化生态补偿机制。实施"土地流转定额补偿+湿地管养动态补偿"的双重补偿制度。
3. 深化"湿地+"产业融合发展路径。因地制宜发展湿地特色生态农业、生态旅游、自然科普教育等多元业态。
4. 探索湿地碳汇等新型价值实现途径。建立湿地碳汇核算方法，积极对接 CCER 交易体系。
5. 强化科技支撑与动态监测体系。建立集成水文水质、生物多样性、碳通量等多源数据的湿地生态产品价值动态监测平台。""",
    "农业品牌型": """1. 构建品牌战略体系，强化品牌差异化定位。建立"区域公用品牌+企业品牌+产品品牌"的金字塔型品牌矩阵。
2. 完善产业链标准化体系与溯源机制。运用区块链、物联网、NFC 技术实现产品质量信息不可篡改与实时可查。
3. 健全多元化利益联结机制。构建"政府—企业—农户—社会组织"多元主体协同治理模式，通过订单收购、二次返利、股权分红等方式共享品牌溢价红利。
4. 创新绿色金融产品。开发面向种植、加工、流通不同环节的差异化绿色金融产品。
5. 深化"农业品牌+"产业融合路径。推动"农业品牌+文旅""农业品牌+研学"等多元业态融合发展。""",
    "农文旅融合型": """1. 构建系统化的规划引导与空间管控体系。编制覆盖生态环境治理、文化遗产保护、农业产业布局与文旅业态发展的综合性规划。
2. 深化资源禀赋的多维度挖掘与特色化表达。构建多层次的资源价值阐释体系，注重在地文化的活态传承与创新表达。
3. 构建生态产业化与产业生态化的协同发展机制。坚持"在保护中发展、在发展中保护"，将生态承载力作为产业开发的前置约束。
4. 完善"立体式"利益联结机制。探索农户以资源使用权、资金、劳动力等多种要素入股的模式。
5. 推动多元业态的系统集成与功能互补。系统规划"文旅+科普研学""文旅+康养度假"等多元业态组合。""",
    "城郊消费型": """1. 构建种养循环的绿色生产体系。建立"种植—养殖—废弃物资源化—生态种植"的闭环循环体系。
2. 深化农文旅多元业态融合。围绕四季物候特征开发差异化的季节性体验产品，统筹规划园区功能分区。
3. 推动品牌化运营与 IP 化打造。建立"区域特色品种+企业品牌+产品品牌"的多层次品牌体系。
4. 创新"电商平台+社群营销"的多元化营销模式。建设区域性地产特色农产品电商平台，发展会员制、认养制、预售制等新型消费模式。
5. 建立联农带农的利益共享机制。通过订单收购、技术指导、就业吸纳、土地流转租金、入股分红等多元方式构建利益联结机制。
6. 强化科技赋能与人才驱动。引进现代农业技术，高度重视"新农人"群体，建立产学研合作机制。""",
}


def _rule_based_mode(validated: Dict[str, float]) -> Tuple[str, str]:
    """规则判定：基于关键指标"""
    forest = validated.get("森林覆盖率（%）", 0)
    water_quality = validated.get("主要水体水质断面达标率（%）", 0)
    agri_total = validated.get("农林牧渔业总产值（万元）", 0)
    rural_income = validated.get("农村居民人均可支配收入（元）", 0)
    patent = validated.get("三种专利申请授权量（件）", 0)
    urban_rate = validated.get("常住人口城镇化率（%）", 0)

    if forest >= 50 and patent < 50:
        return "生态康养型", f"森林覆盖率达 {forest}%，且创新活力偏低，符合依托森林/气候资源的康养型特征"
    if water_quality >= 80:
        return "湿地水域型", f"水质断面达标率达 {water_quality}%，水域生态资源突出，符合湿地水域型特征"
    if agri_total >= 50000:
        return "农业品牌型", f"农林牧渔业总产值达 {agri_total} 万元，农业基础雄厚，符合农业品牌型特征"
    if urban_rate >= 60 and rural_income >= 30000:
        return "城郊消费型", f"城镇化率 {urban_rate}%、农村人均可支配收入 {rural_income} 元，符合城郊消费型特征"
    return "农文旅融合型", "各项指标均衡发展，符合农文旅融合型综合发展特征"


async def _call_llm(prompt: str) -> str:
    """调用 DeepSeek（OpenAI 兼容格式）"""
    if not settings.DEEPSEEK_API_KEY:
        return ""
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
        "max_tokens": 1500,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
            json=payload,
            headers=headers,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


def _build_prompt(region, eco_score, rural_score, d, obstacles, raw) -> str:
    return f"""你是乡村振兴生态产品价值实现领域的专家。请基于以下评估结果，判定该地区属于五种发展模式中的哪一种，并给出500-800字的差异化路径优化建议。

五种模式：
1. 生态康养型（依托森林、气候、温泉、山地等）
2. 湿地水域型（依托湿地、水域等）
3. 农业品牌型（依托区域公用品牌）
4. 农文旅融合型（农业、文化、旅游三产融合）
5. 城郊消费型（依托城郊区位、面向城市居民）

地区：{region}
生态产品价值实现成效得分：{eco_score}/100
乡村振兴水平得分：{rural_score}/100
耦合协调度D值：{d}
主要障碍因子：{obstacles}
原始指标摘要：森林覆盖率={raw.get('森林覆盖率（%）', 'N/A')}%，水质达标率={raw.get('主要水体水质断面达标率（%）', 'N/A')}%，农林牧渔业总产值={raw.get('农林牧渔业总产值（万元）', 'N/A')}万元，农村人均可支配收入={raw.get('农村居民人均可支配收入（元）', 'N/A')}元

请输出格式：
【模式判定】：xxx型
【判定依据】：xxx（150字内）
【路径优化建议】：
（500-800字，针对障碍度最高的2-3个维度提出具体可操作建议）
"""


async def recognize_mode_and_advise(
    region_name: str,
    eco_score: float,
    rural_score: float,
    coupling_d: float,
    obstacles: Dict[str, float],
    raw_data: Dict[str, float],
) -> Tuple[str, str, str]:
    # 1. 规则兜底判定模式
    rule_mode, rule_reason = _rule_based_mode(raw_data)
    # 2. 优先调用 LLM 生成建议
    advice = ""
    if settings.DEEPSEEK_API_KEY:
        prompt = _build_prompt(region_name, eco_score, rural_score, coupling_d, obstacles, raw_data)
        try:
            advice = await _call_llm(prompt)
        except Exception:
            advice = ""
    # 3. LLM 失败/未配置，用模板建议
    if not advice:
        advice = f"【模式判定】：{rule_mode}\n【判定依据】：{rule_reason}\n\n【路径优化建议】\n{ADVICE_TEMPLATES[rule_mode]}"
        return rule_mode, rule_reason, advice
    # 4. LLM 成功：从输出里解析模式（覆盖规则版）
    llm_mode, llm_reason = _parse_llm_output(advice, rule_mode, rule_reason)
    return llm_mode, llm_reason, advice


def _parse_llm_output(text: str, fallback_mode: str, fallback_reason: str) -> Tuple[str, str]:
    """从 LLM 输出里抽取模式判定和依据"""
    import re
    mode = fallback_mode
    reason = fallback_reason
    # 模式判定
    mode_match = re.search(r"【模式判定】[：:]\s*([^\n]+)", text)
    if mode_match:
        m = mode_match.group(1).strip()
        for name in FIVE_MODES:
            if name in m:
                mode = name
                break
    # 判定依据
    reason_match = re.search(r"【判定依据】[：:]\s*([^\n]+(?:\n[^【\[]+)?)", text)
    if reason_match:
        reason = reason_match.group(1).strip().split("\n")[0][:200]
    return mode, reason
