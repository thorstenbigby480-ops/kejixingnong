"""独立测试 DeepSeek API 调用"""
import asyncio
import sys
sys.path.insert(0, ".")
from app.core.ai_advisor import recognize_mode_and_advise

raw = {
    "森林覆盖率（%）": 55,
    "主要水体水质断面达标率（%）": 95,
    "空气环境质量优良率（%）": 90,
    "重要生态功能保护区面积（公顷）": 12000,
    "地区生产总值（万元）": 300000,
    "农林牧渔业总产值（万元）": 80000,
    "粮食总产量（吨）": 20000,
    "新增就业人数（人）": 2000,
    "农村居民人均可支配收入（元）": 32000,
    "粮食播种面积（公顷）": 8000,
    "农产品产出（吨）": 25000,
    "常住人口城镇化率（%）": 65,
}


async def main():
    print("调用 DeepSeek 中...（约 10-30 秒）")
    mode, reason, advice = await recognize_mode_and_advise(
        region_name="江苏省南京市溧水区石湫镇",
        eco_score=53.22,
        rural_score=54.25,
        coupling_d=0.733,
        obstacles={"重要生态功能保护区面积（公顷）": 0.114, "粮食播种面积（公顷）": 0.084},
        raw_data=raw,
    )
    print(f"\n【模式判定】{mode}")
    print(f"【判定依据】{reason}")
    print(f"\n【AI 建议】\n{advice}")
    print(f"\n建议字数: {len(advice)}")


if __name__ == "__main__":
    asyncio.run(main())
