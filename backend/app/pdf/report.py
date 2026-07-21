"""PDF 报告生成 —— reportlab + matplotlib（嵌入雷达图与障碍图）"""
import os
import io
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
    PageBreak, KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import matplotlib
matplotlib.use("Agg")  # 无 GUI 后端
import matplotlib.pyplot as plt
from matplotlib import font_manager


# ============ 字体注册 ============
def _register_cn_font() -> str:
    """注册中文字体（reportlab 用）"""
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simsun.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont("CN", p))
                # matplotlib 也要能显示中文
                font_manager.fontManager.addfont(p)
                prop = font_manager.FontProperties(fname=p)
                plt.rcParams["font.family"] = prop.get_name()
                plt.rcParams["axes.unicode_minus"] = False
                return "CN"
            except Exception:
                continue
    return "Helvetica"


# ============ 图表绘制 ============
def _draw_radar_chart(eco_dims: dict, rural_dims: dict) -> str:
    """绘制雷达图（生态得分 vs 振兴得分 各维度对比）"""
    labels = list(eco_dims.keys()) + list(rural_dims.keys())
    eco_values = list(eco_dims.values()) + [0] * len(rural_dims)
    rural_values = [0] * len(eco_dims) + list(rural_dims.values())

    n = len(labels)
    angles = [i / n * 2 * 3.14159265 for i in range(n)]

    fig = plt.figure(figsize=(7, 5), dpi=120)
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles + angles[:1], eco_values + eco_values[:1], "o-", linewidth=2,
            color="#1b5e20", label="生态产品价值实现")
    ax.fill(angles + angles[:1], eco_values + eco_values[:1], alpha=0.2, color="#1b5e20")
    ax.plot(angles + angles[:1], rural_values + rural_values[:1], "o-", linewidth=2,
            color="#c79a00", label="乡村振兴")
    ax.fill(angles + angles[:1], rural_values + rural_values[:1], alpha=0.2, color="#c79a00")

    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=9)
    plt.title("各维度得分雷达图", fontsize=13, pad=20)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf


def _draw_obstacle_chart(obstacles: dict) -> str:
    """绘制障碍度条形图（取前10项）"""
    if not obstacles:
        return None
    # 按值降序，取前10
    items = sorted(obstacles.items(), key=lambda x: x[1], reverse=True)[:10]
    names = [k[:15] + "…" if len(k) > 15 else k for k, _ in items]
    values = [float(v) for _, v in items]

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=120)
    bars = ax.barh(names, values, color=["#c00" if v > 15 else "#c79a00" for v in values])
    ax.set_xlabel("障碍度 (%)", fontsize=11)
    ax.set_title("主要障碍因子 Top10", fontsize=13, pad=12)
    ax.invert_yaxis()
    # 在条形末端标注数值
    for bar, v in zip(bars, values):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{v:.1f}%", va="center", fontsize=9)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf


# ============ 主报告生成 ============
def generate_report(record, output_path: str) -> str:
    font = _register_cn_font()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm,
        title=f"绿脉兴农评估报告-{record.region_name}",
    )
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Title"], fontName=font, fontSize=20, leading=28,
                         textColor=colors.HexColor("#1b5e20"))
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName=font, fontSize=14, leading=20,
                        spaceBefore=12, spaceAfter=6, textColor=colors.HexColor("#1b5e20"))
    h3 = ParagraphStyle("h3", parent=styles["Heading3"], fontName=font, fontSize=12, leading=18,
                        spaceBefore=6, spaceAfter=4, textColor=colors.HexColor("#8b1e3f"))
    body = ParagraphStyle("body", parent=styles["BodyText"], fontName=font, fontSize=11, leading=18)
    small = ParagraphStyle("small", parent=styles["BodyText"], fontName=font, fontSize=9,
                           leading=12, textColor=colors.grey)

    elems = []

    # ============ 封面 / 标题区 ============
    elems.append(Paragraph("生态产品价值实现赋能乡村振兴", h1))
    elems.append(Paragraph("评 估 报 告", h1))
    elems.append(Spacer(1, 0.5 * cm))

    # 报告元信息
    meta_data = [
        ["评估地区", record.region_name or "—"],
        ["评估年份", str(record.year) if record.year else "—"],
        ["报告编号", f"GP-{record.id:06d}"],
        ["生成时间", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    ]
    meta_t = Table(meta_data, colWidths=[3.5 * cm, 12 * cm])
    meta_t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), font, 10),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1f8e9")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1b5e20")),
        ("FONTNAME", (0, 0), (0, -1), font),
        ("BOLD", (0, 0), (0, -1), True),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#c8e6c9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(meta_t)
    elems.append(Spacer(1, 0.4 * cm))

    # ============ 一、综合得分 ============
    elems.append(Paragraph("一、综合评估结果", h2))
    score_data = [
        ["指标", "得分", "等级"],
        ["生态产品价值实现成效", f"{record.eco_score:.2f} / 100", _grade(record.eco_score)],
        ["乡村振兴水平", f"{record.rural_score:.2f} / 100", _grade(record.rural_score)],
        ["耦合协调度 D 值", f"{record.coupling_d:.4f}", record.coordination_level or "—"],
    ]
    t = Table(score_data, colWidths=[8 * cm, 4 * cm, 3.5 * cm])
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), font, 11),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b5e20")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f8e9")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.3 * cm))

    # ============ 二、各维度得分雷达图 ============
    elems.append(PageBreak())
    elems.append(Paragraph("二、各维度得分雷达图", h2))

    # 从 raw_data 中提取维度得分（如果没存维度分，就跳过）
    eco_dims = {}
    rural_dims = {}
    # raw_data 在数据库里存的是原始指标值，维度分需要重新计算
    # 这里直接展示原始关键指标
    if record.raw_data:
        try:
            raw = record.raw_data if isinstance(record.raw_data, dict) else json.loads(record.raw_data)
            # 关键生态指标
            eco_keys = [
                "森林覆盖率（%）", "空气环境质量优良率（%）", "主要水体水质断面达标率（%）",
                "地区生产总值（万元）", "全区粮食播种面积（公顷）", "农产品产出（吨）",
            ]
            # 关键振兴指标
            rural_keys = [
                "粮食总产量（吨）", "农林牧渔业总产值（万元）", "农村人均可支配收入（元）",
                "三种专利申请授权量（件）", "农村人均消费支出（元）", "人均道路面积（平方米）",
            ]
            # 简单归一化展示（用项目数据范围）
            ranges = {
                "森林覆盖率（%）": (0, 80), "空气环境质量优良率（%）": (0, 100),
                "主要水体水质断面达标率（%）": (0, 100), "地区生产总值（万元）": (0, 30000000),
                "全区粮食播种面积（公顷）": (0, 200000), "农产品产出（吨）": (0, 1500000),
                "粮食总产量（吨）": (0, 1000000), "农林牧渔业总产值（万元）": (0, 2000000),
                "农村人均可支配收入（元）": (0, 60000), "三种专利申请授权量（件）": (0, 20000),
                "农村人均消费支出（元）": (0, 40000), "人均道路面积（平方米）": (0, 30),
            }
            for k in eco_keys:
                if k in raw and k in ranges:
                    lo, hi = ranges[k]
                    v = (float(raw[k]) - lo) / (hi - lo) * 100 if hi > lo else 0
                    eco_dims[k.replace("（%）", "").replace("（万元）", "").replace("（公顷）", "").replace("（吨）", "")[:10]] = max(0, min(100, v))
            for k in rural_keys:
                if k in raw and k in ranges:
                    lo, hi = ranges[k]
                    v = (float(raw[k]) - lo) / (hi - lo) * 100 if hi > lo else 0
                    rural_dims[k.replace("（万元）", "").replace("（吨）", "").replace("（元）", "").replace("（平方米）", "").replace("（件）", "")[:10]] = max(0, min(100, v))
        except Exception:
            pass

    if eco_dims or rural_dims:
        try:
            buf = _draw_radar_chart(eco_dims, rural_dims)
            elems.append(Image(buf, width=15 * cm, height=10 * cm))
            elems.append(Spacer(1, 0.2 * cm))
            elems.append(Paragraph("注：雷达图展示各项关键指标的归一化得分（0-100）。绿色为生态产品价值实现维度，金色为乡村振兴维度。", small))
        except Exception as e:
            elems.append(Paragraph(f"（雷达图生成失败：{e}）", small))
    else:
        elems.append(Paragraph("（评估数据不足，无法生成雷达图）", body))

    elems.append(Spacer(1, 0.4 * cm))

    # ============ 三、障碍度分析 ============
    elems.append(Paragraph("三、主要障碍因子分析", h2))
    if record.obstacles:
        try:
            obs = record.obstacles if isinstance(record.obstacles, dict) else json.loads(record.obstacles)
            buf = _draw_obstacle_chart(obs)
            if buf:
                elems.append(Image(buf, width=16 * cm, height=9 * cm))
                elems.append(Spacer(1, 0.2 * cm))
                elems.append(Paragraph("注：红色条目障碍度大于15%，表示该指标是该地区发展的主要瓶颈；金色条目为次要障碍。", small))
        except Exception as e:
            elems.append(Paragraph(f"（障碍图生成失败：{e}）", small))
    else:
        elems.append(Paragraph("（无障碍度数据）", body))

    elems.append(PageBreak())

    # ============ 四、模式判定 ============
    elems.append(Paragraph("四、模式判定", h2))
    elems.append(Paragraph(f"<b>判定模式：{record.mode_type}</b>", h3))
    elems.append(Paragraph(f"判定依据：{record.mode_reason or '—'}", body))
    elems.append(Spacer(1, 0.3 * cm))

    # ============ 五、路径优化建议 ============
    elems.append(Paragraph("五、路径优化建议", h2))
    advice_text = (record.advice or "暂无建议").replace("\n", "<br/>")
    elems.append(Paragraph(advice_text, body))

    # ============ 页脚 ============
    elems.append(Spacer(1, 1 * cm))
    elems.append(Paragraph("=" * 70, small))
    elems.append(Paragraph("绿脉兴农 · 生态产品价值实现赋能乡村振兴一体化智能系统", small))
    elems.append(Paragraph("本报告由系统基于耦合协调度模型与AI路径优化算法自动生成，仅供参考。", small))

    doc.build(elems)
    return output_path


def _grade(score: float) -> str:
    """根据得分评定等级"""
    if score is None:
        return "—"
    if score >= 80:
        return "优秀"
    elif score >= 70:
        return "良好"
    elif score >= 60:
        return "中等"
    elif score >= 40:
        return "较弱"
    else:
        return "较差"
