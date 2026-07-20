"""端到端测试智能分析流程"""
import json
import requests

URL = "http://127.0.0.1:8000"

# 1. 检查根接口
print("=== 1. 根接口 ===")
r = requests.get(f"{URL}/")
print(r.json())

# 2. 拿模板
print("\n=== 2. 数据模板 ===")
tpl = requests.get(f"{URL}/api/analysis/template").json()
print(f"生态指标 {len(tpl['eco_indicators'])} 个，乡村振兴指标 {len(tpl['rural_indicators'])} 个")

# 3. 调用评估（模拟溧水石湫镇）
print("\n=== 3. 提交评估 ===")
data = {
    "森林覆盖率（%）": 55, "主要水体水质断面达标率（%）": 95,
    "空气环境质量优良率（%）": 90, "重要生态功能保护区面积（公顷）": 12000,
    "地区生产总值（万元）": 300000, "农林牧渔业总产值（万元）": 80000,
    "粮食总产量（吨）": 20000, "新增就业人数（人）": 2000,
    "农村居民人均可支配收入（元）": 32000,
    "粮食播种面积（公顷）": 8000, "农产品产出（吨）": 25000,
    "农业机械总动力/农作物播种面积（千瓦/亩）": 3.5,
    "污水处理厂集中处理率（%）": 85, "农村卫生厕所普及率（%）": 95,
    "普通中学专任教师数/在校学生数（%）": 8, "图书馆个数（个）": 12,
    "一般公共服务支出（万元）": 8000, "农林水事务支出占比（%）": 18,
    "卫生机构数量（个）": 20, "三种专利申请授权量（件）": 80,
    "常住人口城镇化率（%）": 65, "城乡低保标准（元/月）": 1000,
    "农村人均可支配收入（元）": 32000, "农村人均消费支出（元）": 22000,
    "人均道路面积（平方米）": 15, "固定互联网宽带接入用户（户）": 3000,
}
files = {
    "region_name": (None, "江苏省南京市溧水区石湫镇"),
    "year": (None, "2024"),
    "data": (None, json.dumps(data, ensure_ascii=False)),
}
r = requests.post(f"{URL}/api/analysis/assess", files=files)
print(f"HTTP {r.status_code}")
result = r.json()
print(f"地区: {result['region_name']} ({result['year']})")
print(f"生态得分: {result['eco_score']}/100")
print(f"乡村振兴得分: {result['rural_score']}/100")
print(f"耦合协调度 D: {result['coupling_d']} ({result['coordination_level']})")
print(f"判定模式: {result['mode_type']}")
print(f"判定依据: {result['mode_reason']}")
print(f"\n障碍因子 Top 5:")
for k, v in list(result["obstacles"].items())[:5]:
    print(f"  - {k}: {v}")
print(f"\nAI 建议（前 300 字）:")
print(result["advice"][:300])

# 4. 生成 PDF 报告
print("\n=== 4. 生成 PDF 报告 ===")
r = requests.get(f"{URL}/api/analysis/{result['id']}/report")
print(f"HTTP {r.status_code}: {r.json()}")

# 5. 查询评估历史
print("\n=== 5. 评估历史 ===")
hist = requests.get(f"{URL}/api/analysis/history").json()
print(f"共 {hist['total']} 条记录")

print("\n✅ 全流程跑通！")
