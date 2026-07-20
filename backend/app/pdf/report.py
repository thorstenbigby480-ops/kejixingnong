"""PDF 报告生成 —— reportlab"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def _register_font() -> str:
    """注册中文字体"""
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simsun.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont("CN", p))
                return "CN"
            except Exception:
                continue
    return "Helvetica"


def generate_report(record, output_path: str) -> str:
    font = _register_font()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Title"], fontName=font, fontSize=20, leading=28)
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName=font, fontSize=14, leading=20,
                        spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#1b5e20"))
    body = ParagraphStyle("body", parent=styles["BodyText"], fontName=font, fontSize=11, leading=18)

    elems = []
    elems.append(Paragraph("生态产品价值实现赋能乡村振兴评估报告", h1))
    elems.append(Spacer(1, 0.5 * cm))
    elems.append(Paragraph(f"评估地区：<b>{record.region_name}</b>    年份：{record.year or '未填'}", body))
    elems.append(Spacer(1, 0.3 * cm))

    elems.append(Paragraph("一、综合得分", h2))
    score_data = [
        ["指标", "得分"],
        ["生态产品价值实现成效", f"{record.eco_score} / 100"],
        ["乡村振兴水平", f"{record.rural_score} / 100"],
        ["耦合协调度 D 值", f"{record.coupling_d}（{record.coordination_level}）"],
    ]
    t = Table(score_data, colWidths=[8 * cm, 8 * cm])
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), font, 11),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b5e20")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f8e9")]),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.3 * cm))

    elems.append(Paragraph("二、模式判定", h2))
    elems.append(Paragraph(f"判定模式：<b>{record.mode_type}</b>", body))
    elems.append(Paragraph(f"判定依据：{record.mode_reason}", body))
    elems.append(Spacer(1, 0.3 * cm))

    elems.append(Paragraph("三、路径优化建议", h2))
    advice_text = (record.advice or "暂无建议").replace("\n", "<br/>")
    elems.append(Paragraph(advice_text, body))

    doc.build(elems)
    return output_path
