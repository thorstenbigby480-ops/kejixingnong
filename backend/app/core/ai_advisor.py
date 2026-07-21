"""AI 模式识别与路径建议

策略：
1. 先用规则兜底判定模式（基于项目实际聚类分析的识别阈值）
2. 若配置了 DEEPSEEK_API_KEY，则调用大模型生成 500-800 字建议
3. 若调用失败，返回规则版建议

模式识别规则来自《五种模式识别与路径优化建议》
聚类结果基于10个样本区县2024年数据层次聚类分析
"""
from typing import Tuple, Dict
import httpx
from app.config import settings

FIVE_MODES = [
    "生态康养型", "湿地水域型", "农业品牌型", "农文旅融合型", "城郊消费型"
]

# 五种模式的完整路径优化建议（来自项目文档）
ADVICE_TEMPLATES = {
    "生态康养型": """1. 科学规划康养功能分区，差异化布局生态康养产品。依据资源禀赋与生态承载力，划定保护性康养区、一般利用区及限制开发区，实施分级分类管控，构建"社区—片区—区域"多级网络体系。
2. 创新土地经营机制，保障康养项目长期稳定运营。借鉴农村土地"三权分置"改革经验，通过出租、入股、合作等方式集中流转土地经营权，流转期限建议10—20年。
3. 丰富康养业态产品体系，提升生态产品的体验价值。构建多层次、复合型的康养产品谱系，包括森林浴、森林冥想、疗养舱、森林徒步、自然教育等静态与动态康养业态。
4. 建立多元化投融资机制，吸引社会资本参与。构建"财政奖补+社会资本+合作经营"的多元投入体系，探索混合所有制康养项目运营模式。
5. 强化科技赋能，建立森林环境实时监测系统。运用物联网、大数据、AI等技术监测森林环境，发布负氧离子浓度等康养环境指标。
6. 完善利益联结机制，构建"企业+村集体+农户"的利益共同体，通过土地流转租金、劳务用工、合作社分红等方式惠及当地居民。""",
    "湿地水域型": """1. 构建科学规范的生态产品价值核算体系。基于GEP框架，涵盖洪水调蓄量、污染物削减量、固碳释氧量等湿地特有生态效益，建立长期监测与核算制度。
2. 完善多元化市场化生态补偿机制。实施跨区域横向生态补偿、湿地信用交易、生态产品政府采购等多元补偿方式，建立"土地流转定额补偿+湿地管养动态补偿"的双重补偿制度。
3. 深化"湿地+"产业融合发展路径。因地制宜发展湿地特色生态农业、生态旅游、自然科普教育、文创产品等多元业态，实现湿地生态价值多元化转化。
4. 探索湿地碳汇等新型价值实现途径。建立湿地碳汇核算方法，积极对接CCER交易体系，探索"蓝碳"生态系统碳汇质押贷款等绿色金融创新。
5. 强化科技支撑与动态监测体系。建立集成水文水质、生物多样性、碳通量等多源数据的湿地生态产品价值动态监测平台，形成"监测—评估—预警—反馈"闭环管理。""",
    "农业品牌型": """1. 构建品牌战略体系，强化品牌差异化定位。建立"区域公用品牌+企业品牌+产品品牌"的金字塔型品牌矩阵，明确品牌核心价值与市场定位。
2. 完善产业链标准化体系与溯源机制。运用区块链、物联网、NFC技术实现产品质量信息不可篡改与实时可查，建立第三方认证与全程溯源体系。
3. 健全多元化利益联结机制。构建"政府—企业—农户—社会组织"多元主体协同治理模式，通过订单收购、二次返利、股权分红、溢价分成等方式共享品牌溢价红利。
4. 创新绿色金融产品。开发茶园贷、设备升级贷、仓单质押贷等面向种植、加工、流通不同环节的差异化绿色金融产品，探索生态资产价值核算融资。
5. 深化"农业品牌+"产业融合路径。推动"农业品牌+文旅""农业品牌+研学""农业品牌+康养"等多元业态融合发展，对接国际市场提升品牌影响力。""",
    "农文旅融合型": """1. 构建系统化的规划引导与空间管控体系。编制覆盖生态环境治理、文化遗产保护、农业产业布局与文旅业态发展的综合性规划，强化空间统筹。
2. 深化资源禀赋的多维度挖掘与特色化表达。构建多层次的资源价值阐释体系，挖掘科学价值、文化价值、美学价值，注重在地文化的活态传承与创新表达。
3. 构建生态产业化与产业生态化的协同发展机制。坚持"在保护中发展、在发展中保护"，将生态承载力作为产业开发的前置约束，建设"生态银行"平台。
4. 完善"立体式"利益联结机制。探索"资源变资产、资金变股金、农民变股东"的改革路径，建立农户以资源使用权、资金、劳动力等多种要素入股的模式。
5. 推动多元业态的系统集成与功能互补。系统规划"文旅+科普研学""文旅+康养度假""文旅+体育赛事""文旅+特色农业体验"等多元业态组合。""",
    "城郊消费型": """1. 构建种养循环的绿色生产体系。建立"种植—养殖—废弃物资源化—生态种植"的闭环循环体系，推进绿色防控、肥水一体化、智能温控技术应用。
2. 深化农文旅多元业态融合。围绕四季物候特征开发差异化的季节性体验产品，统筹规划园区功能分区，推动从"一日游"向"多日度假"升级。
3. 推动品牌化运营与IP化打造。建立"区域特色品种+企业品牌+产品品牌"的多层次品牌体系，培育具有市场辨识度的特色IP。
4. 创新"电商平台+社群营销"的多元化营销模式。建设区域性地产特色农产品电商平台，发展会员制、认养制、预售制等新型消费模式。
5. 建立联农带农的利益共享机制。通过"龙头企业/生态园+合作社+农户"模式，以订单收购、技术指导、就业吸纳、土地流转租金、入股分红等多元方式构建利益联结机制。
6. 强化科技赋能与人才驱动。引进现代农业技术，高度重视"新农人"群体，建立产学研合作机制，为乡村振兴提供人才支撑。""",
}


def _rule_based_mode(validated: Dict[str, float]) -> Tuple[str, str]:
    """基于项目实际聚类分析阈值的规则判定

    阈值来自《五种模式识别与路径优化建议》中的识别规则
    """
    forest = validated.get("森林覆盖率（%）", 0)
    water_quality = validated.get("主要水体水质断面达标率（%）", 0)
    air_quality = validated.get("空气环境质量优良率（%）", 0)
    urban_rate = validated.get("常住人口城镇化率（%）", 0)
    gdp = validated.get("地区生产总值（万元）", 0)
    rural_income = validated.get("农村居民人均可支配收入（元）", 0)
    new_jobs = validated.get("新增就业人数（人）", 0)
    grain_area = validated.get("全区粮食播种面积（公顷）", 0)
    agri_output = validated.get("农产品产出（吨）", 0)
    eco_protection = validated.get("重要生态功能保护区面积（公顷）", 0)
    patent = validated.get("三种专利申请授权量（件）", 0)

    # 模式一：生态康养型
    # 森林覆盖率 ≥65%，城镇化率 ≤55%，空气优良率 ≥80%
    if forest >= 65 and urban_rate <= 55 and air_quality >= 80:
        return "生态康养型", f"森林覆盖率达 {forest}%（≥65%），城镇化率 {urban_rate}%（≤55%），空气优良率 {air_quality}%（≥80%），符合依托森林/气候资源的生态康养型特征"

    # 模式二：湿地水域型
    # 水质达标率 ≥95%，重要生态功能保护区占比高
    if water_quality >= 95 and eco_protection >= 40000:
        return "湿地水域型", f"水质断面达标率达 {water_quality}%（≥95%），重要生态功能保护区面积 {eco_protection} 公顷，符合湿地水域型特征"

    # 模式五：城郊消费型
    # 城镇化率 ≥70%，GDP ≥10000000万元，农村人均收入 ≥40000元，新增就业 ≥20000人
    if urban_rate >= 70 and gdp >= 10000000 and rural_income >= 40000 and new_jobs >= 20000:
        return "城郊消费型", f"城镇化率 {urban_rate}%（≥70%），GDP {gdp}万元，农村人均收入 {rural_income}元，符合城郊消费型特征"

    # 模式三：农业品牌型
    # 粮食播种面积 ≥100000公顷，农产品产出 ≥900000吨
    if grain_area >= 100000 and agri_output >= 900000:
        return "农业品牌型", f"粮食播种面积 {grain_area} 公顷（≥100000），农产品产出 {agri_output} 吨（≥900000），符合农业品牌型特征"

    # 模式四：农文旅融合型（默认）
    # 森林覆盖率 ≥15%，空气优良率 ≥80%，水质达标率 ≥90%
    if forest >= 15 and air_quality >= 80:
        return "农文旅融合型", f"森林覆盖率 {forest}%，空气优良率 {air_quality}%，各项指标均衡发展，符合农文旅融合型特征"

    # 兜底
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

五种模式识别规则（基于层次聚类分析结果）：
1. 生态康养型：森林覆盖率≥65%，城镇化率≤55%，空气优良率≥80%（代表区县：黟县、蒲江县）
2. 湿地水域型：水质达标率≥95%，重要生态功能保护区面积大（代表区县：淳安县）
3. 农业品牌型：粮食播种面积≥100000公顷，农产品产出≥900000吨（代表区县：兴化市、盱眙县、大丰区）
4. 农文旅融合型：森林覆盖率≥15%，空气优良率≥80%，水质达标率≥90%（代表区县：安吉县、溧阳市、高淳区）
5. 城郊消费型：城镇化率≥70%，GDP≥10000000万元，农村人均收入≥40000元（代表区县：吴中区）

地区：{region}
生态产品价值实现成效得分：{eco_score}/100
乡村振兴水平得分：{rural_score}/100
耦合协调度D值：{d}
主要障碍因子：{obstacles}
原始指标摘要：森林覆盖率={raw.get('森林覆盖率（%）', 'N/A')}%，水质达标率={raw.get('主要水体水质断面达标率（%）', 'N/A')}%，城镇化率={raw.get('常住人口城镇化率（%）', 'N/A')}%，GDP={raw.get('地区生产总值（万元）', 'N/A')}万元，粮食播种面积={raw.get('全区粮食播种面积（公顷）', 'N/A')}公顷

请输出格式：
【模式判定】：xxx型
【判定依据】：xxx（150字内，需引用具体指标数据）
【路径优化建议】：
（500-800字，针对障碍度最高的2-3个维度提出具体可操作建议，需结合该模式的典型做法）
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
