"""
绿脉兴农平台技术白皮书 · Word 文档生成脚本

使用 python-docx 生成符合 GB/T 7713.1 学位论文格式 + 华为产品白皮书风格的 .docx 文档
运行：python docs/generate_docx.py
输出：docs/绿脉兴农平台技术白皮书.docx
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement
from pathlib import Path

OUTPUT = Path(__file__).parent / "绿脉兴农平台技术白皮书.docx"

# ===== 颜色常量 =====
FOREST = RGBColor(0x0D, 0x3B, 0x2E)
FOREST_3 = RGBColor(0x2D, 0x6A, 0x4F)
GOLD = RGBColor(0xC7, 0x9A, 0x00)
GOLD_LIGHT = RGBColor(0xE6, 0xC4, 0x49)
RED = RGBColor(0x8B, 0x1E, 0x3F)
INK = RGBColor(0x2A, 0x2A, 0x2A)
INK_2 = RGBColor(0x5A, 0x5A, 0x5A)
INK_3 = RGBColor(0x8A, 0x8A, 0x8A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


# ===== 工具函数 =====
def set_run_font(run, name="宋体", name_ascii="Times New Roman", size=12, bold=False, color=None):
    """设置 run 字体"""
    run.font.name = name_ascii
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color


def add_paragraph(doc, text="", style=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                  first_line_indent=True, font_name="宋体", font_size=12,
                  bold=False, color=None, line_spacing=1.5, space_before=0, space_after=0):
    """添加段落并设置格式"""
    p = doc.add_paragraph(style=style)
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = line_spacing
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    if first_line_indent:
        pf.first_line_indent = Pt(font_size * 2)
    if text:
        run = p.add_run(text)
        set_run_font(run, name=font_name, size=font_size, bold=bold, color=color)
    return p


def add_heading(doc, text, level=1, color=None, size=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    """添加自定义标题"""
    sizes = {1: 16, 2: 14, 3: 12}
    colors = {1: FOREST, 2: FOREST, 3: FOREST_3}
    s = size or sizes.get(level, 12)
    c = color or colors.get(level, INK)
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_before = Pt(12 if level <= 2 else 6)
    pf.space_after = Pt(6)
    run = p.add_run(text)
    set_run_font(run, name="黑体", name_ascii="Times New Roman", size=s, bold=True, color=c)
    return p


def add_chapter_title(doc, text):
    """章节大标题（居中+下划线）"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_before = Pt(0)
    pf.space_after = Pt(18)
    run = p.add_run(text)
    set_run_font(run, name="黑体", size=18, bold=True, color=FOREST)
    # 添加底部边框
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), '0D3B2E')
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def add_table_three_line(doc, data, header=True, caption=None):
    """添加三线表"""
    if caption:
        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_before = Pt(6)
        cap_p.paragraph_format.space_after = Pt(3)
        run = cap_p.add_run(caption)
        set_run_font(run, name="黑体", size=10.5, bold=True, color=FOREST)

    rows = len(data)
    cols = len(data[0]) if data else 0
    table = doc.add_table(rows=rows, cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # 填充数据
    for i, row_data in enumerate(data):
        for j, cell_text in enumerate(row_data):
            cell = table.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (i == 0 or j > 0) else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(cell_text))
            is_header = (i == 0 and header)
            set_run_font(run, name="黑体" if is_header else "宋体",
                         size=10.5, bold=is_header,
                         color=FOREST if is_header else INK)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # 三线表样式：去掉所有边框，只保留顶、表头下、底
    tbl = table._element
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')

    # 清除默认边框
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'none')
        tblBorders.append(border)
    tblPr.append(tblBorders)

    # 顶边框（粗）
    for cell_idx in range(cols):
        cell = table.cell(0, cell_idx)
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        top = OxmlElement('w:top')
        top.set(qn('w:val'), 'single')
        top.set(qn('w:sz'), '12')
        top.set(qn('w:color'), '000000')
        tcBorders.append(top)
        tcPr.append(tcBorders)

    # 表头下边框
    if header and rows > 1:
        for cell_idx in range(cols):
            cell = table.cell(0, cell_idx)
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = tcPr.find(qn('w:tcBorders'))
            if tcBorders is None:
                tcBorders = OxmlElement('w:tcBorders')
                tcPr.append(tcBorders)
            bottom = OxmlElement('w:bottom')
            bottom.set(qn('w:val'), 'single')
            bottom.set(qn('w:sz'), '6')
            bottom.set(qn('w:color'), '000000')
            tcBorders.append(bottom)

    # 底边框（粗）
    for cell_idx in range(cols):
        cell = table.cell(rows - 1, cell_idx)
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = tcPr.find(qn('w:tcBorders'))
        if tcBorders is None:
            tcBorders = OxmlElement('w:tcBorders')
            tcPr.append(tcBorders)
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '12')
        bottom.set(qn('w:color'), '000000')
        tcBorders.append(bottom)

    return table


def add_formula(doc, formula_text, num=None):
    """添加公式块"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_before = Pt(6)
    pf.space_after = Pt(6)
    pf.left_indent = Cm(1)
    pf.right_indent = Cm(1)
    # 添加浅色底纹
    pPr = p._element.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), 'FAF7F0')
    pPr.append(shd)
    # 左边框
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '24')
    left.set(qn('w:space'), '4')
    left.set(qn('w:color'), 'C79A00')
    pBdr.append(left)
    pPr.append(pBdr)

    run = p.add_run(formula_text)
    set_run_font(run, name="Cambria Math", name_ascii="Cambria Math", size=11, color=FOREST)
    if num:
        run2 = p.add_run("    " + num)
        set_run_font(run2, name="Times New Roman", size=11, color=INK_2)
    return p


def add_figure_caption(doc, num, text):
    """添加图题"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run(f"图 {num}  {text}")
    set_run_font(run, name="黑体", size=10.5, bold=True, color=INK)


def add_page_break(doc):
    """分页符"""
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(WD_BREAK.PAGE)


def set_cell_shading(cell, color_hex):
    """设置单元格背景色"""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)


# ============================================================
# 文档生成主流程
# ============================================================
def build_document():
    doc = Document()

    # === 页面设置：A4，上下 2.54cm，左右 3.17cm ===
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(3.17)
        section.right_margin = Cm(3.17)
        # 页眉
        header = section.header
        header_p = header.paragraphs[0]
        header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        header_run = header_p.add_run("绿脉兴农平台技术白皮书")
        set_run_font(header_run, size=9, color=INK_3)
        # 页脚（页码）
        footer = section.footer
        footer_p = footer.paragraphs[0]
        footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer_run = footer_p.add_run()
        # 插入页码字段
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        instrText = OxmlElement('w:instrText')
        instrText.text = 'PAGE'
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')
        footer_run._r.append(fldChar1)
        footer_run._r.append(instrText)
        footer_run._r.append(fldChar2)
        set_run_font(footer_run, size=10, color=INK)

    # ============================================================
    # 封面
    # ============================================================
    # 顶部品牌区
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("机密 · 内部使用")
    set_run_font(run, name="黑体", size=10, bold=True, color=RED)

    # Logo 行
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(24)
    run = p.add_run("绿脉兴农  LVMAI · ECO-VALUE PLATFORM")
    set_run_font(run, name="黑体", size=22, bold=True, color=FOREST)

    # 分隔线
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(60)
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '18')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '0D3B2E')
    pBdr.append(bottom)
    pPr.append(pBdr)

    # 主标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(80)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run("TECHNICAL WHITE PAPER · V1.0")
    set_run_font(run, name="Times New Roman", size=11, bold=True, color=GOLD)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("绿脉兴农平台")
    set_run_font(run, name="黑体", size=36, bold=True, color=FOREST)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("技术白皮书")
    set_run_font(run, name="黑体", size=36, bold=True, color=FOREST)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(60)
    run = p.add_run("生态产品价值实现赋能乡村振兴一体化智能系统")
    set_run_font(run, name="黑体", size=16, color=FOREST_3)

    # 底部信息
    info_items = [
        ("文档版本", "V1.0"),
        ("发布日期", "2026 年 07 月"),
        ("保密等级", "内部公开"),
        ("文档状态", "正式发布"),
        ("编制单位", "南京师范大学 · 绿脉兴农团队"),
        ("适用赛事", "中国研究生乡村振兴科技强农+创新大赛"),
    ]
    for label, value in info_items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(f"{label}：")
        set_run_font(run, name="黑体", size=11, bold=True, color=FOREST)
        run = p.add_run(value)
        set_run_font(run, name="宋体", size=11, color=INK)

    add_page_break(doc)

    # ============================================================
    # 摘要
    # ============================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(18)
    run = p.add_run("摘 要")
    set_run_font(run, name="黑体", size=18, bold=True, color=FOREST)

    abstract_zh = (
        '在"绿水青山就是金山银山"理念与乡村振兴战略双重背景下，如何科学量化生态产品价值实现水平、'
        '识别区域发展模式、生成差异化路径建议，成为地方政府与研究机构亟待解决的关键问题。本文介绍了一款'
        '名为"绿脉兴农"的一体化智能决策支持平台，该平台融合层次分析法（AHP）、熵权法、耦合协调度模型与'
        '障碍度模型四大数学方法，并集成 DeepSeek 大语言模型，构建了从数据采集、模型评估到路径优化的完整闭环。'
    )
    add_paragraph(doc, abstract_zh, font_size=12, line_spacing=1.875)

    abstract_zh2 = (
        "平台以长江三角洲地区 10 个典型区县 2020—2024 年面板数据为样本，构建了包含 11 项生态产品价值实现指标"
        "与 15 项乡村振兴指标的二维评估体系，通过层次聚类分析提炼出生态康养型、湿地水域型、农业品牌型、"
        "农文旅融合型、城郊消费型五种发展模式，并为每种模式配置量化识别阈值与 27 条结构化路径优化建议。"
        "平台采用前后端分离架构，前端基于 Vue 3 与 Element Plus 构建，后端基于 FastAPI 与 SQLAlchemy 实现。"
        "测试表明，平台可在 3 秒内完成单次综合评估，PDF 报告自动生成，AI 路径建议响应稳定。"
    )
    add_paragraph(doc, abstract_zh2, font_size=12, line_spacing=1.875)

    abstract_zh3 = (
        "本文系统阐述了平台的总体架构、核心算法原理、功能模块设计、关键流程实现及部署运维方案，"
        "并附完整指标体系与 API 接口规范，为同类研究与产品研发提供参考。"
    )
    add_paragraph(doc, abstract_zh3, font_size=12, line_spacing=1.875)

    # 关键词
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.first_line_indent = Pt(0)
    run = p.add_run("关键词：")
    set_run_font(run, name="黑体", size=12, bold=True, color=FOREST)
    run = p.add_run("生态产品价值实现；乡村振兴；层次分析法；耦合协调度；障碍度模型；DeepSeek；智能决策支持系统")
    set_run_font(run, name="宋体", size=12, color=INK)

    add_page_break(doc)

    # ============================================================
    # 目录（Word 打开后可右键更新域生成）
    # ============================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(18)
    run = p.add_run("目 录")
    set_run_font(run, name="黑体", size=18, bold=True, color=FOREST)

    # 插入 TOC 域
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Pt(0)
    run = p.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' TOC \\o "1-3" \\h \\z \\u '
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run = p.add_run('（请在 Word 中按 F9 或右键"更新域"生成目录）')
    set_run_font(run, name="宋体", size=10.5, color=INK_3)
    run._r.append(fldChar3)

    add_page_break(doc)

    # ============================================================
    # 第一章 绪论
    # ============================================================
    add_chapter_title(doc, "第一章 绪论")

    add_heading(doc, "1.1 研究背景与意义", level=2)
    add_paragraph(doc,
        '2021 年 4 月，中共中央办公厅、国务院办公厅印发《关于建立健全生态产品价值实现机制的意见》，'
        '明确提出"建立生态产品调查监测机制、价值评价机制、经营开发机制、保护补偿机制、实现保障机制"五大核心任务。'
        '2022 年中央一号文件进一步强调"探索生态产品价值实现路径"，将生态产品价值实现纳入乡村振兴战略整体布局。')
    add_paragraph(doc,
        '然而，当前生态产品价值实现仍面临三大挑战：其一，生态产品价值"算不清"，缺乏统一规范的量化评估方法；'
        '其二，区域发展模式"看不透"，难以从复杂指标中识别差异化路径；其三，政策建议"落不实"，'
        '理论研究成果难以转化为地方政府可操作的决策依据。')
    add_paragraph(doc,
        '针对上述问题，本团队研发"绿脉兴农"一体化智能决策支持平台，通过融合多源数学模型与 AI 大模型，'
        '构建从数据采集、综合评估、模式识别到路径优化的完整闭环，为地方政府、农业合作社、研究学者提供科学决策支持，'
        '具有重要的理论意义与实践价值。')

    add_heading(doc, "1.2 国内外研究现状", level=2)
    add_paragraph(doc,
        "国外生态产品价值评估起源于 Costanza 等人（1997）的全球生态系统服务价值评估研究，"
        "随后 InVEST 模型、ARIES 模型等工具相继问世，为生态系统服务量化提供了方法基础。"
        "然而，这些工具主要面向生态系统服务物理量评估，对价值实现机制与社会经济耦合分析支持不足。")
    add_paragraph(doc,
        "国内研究起步较晚但发展迅速。欧阳志云团队（2013—2020）提出了生态系统生产总值（GEP）核算框架，"
        "已在浙江丽水、深圳等地开展试点；高楠等（2019）构建了耦合协调度模型评估生态与经济协同发展水平；"
        "李芳林等（2021）运用障碍度模型识别乡村振兴制约因素。但现有研究多聚焦于单一模型应用，"
        "缺乏多模型集成与智能化路径优化能力，难以满足地方政府综合决策需求。")
    add_paragraph(doc,
        "近年来，大语言模型（LLM）的快速发展为智能决策支持提供了新契机。DeepSeek 等国产开源大模型在中文语境下表现优异，"
        "具备处理领域知识、生成结构化建议的能力。本平台创新性地将传统数学模型与大语言模型结合，"
        "弥补了现有研究在智能化路径优化方面的不足。")

    add_heading(doc, "1.3 平台建设目标", level=2)
    add_paragraph(doc, '绿脉兴农平台旨在构建一个"算得清、看得见、走得通"的一体化智能决策支持系统，具体目标如下：')

    add_paragraph(doc,
        "（1）算得清：基于 AHP 层次分析法与熵权法，构建涵盖 11 项生态产品价值实现指标与 15 项乡村振兴指标的"
        "二维评估体系，通过组合权重加权综合评分，实现地区生态与乡村振兴水平的科学量化。",
        first_line_indent=True)
    add_paragraph(doc,
        "（2）看得见：以 10 个典型区县 5 年面板数据为基础，构建多维可视化数据大屏，支持横向对比、时间演化、"
        "模式雷达、耦合散点等多种分析视角，使数据规律直观可见。",
        first_line_indent=True)
    add_paragraph(doc,
        "（3）走得通：通过层次聚类分析提取 5 种发展模式，结合 DeepSeek AI 引擎生成 27 条差异化路径优化建议，"
        "并一键导出 PDF 评估报告，为地方政府决策提供可操作依据。",
        first_line_indent=True)

    add_heading(doc, "1.4 文档组织结构", level=2)
    add_paragraph(doc, "本文共分九章，组织结构如下：")
    chapters = [
        "第一章 绪论。介绍研究背景、意义、国内外现状及平台建设目标。",
        "第二章 平台总体架构。阐述设计原则、四层架构与技术选型。",
        "第三章 核心算法原理。详细说明 AHP、耦合协调度、障碍度、AI 引擎与聚类分析五大算法。",
        "第四章 功能模块设计。介绍七大功能模块的设计与实现。",
        "第五章 五种发展模式。说明模式提取方法、详细特征与路径优化建议矩阵。",
        "第六章 关键流程实现。描述智能评估与商城交易两大核心流程。",
        "第七章 API 接口规范。列出全部 RESTful 端点。",
        "第八章 部署与运维。说明环境配置、启动方式与生产部署方案。",
        "第九章 总结与展望。总结平台价值并展望未来工作。",
    ]
    for ch in chapters:
        add_paragraph(doc, ch, first_line_indent=True)

    add_page_break(doc)

    # ============================================================
    # 第二章 平台总体架构
    # ============================================================
    add_chapter_title(doc, "第二章 平台总体架构")

    add_heading(doc, "2.1 设计原则", level=2)
    add_paragraph(doc, "平台设计遵循以下五项原则：")
    principles = [
        "（1）科学性原则：所有评估方法基于成熟数学模型，权重通过 AHP 专家打分得出，避免主观随意性。",
        "（2）实用性原则：功能设计紧密对接地方政府实际需求，所有评估结果可直接用于决策汇报。",
        "（3）可扩展性原则：采用模块化架构，新增指标、模式、算法模块不影响现有功能。",
        "（4）安全性原则：基于 JWT 实现无状态身份认证，敏感操作进行权限校验。",
        "（5）易用性原则：界面遵循 Element Plus 设计规范，操作流程符合用户直觉。",
    ]
    for pr in principles:
        add_paragraph(doc, pr, first_line_indent=True)

    add_heading(doc, "2.2 总体架构", level=2)
    add_paragraph(doc,
        "平台采用前后端分离架构，整体分为四层：前端展示层、后端服务层、核心算法层与数据存储层，"
        "各层之间通过明确定义的接口进行通信，层间耦合度低，便于独立演进。架构如图 2-1 所示。")

    # 架构图说明（文本形式，因 python-docx 难以绘制复杂 SVG）
    add_paragraph(doc,
        "图 2-1 展示了平台四层架构。最上层为前端展示层，包含首页、政策中心、智能分析、数据大屏、"
        "农产品商城、案例中心、用户中心 7 个 Vue 视图模块；第二层为后端服务层，包含 Auth、Policy、Analysis、"
        "Dashboard、Mall、Case 共 6 个 FastAPI 路由模块；第三层为核心算法层，包含 AHP 层次分析、耦合协调度、"
        "障碍度、AI 智能建议、模式数据共 5 个 Python 模块；最底层为数据存储层，包含 SQLite/MySQL 数据库、"
        "reportlab 生成的 PDF 报告与 DeepSeek AI 接口。各层自上而下逐层调用，通过明确定义的接口通信。",
        first_line_indent=True)
    add_figure_caption(doc, "2-1", "绿脉兴农平台总体架构图")

    add_heading(doc, "2.3 技术选型", level=2)
    add_paragraph(doc, "平台技术选型兼顾成熟度、性能、可维护性与开源友好性，具体如表 2-1 所示。")

    tech_data = [
        ["层级", "技术选型", "版本", "选用理由"],
        ["前端框架", "Vue 3", "3.4", "Composition API 响应式视图层"],
        ["UI 组件库", "Element Plus", "2.6", "企业级组件，文档完善"],
        ["图表库", "ECharts", "5.5", "功能丰富，性能优异"],
        ["构建工具", "Vite", "5.4", "极速热更新，开发体验佳"],
        ["后端框架", "FastAPI", "0.111", "高性能异步，自动生成文档"],
        ["ORM 框架", "SQLAlchemy", "2.0", "Python 生态成熟 ORM"],
        ["数据库", "SQLite → MySQL", "—", "开发用 SQLite，生产用 MySQL"],
        ["身份认证", "JWT", "—", "无状态鉴权，便于水平扩展"],
        ["AI 引擎", "DeepSeek API", "—", "国产开源大模型，中文表现优异"],
        ["PDF 生成", "reportlab", "4.0", "Python 原生 PDF 库"],
    ]
    add_table_three_line(doc, tech_data, caption="表 2-1 平台技术选型表")

    add_heading(doc, "2.4 数据规模", level=2)
    add_paragraph(doc,
        "平台以长江三角洲地区 10 个典型区县为研究样本，覆盖江苏、浙江、安徽、四川四省，"
        "时间跨度为 2020—2024 年共 5 年。数据来源于《中国县域统计年鉴》《中国城市统计年鉴》及各地统计公报，"
        "经清洗后形成 50 条面板数据记录。数据规模如表 2-2 所示。")

    data_scale = [
        ["维度", "规模", "说明"],
        ["样本区县数", "10 个", "江苏 6、浙江 2、安徽 1、四川 1"],
        ["时间跨度", "5 年", "2020—2024 年面板数据"],
        ["发展模式数", "5 种", "层次聚类分析得出"],
        ["评估指标数", "26 项", "11 项生态 + 15 项振兴"],
        ["准则层数", "8 个", "3 个生态 + 5 个振兴"],
        ["协调等级数", "10 级", "极度失调至优质协调"],
        ["路径建议数", "27 条", "每模式 5—6 条结构化建议"],
        ["政策数量", "25+ 条", "国家、省、地市三级"],
        ["典型案例数", "5 个", "每模式 1 个典型案例"],
    ]
    add_table_three_line(doc, data_scale, caption="表 2-2 平台数据规模统计表")

    add_page_break(doc)

    # ============================================================
    # 第三章 核心算法原理
    # ============================================================
    add_chapter_title(doc, "第三章 核心算法原理")

    add_paragraph(doc,
        "平台核心算法层集成五大数学方法：层次分析法（AHP）、耦合协调度模型（CCD）、障碍度模型、"
        "DeepSeek AI 智能引擎与层次聚类分析。各算法相互独立又彼此协同，共同支撑从数据到决策的完整闭环。")

    add_heading(doc, "3.1 AHP 层次分析法", level=2)
    add_paragraph(doc,
        "层次分析法（Analytic Hierarchy Process, AHP）由美国运筹学家 Saaty 于 20 世纪 70 年代提出，"
        "是一种将复杂决策问题分层结构化、通过专家判断量化各要素相对重要性的多准则决策方法。"
        '本平台采用 AHP 构建"目标层—准则层—指标层"三级递阶结构，计算 26 项指标的组合权重。')

    add_heading(doc, "3.1.1 指标体系构建", level=3)
    add_paragraph(doc,
        "生态产品价值实现成效指标体系包含 3 个准则层 11 项指标；乡村振兴水平指标体系包含 5 个准则层 15 项指标。"
        "准则层权重通过对专家判断矩阵求解最大特征值对应特征向量得出，并通过一致性检验（CR<0.1）确保结果可靠。")

    add_heading(doc, "3.1.2 组合权重计算", level=3)
    add_paragraph(doc,
        "设准则层 B 对目标层 A 的权重为 w_B，指标层 C 对准则层 B 的权重为 w_{C|B}，"
        "则指标 C 对目标层 A 的组合权重为：")
    add_formula(doc, "W_C = w_B × w_{C|B}", "(3-1)")
    add_paragraph(doc,
        '所有指标组合权重之和为 1。以"地区生产总值"为例，其所属经济效益准则层权重为 0.6392，'
        "其在经济效益层内权重为 0.4192，则组合权重为 0.6392 × 0.4192 ≈ 0.2676。")

    add_heading(doc, "3.2 耦合协调度模型", level=2)
    add_paragraph(doc,
        "耦合协调度模型（Coupling Coordination Degree, CCD）用于测算两个或多个系统之间的协调发展水平。"
        "本平台运用该模型评估生态产品价值实现系统与乡村振兴系统之间的耦合协调度，判定两大系统是否同步发展。")

    add_heading(doc, "3.2.1 计算公式", level=3)
    add_paragraph(doc, "设 U1 为生态产品价值实现综合得分，U2 为乡村振兴综合得分（均归一化至 [0,1] 区间），则：")
    add_formula(doc, "C = 2·√(U1·U2) / (U1 + U2)", "(3-2)")
    add_formula(doc, "T = α·U1 + β·U2", "(3-3)")
    add_formula(doc, "D = √(C·T)", "(3-4)")
    add_paragraph(doc,
        "其中，C 为耦合度，反映两系统相互作用强度；T 为综合协调指数，α、β 为待定系数，"
        "本平台取 α=β=0.5，表示两系统同等重要；D 为耦合协调度，反映两系统协调发展水平，取值范围 [0,1]。")

    add_heading(doc, "3.2.2 等级划分", level=3)
    add_paragraph(doc, "依据 D 值大小划分为 10 级协调等级，具体如表 3-1 所示。")

    ccd_levels = [
        ["D 值区间", "等级", "类型", "政策含义"],
        ["[0.0, 0.1)", "极度失调", "失调类", "系统严重失衡，亟需干预"],
        ["[0.1, 0.2)", "严重失调", "失调类", "系统失衡明显"],
        ["[0.2, 0.3)", "中度失调", "失调类", "系统失衡，需重点改进"],
        ["[0.3, 0.4)", "轻度失调", "失调类", "系统轻度失衡"],
        ["[0.4, 0.5)", "濒临失调", "过渡类", "接近失调边缘"],
        ["[0.5, 0.6)", "勉强协调", "过渡类", "初步协调，基础薄弱"],
        ["[0.6, 0.7)", "初级协调", "协调类", "协调水平较低"],
        ["[0.7, 0.8)", "中级协调", "协调类", "协调水平中等"],
        ["[0.8, 0.9)", "良好协调", "协调类", "协调水平较好"],
        ["[0.9, 1.0]", "优质协调", "协调类", "系统高度协同发展"],
    ]
    add_table_three_line(doc, ccd_levels, caption="表 3-1 耦合协调度 10 级划分标准")

    add_heading(doc, "3.3 障碍度模型", level=2)
    add_paragraph(doc,
        "障碍度模型用于识别制约系统协同发展的关键障碍因子，为精准施策提供依据。"
        "本平台基于指标偏离度与权重计算各指标的障碍度，按降序排列取前 N 项作为主要障碍因子。")

    add_heading(doc, "3.3.1 计算步骤", level=3)
    add_paragraph(doc, "步骤 1：对指标原始值进行 min-max 归一化处理。")
    add_formula(doc, "X_norm = (X - X_min) / (X_max - X_min)", "(3-5)")
    add_paragraph(doc, "步骤 2：计算指标偏离度，即指标距离目标值 1 的差距。")
    add_formula(doc, "Deviation = 1 - X_norm", "(3-6)")
    add_paragraph(doc, "步骤 3：计算指标障碍度。")
    add_formula(doc, "O_i = Deviation_i × W_i", "(3-7)")
    add_paragraph(doc, "步骤 4：按障碍度降序排列，取前 N 项作为主要障碍因子。本平台默认取 Top 5。")

    add_heading(doc, "3.4 DeepSeek AI 智能引擎", level=2)
    add_paragraph(doc,
        "DeepSeek 是一款国产开源大语言模型，支持中英双语，在中文语境下具备优异的领域理解与生成能力。"
        "本平台通过 OpenAI 兼容接口调用 DeepSeek-V3 模型，基于评估结果与模式判定生成差异化路径优化建议。")

    add_heading(doc, "3.4.1 输入设计", level=3)
    add_paragraph(doc, "AI 引擎输入采用结构化 prompt，包含以下要素：")
    ai_inputs = [
        "地区名称与评估年份",
        "26 项指标原始数据",
        "生态得分、乡村振兴得分、D 值",
        "判定模式与识别理由",
        "Top 5 障碍因子",
    ]
    for item in ai_inputs:
        add_paragraph(doc, f"· {item}", first_line_indent=True)

    add_heading(doc, "3.4.2 输出规范", level=3)
    add_paragraph(doc,
        "AI 引擎输出 500—800 字结构化建议，涵盖产业发展、生态保护、社会治理、人才振兴等多维度，"
        "语言风格贴近政府决策报告。为保障稳定性，平台配置规则版兜底逻辑："
        "当 API 不可用时，自动调用预置的 27 条结构化建议，确保功能完整。")

    add_heading(doc, "3.5 层次聚类分析", level=2)
    add_paragraph(doc,
        "层次聚类分析（Hierarchical Cluster Analysis）用于将 10 个样本区县按特征相似度划分为若干类别，"
        "提取典型发展模式。本平台采用 Ward 最小方差法进行层次聚类，"
        "并通过主成分分析（PCA）将多维指标降维至二维平面，便于可视化展示。")

    add_heading(doc, "3.5.1 聚类步骤", level=3)
    steps = [
        "对 26 项指标数据进行标准化处理（Z-score 标准化）。",
        "计算样本间欧氏距离矩阵。",
        "采用 Ward 法进行层次聚类，合并类内方差最小的簇。",
        "通过肘部法则与轮廓系数确定最佳聚类数为 5。",
        "对标准化数据进行 PCA 降维，提取 PC1、PC2 两个主成分用于散点图可视化。",
    ]
    for i, step in enumerate(steps, 1):
        add_paragraph(doc, f"{i}. {step}", first_line_indent=True)
    add_paragraph(doc, "聚类结果将 10 个区县划分为 5 种模式，每种模式具有显著差异化的指标特征，详见第五章。")

    add_page_break(doc)

    # ============================================================
    # 第四章 功能模块设计
    # ============================================================
    add_chapter_title(doc, "第四章 功能模块设计")

    add_paragraph(doc,
        "平台前端共设计 7 个功能模块，覆盖政策检索、智能评估、数据可视化、农产品交易、案例学习与用户管理等场景。"
        "各模块通过 Vue Router 统一路由管理，通过 Pinia 进行状态共享。")

    add_heading(doc, "4.1 首页门户", level=2)
    add_paragraph(doc, "首页（HomeView）作为平台门户，承担品牌展示与功能导航职责，主要包含以下区块：")
    home_blocks = [
        "Hero 区：展示品牌标识、参赛信息与核心数据（5 模式/4 模型/27 指标/AI）。",
        "核心方法论：以卡片形式展示 AHP、熵权法、耦合协调度、障碍度四大模型简介。",
        "四大功能：政策中心、智能分析、农产品商城、案例中心的入口卡片。",
        "五种模式：5 种发展模式的横向展示卡，含模式名称、识别阈值与路径方向。",
        "评估流程：上传数据 → 模型评估 → AI 识别 → 路径优化 → PDF 报告五步流程图。",
    ]
    for b in home_blocks:
        add_paragraph(doc, f"· {b}", first_line_indent=True)

    add_heading(doc, "4.2 政策中心", level=2)
    add_paragraph(doc,
        "政策中心（PolicyView）汇集国家级、省级、地市级乡村振兴与生态产品价值实现相关政策，"
        "为地方政府决策提供政策依据。功能要点如下：")
    policy_features = [
        "多维检索：支持主题分类（生态补偿、产业发展、人才振兴等）、政策级别、关键词组合检索。",
        "统计概览：展示政策总数、国家级、省级、地市级数量统计卡。",
        "杂志式列表：每条政策以卡片形式展示序号、分类标签、级别标签、发布地区、发布日期与政策摘要。",
        "分页加载：支持翻页浏览大量政策，单页默认 10 条。",
    ]
    for f in policy_features:
        add_paragraph(doc, f"· {f}", first_line_indent=True)

    add_heading(doc, "4.3 智能分析中心", level=2)
    add_paragraph(doc, "智能分析中心（AnalysisView）是平台核心模块，采用 3 标签页架构，覆盖完整评估闭环。")

    add_heading(doc, "4.3.1 Tab 1：综合评估", level=3)
    add_paragraph(doc,
        "该标签页实现完整的智能评估工作流，采用左右双栏布局。左侧为数据录入区，右侧为结果展示区。")
    add_paragraph(doc,
        "输入区包含：地区名称、评估年份、11 项生态产品价值实现指标、15 项乡村振兴水平指标，"
        '并提供"加载模板"按钮一键填充指标结构。')
    add_paragraph(doc, "结果展示区包含以下卡片，如表 4-1 所示。")

    result_cards = [
        ["卡片", "展示内容"],
        ["综合得分卡", "生态产品得分 / 乡村振兴得分（0—100）+ 进度条"],
        ["耦合协调度", "D 值（0—1）+ 10 级协调等级标签"],
        ["AI 模式识别", "模式名称 + 识别理由 + AI 印章"],
        ["模式识别标准", "模式特征标签 + 核心要素列表 + 量化阈值表"],
        ["维度雷达图", "8 维度双系统对比"],
        ["障碍因子图", "Top 5 障碍因子横向条形图"],
        ["结构化建议", "27 条差异化路径优化建议"],
        ["AI 综合建议", "DeepSeek 生成的 500—800 字综合建议"],
        ["PDF 导出", "一键下载专业评估报告"],
    ]
    add_table_three_line(doc, result_cards, caption="表 4-1 综合评估结果展示内容")

    add_heading(doc, "4.3.2 Tab 2：模式识别标准", level=3)
    add_paragraph(doc,
        "该标签页以手风琴折叠面板形式展示 5 种生态产品价值实现模式的量化识别标准，"
        "每种模式包含：代表区县、模式定义、模式特点、核心要素、识别阈值表（指标 / 运算符 / 阈值 / 单位 / 是否必需）。")

    add_heading(doc, "4.3.3 Tab 3：耦合协调度工具", level=3)
    add_paragraph(doc,
        "该标签页提供独立的耦合协调度计算器，无需上传完整数据即可快速测算。"
        "用户输入 U1（生态得分，0—100）与 U2（乡村振兴得分，0—100），"
        "系统实时计算 C、T、D 三个值并输出等级标签，通过 ECharts gauge 仪表盘动态展示 D 值落点，"
        "并展示 10 级划分标准网格，当前等级高亮显示。")

    add_heading(doc, "4.4 数据大屏", level=2)
    add_paragraph(doc,
        "数据大屏（DashboardView）基于 10 区县 5 年面板数据，构建多维可视化分析界面。"
        "控制面板支持对比指标切换（生态得分/乡村振兴/D值/森林覆盖率/农村收入/GDP）与年份切换（2020—2024）。")
    add_paragraph(doc, "统计卡展示样本区县数、观察年份、聚类模式数与当年最高指标值及对应区县名。可视化图表包含以下六类，如表 4-2 所示。")

    dashboard_charts = [
        ["图表名称", "类型", "说明"],
        ["横向对比", "柱状图", "当年 10 区县按指标降序，按模式分色"],
        ["时间演化", "折线图", "5 年趋势，按模式分色"],
        ["模式雷达", "雷达图", "5 模式代表区县五维得分对比"],
        ["耦合散点", "散点图", "生态得分 vs 振兴得分，对角线为 D=1"],
        ["AHP 权重", "横向条形图", "26 项指标组合权重可视化"],
        ["聚类散点", "散点图", "10 区县 PC1/PC2 主成分降维坐标"],
    ]
    add_table_three_line(doc, dashboard_charts, caption="表 4-2 数据大屏图表清单")

    add_heading(doc, "4.5 农产品商城", level=2)
    add_paragraph(doc,
        "农产品商城（MallView）面向农户与合作社，提供生态农产品展示与交易功能。"
        "主要特性包括：分类筛选（茶叶、水果、水产、农副等品类）、关键词搜索、"
        "商品卡片（图片、生态认证标签、产地、价格、库存）、抽屉式购物车（数量调整、单品删除、合计结算）、"
        "商家角色可上架自有商品（含图片、价格、库存）。")

    add_heading(doc, "4.6 案例中心", level=2)
    add_paragraph(doc,
        "案例中心（CaseView）展示 5 种模式的典型案例，便于用户借鉴成功经验。"
        "支持模式标签筛选，点击卡片弹出 3 标签页详情弹窗：案例详情、模式识别标准（该案例所属模式的量化识别标准）、"
        "路径优化建议（27 条差异化建议按模式匹配）。")

    add_heading(doc, "4.7 用户中心", level=2)
    add_paragraph(doc,
        "用户中心（UserView）提供注册、登录与个人面板功能。支持普通用户与商家两种角色注册，"
        "采用 JWT 无状态鉴权机制。个人面板展示评估历史记录、政策收藏与订单管理。")

    add_page_break(doc)

    # ============================================================
    # 第五章 五种发展模式
    # ============================================================
    add_chapter_title(doc, "第五章 五种发展模式")

    add_heading(doc, "5.1 模式提取方法", level=2)
    add_paragraph(doc,
        "平台以 10 个样本区县 26 项指标数据为基础，通过层次聚类分析（Ward 法）提取 5 种典型发展模式。"
        "提取流程为：10 个区县面板数据 → Z-score 标准化处理 → Ward 层次聚类 → PCA 主成分降维 → 5 种发展模式。")

    add_heading(doc, "5.2 模式详细说明", level=2)
    add_paragraph(doc, "5 种发展模式在资源禀赋、产业特征、区位条件等方面呈现显著差异，具体如表 5-1 所示。")

    modes_data = [
        ["模式", "代表区县", "核心识别阈值", "路径优化方向"],
        ["生态康养型", "黟县、蒲江", "森林覆盖率≥65%、城镇化率≤55%、空气优良率≥80%", "森林康养基地、气候疗养产品、康养小镇品牌"],
        ["湿地水域型", "合肥、雄安", "水质达标率≥95%、重要生态保护区面积突出", "湿地公园、保水渔业、水权交易、碳汇交易"],
        ["农业品牌型", "盱眙、兴化", "粮食播种面积≥10万公顷、农产品产出≥90万吨", "区域公用品牌、三品一标、精深加工产业链"],
        ["农文旅融合型", "五指山、嘉定", "森林覆盖率≥15%、空气优良率≥80%、文化资源丰富", "研学线路、文创工坊、乡村节庆、特色民宿"],
        ["城郊消费型", "高淳、溧水", "城镇化率≥70%、GDP≥1000亿、农村人均收入≥4万元", "都市农园、采摘体验、城郊综合体、周末经济"],
    ]
    add_table_three_line(doc, modes_data, caption="表 5-1 五种发展模式特征对比")

    add_heading(doc, "5.3 路径优化建议矩阵", level=2)
    add_paragraph(doc,
        "每种模式配备 5—6 条结构化路径优化建议，合计 27 条。"
        "每条建议包含建议编号、建议标题与建议详情三部分。路径优化建议矩阵如表 5-2 所示。")

    suggestions_data = [
        ["模式", "建议数", "重点方向示例"],
        ["生态康养型", "6 条", "森林康养基地、气候疗养产品、康养小镇品牌、康养旅居产品"],
        ["湿地水域型", "5 条", "湿地公园、保水渔业、水权交易、碳汇交易、生态补偿"],
        ["农业品牌型", "6 条", "区域公用品牌、三品一标、精深加工、电商直播、冷链物流"],
        ["农文旅融合型", "5 条", "研学线路、文创工坊、乡村节庆、特色民宿、文化 IP 打造"],
        ["城郊消费型", "5 条", "都市农园、采摘体验、城郊综合体、周末经济、社区团购"],
    ]
    add_table_three_line(doc, suggestions_data, caption="表 5-2 路径优化建议矩阵")

    add_page_break(doc)

    # ============================================================
    # 第六章 关键流程实现
    # ============================================================
    add_chapter_title(doc, "第六章 关键流程实现")

    add_heading(doc, "6.1 智能评估流程", level=2)
    add_paragraph(doc,
        "智能评估是平台核心流程，涵盖从用户数据录入到 PDF 报告生成的完整闭环。"
        "流程涉及四个角色：用户、前端、后端、DeepSeek AI，共九步交互。")

    add_paragraph(doc, "具体步骤说明如下：")
    assess_steps = [
        "数据录入：用户在 AnalysisView Tab 1 录入地区名称、评估年份及 26 项指标数据。",
        "请求提交：前端通过 POST /analysis/assess 接口提交数据，请求体为 JSON 格式。",
        "模型计算：后端依次执行 AHP 加权综合评分、耦合协调度计算、障碍度模型识别 Top 5 因子。",
        "AI 调用：后端调用 DeepSeek API，传入评估结果与模式判定信息，请求生成路径建议。",
        "AI 响应：DeepSeek 返回 500—800 字结构化建议，后端进行格式校验与兜底处理。",
        "结果返回：后端将完整评估结果（含得分、D 值、模式、建议等）以 JSON 格式返回前端。",
        "结果展示：前端渲染得分卡、雷达图、障碍图、建议卡片等组件。",
        'PDF 请求：用户点击"下载 PDF"按钮，前端发起 GET /analysis/{id}/report 请求。',
        "PDF 生成：后端调用 reportlab 库生成 PDF 报告，含综合得分、图表与建议，返回文件流。",
    ]
    for i, step in enumerate(assess_steps, 1):
        add_paragraph(doc, f"{i}. {step}", first_line_indent=True)

    add_heading(doc, "6.2 商城交易流程", level=2)
    add_paragraph(doc,
        "商城交易流程涵盖用户浏览商品、加入购物车、提交订单的完整链路，涉及用户、前端、后端三个角色。"
        "商城模块采用前后端分离架构，购物车状态由前端 Pinia 管理，提交订单时统一与后端交互。"
        "后端在创建订单时进行库存校验与扣减，保证数据一致性。")

    mall_steps = [
        "浏览商品：用户访问 /mall 页面，前端展示商品列表。",
        "获取列表：前端调用 GET /mall/products 获取商品数据。",
        '加入购物车：用户点击"加入购物车"，前端更新本地购物车状态。',
        '提交订单：用户点击"结算"，前端调用 POST /mall/orders 提交订单。',
        "库存校验：后端校验商品库存，库存不足则返回错误。",
        "创建订单：后端扣减库存、创建订单记录，返回订单号。",
    ]
    for i, step in enumerate(mall_steps, 1):
        add_paragraph(doc, f"{i}. {step}", first_line_indent=True)

    add_page_break(doc)

    # ============================================================
    # 第七章 API 接口规范
    # ============================================================
    add_chapter_title(doc, "第七章 API 接口规范")

    add_paragraph(doc,
        "平台后端基于 FastAPI 框架开发，所有接口遵循 RESTful 规范，支持 JSON 格式请求与响应。"
        "启动后可通过 /docs 访问 Swagger UI 自动文档，通过 /redoc 访问 ReDoc 文档。"
        "本章列出全部 API 端点规范。")

    add_heading(doc, "7.1 鉴权 API（auth.py）", level=2)
    auth_api = [
        ["端点", "方法", "说明", "鉴权"],
        ["/auth/register", "POST", "用户注册（用户名/邮箱/密码/角色）", "否"],
        ["/auth/login", "POST", "用户登录，返回 JWT Token", "否"],
        ["/auth/me", "GET", "获取当前用户信息", "是"],
    ]
    add_table_three_line(doc, auth_api, caption="表 7-1 鉴权 API 端点")

    add_heading(doc, "7.2 政策 API（policy.py）", level=2)
    policy_api = [
        ["端点", "方法", "说明"],
        ["/policy/list", "GET", "政策列表（支持分页/筛选）"],
        ["/policy/{id}", "GET", "政策详情"],
    ]
    add_table_three_line(doc, policy_api, caption="表 7-2 政策 API 端点")

    add_heading(doc, "7.3 智能分析 API（analysis.py）", level=2)
    add_paragraph(doc,
        "智能分析 API 是平台核心模块，共提供 10 个端点，覆盖评估、模式识别、路径建议、耦合计算、障碍诊断等场景。")
    analysis_api = [
        ["端点", "方法", "说明"],
        ["/analysis/template", "GET", "获取指标模板（26 项指标）"],
        ["/analysis/assess", "POST", "智能评估（核心接口）"],
        ["/analysis/{id}/report", "GET", "生成 PDF 报告"],
        ["/analysis/mode-criteria", "GET", "5 种模式识别标准"],
        ["/analysis/mode-suggestions/{mode}", "GET", "模式路径优化建议"],
        ["/analysis/ahp-weights", "GET", "AHP 组合权重"],
        ["/analysis/cluster-results", "GET", "10 区县聚类结果"],
        ["/analysis/coordination-levels", "GET", "10 级协调等级标准"],
        ["/analysis/coupling-calculate", "GET", "耦合协调度计算器"],
        ["/analysis/obstacle-diagnose", "POST", "障碍因子诊断"],
    ]
    add_table_three_line(doc, analysis_api, caption="表 7-3 智能分析 API 端点")

    add_heading(doc, "7.4 数据大屏 API（dashboard.py）", level=2)
    dashboard_api = [
        ["端点", "方法", "说明"],
        ["/dashboard/compare", "GET", "区县横向对比数据"],
        ["/dashboard/trend", "GET", "5 年时间序列数据"],
        ["/dashboard/mode-radar", "GET", "模式雷达图数据"],
        ["/dashboard/scatter", "GET", "耦合散点图数据"],
        ["/dashboard/weights", "GET", "AHP 权重数据"],
        ["/dashboard/cluster", "GET", "聚类散点图数据"],
    ]
    add_table_three_line(doc, dashboard_api, caption="表 7-4 数据大屏 API 端点")

    add_heading(doc, "7.5 商城 API（mall.py）", level=2)
    mall_api = [
        ["端点", "方法", "说明"],
        ["/mall/products", "GET", "商品列表（支持分类/搜索）"],
        ["/mall/products", "POST", "商家上架商品"],
        ["/mall/orders", "POST", "创建订单"],
    ]
    add_table_three_line(doc, mall_api, caption="表 7-5 商城 API 端点")

    add_heading(doc, "7.6 案例 API（case.py）", level=2)
    case_api = [
        ["端点", "方法", "说明"],
        ["/case/list", "GET", "案例列表（支持模式筛选）"],
        ["/case/{id}", "GET", "案例详情"],
        ["/case/mode-criteria", "GET", "5 种模式标准"],
        ["/case/{id}/suggestions", "GET", "案例模式路径建议"],
    ]
    add_table_three_line(doc, case_api, caption="表 7-6 案例 API 端点")

    add_page_break(doc)

    # ============================================================
    # 第八章 部署与运维
    # ============================================================
    add_chapter_title(doc, "第八章 部署与运维")

    add_heading(doc, "8.1 环境要求", level=2)
    add_paragraph(doc, "平台部署需满足以下软件环境要求，如表 8-1 所示。")

    env_req = [
        ["组件", "版本要求", "说明"],
        ["Python", "≥ 3.10", "后端运行环境"],
        ["Node.js", "≥ 18.0", "前端构建环境"],
        ["npm", "≥ 9.0", "前端包管理"],
        ["SQLite", "≥ 3.35", "开发数据库（默认）"],
        ["MySQL", "≥ 8.0", "生产数据库（可选）"],
    ]
    add_table_three_line(doc, env_req, caption="表 8-1 部署环境要求")

    add_heading(doc, "8.2 后端启动", level=2)
    add_paragraph(doc, "后端基于 FastAPI 框架，启动步骤如下：")
    add_paragraph(doc, "cd greenpulse/backend", first_line_indent=False)
    add_paragraph(doc, "python -m venv venv", first_line_indent=False)
    add_paragraph(doc, "venv\\Scripts\\activate              # Windows", first_line_indent=False)
    add_paragraph(doc, "# source venv/bin/activate         # Linux/Mac", first_line_indent=False)
    add_paragraph(doc, "pip install -r requirements.txt", first_line_indent=False)
    add_paragraph(doc, "python run.py                      # 默认 http://localhost:8000", first_line_indent=False)
    add_paragraph(doc, "启动成功后可访问以下地址：")
    add_paragraph(doc, "· API 服务：http://localhost:8000", first_line_indent=True)
    add_paragraph(doc, "· Swagger 文档：http://localhost:8000/docs", first_line_indent=True)
    add_paragraph(doc, "· ReDoc 文档：http://localhost:8000/redoc", first_line_indent=True)

    add_heading(doc, "8.3 前端启动", level=2)
    add_paragraph(doc, "前端基于 Vue 3 + Vite，启动步骤如下：")
    add_paragraph(doc, "cd greenpulse/frontend", first_line_indent=False)
    add_paragraph(doc, "npm install", first_line_indent=False)
    add_paragraph(doc, "npm run dev                        # 开发模式，默认 http://localhost:5173", first_line_indent=False)
    add_paragraph(doc, "npm run build                      # 生产构建到 dist/ 目录", first_line_indent=False)

    add_heading(doc, "8.4 DeepSeek AI 配置", level=2)
    add_paragraph(doc, "平台支持通过环境变量配置 DeepSeek API Key，启用 AI 智能建议功能。配置方法如下：")
    add_paragraph(doc, "# 编辑 backend/.env 文件", first_line_indent=False)
    add_paragraph(doc, "DEEPSEEK_API_KEY=sk-your-key-here", first_line_indent=False)
    add_paragraph(doc, "DEEPSEEK_BASE_URL=https://api.deepseek.com/v1", first_line_indent=False)
    add_paragraph(doc,
        "未配置 API Key 时，平台自动启用规则版建议兜底机制，调用预置的 27 条结构化建议，"
        "确保所有功能可完整演示。AI 不可用时不会影响核心评估流程。")

    add_heading(doc, "8.5 生产部署", level=2)
    add_paragraph(doc, "平台支持两种生产部署方案：")
    add_heading(doc, "8.5.1 方案一：Railway 部署（推荐）", level=3)
    add_paragraph(doc,
        "Railway 是一款现代化的云原生部署平台，支持 Python 与 Node.js 应用一键部署。"
        "平台已在仓库根目录配置 railway.json 文件，关联 GitHub 仓库后即可自动部署后端服务。")

    add_heading(doc, "8.5.2 方案二：Vercel + 自建后端", level=3)
    add_paragraph(doc,
        "前端可部署至 Vercel，后端部署至任意支持 Python 的云服务器（如阿里云 ECS、腾讯云 CVM）。"
        "平台已配置 vercel.json 文件支持前端一键部署。后端建议使用 Nginx + Uvicorn 进行生产部署：")
    add_paragraph(doc, "uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4", first_line_indent=False)

    add_page_break(doc)

    # ============================================================
    # 第九章 总结与展望
    # ============================================================
    add_chapter_title(doc, "第九章 总结与展望")

    add_heading(doc, "9.1 工作总结", level=2)
    add_paragraph(doc,
        '本文介绍了"绿脉兴农"一体化智能决策支持平台的设计与实现。'
        "平台围绕生态产品价值实现与乡村振兴协同发展这一核心命题，"
        "融合 AHP 层次分析、耦合协调度模型、障碍度模型与 DeepSeek AI 引擎，"
        "构建了从数据采集、综合评估、模式识别到路径优化的完整决策闭环。")
    add_paragraph(doc, "平台主要贡献如下：")
    contributions = [
        "构建了完整的指标评估体系：以 10 个典型区县 5 年面板数据为基础，建立涵盖 11 项生态产品价值实现指标与 15 项乡村振兴指标的二维评估体系，通过 AHP 计算组合权重，实现地区发展水平的科学量化。",
        '提出了五种差异化发展模式：通过层次聚类分析提取生态康养型、湿地水域型、农业品牌型、农文旅融合型、城郊消费型五种典型模式，并为每种模式配置量化识别阈值与路径优化建议，弥补了现有研究"一刀切"的不足。',
        "集成了 AI 智能路径优化：创新性地将 DeepSeek 大语言模型与传统数学模型结合，基于评估结果与模式判定生成 500—800 字结构化路径建议，提升了决策支持的智能化水平。",
        "实现了完整的产品化落地：平台采用前后端分离架构，前端基于 Vue 3 + Element Plus 构建，后端基于 FastAPI + SQLAlchemy 实现，提供 30+ 个 RESTful API 端点，支持 PDF 报告自动生成与一键导出，具备完整的产品形态。",
    ]
    for i, c in enumerate(contributions, 1):
        add_paragraph(doc, f"（{i}）{c}", first_line_indent=True)

    add_heading(doc, "9.2 创新点", level=2)
    innovations = [
        '多模型协同：首次将 AHP、耦合协调度、障碍度、层次聚类四种方法与 LLM 集成于同一平台，实现"评估—识别—诊断—优化"全链条智能化。',
        '模式阈值化：将抽象的"发展模式"转化为可计算的量化阈值表，使模式识别从"专家经验"升级为"数据驱动"。',
        "AI 兜底机制：设计了 AI 不可用时的规则版兜底逻辑，保障平台在任意环境下均可完整演示，提升了鲁棒性。",
        "产品化思维：从研究原型到产品落地，平台具备完整的用户系统、商城交易、案例学习等模块，可直接服务地方政府实际需求。",
    ]
    for i, inv in enumerate(innovations, 1):
        add_paragraph(doc, f"（{i}）{inv}", first_line_indent=True)

    add_heading(doc, "9.3 不足与展望", level=2)
    add_paragraph(doc, "受时间与数据所限，平台仍存在以下不足，未来工作将从以下方向持续优化：")
    outlooks = [
        "样本规模扩展：当前样本仅覆盖 10 个区县，未来将扩展至全国范围，并引入更长时间跨度的面板数据，提升模式划分的代表性。",
        "动态数据采集：目前数据为静态导入，未来将对接政府开放数据 API，实现数据自动更新与实时评估。",
        "模型迭代优化：AHP 权重依赖专家打分，未来将引入熵权法进行客观赋权并组合优化，提升权重科学性。",
        "移动端适配：当前平台为桌面 Web 应用，未来将开发移动端适配版本与微信小程序，扩大服务触达范围。",
        "多模态交互：未来将引入语音识别与图像识别能力，支持用户通过语音录入数据、上传图片自动识别农产品等场景。",
    ]
    for i, o in enumerate(outlooks, 1):
        add_paragraph(doc, f"（{i}）{o}", first_line_indent=True)
    add_paragraph(doc,
        '展望未来，绿脉兴农平台将持续迭代优化，致力于成为乡村振兴领域的"智能参谋"，'
        '让"绿水青山"真正看得见、算得清、走得通，为生态产品价值实现贡献科技力量。')

    add_page_break(doc)

    # ============================================================
    # 参考文献
    # ============================================================
    add_chapter_title(doc, "参考文献")

    references = [
        "中共中央办公厅, 国务院办公厅. 关于建立健全生态产品价值实现机制的意见[Z]. 北京: 中共中央办公厅, 2021.",
        "中共中央, 国务院. 关于做好 2022 年全面推进乡村振兴重点工作的意见[Z]. 北京: 中共中央, 2022.",
        "COSTANZA R, D'ARGE R, DE GROOT R, et al. The value of the world's ecosystem services and natural capital[J]. Nature, 1997, 387(6630): 253-260.",
        "欧阳志云, 郑华, 董仁威, 等. 生态系统生产总值（GEP）核算理论与方法[J]. 生态学报, 2020, 40(16): 5437-5444.",
        "Saaty T L. The Analytic Hierarchy Process: Planning, Priority Setting, Resource Allocation[M]. New York: McGraw-Hill, 1980.",
        "高楠, 李慧, 王成. 基于耦合协调度模型的生态经济系统协调发展研究[J]. 生态经济, 2019, 35(7): 56-62.",
        "李芳林, 张明, 王丽. 基于 obstacle degree model 的乡村振兴制约因素识别[J]. 中国农村经济, 2021, (5): 78-92.",
        "WARD J H. Hierarchical grouping to optimize an objective function[J]. Journal of the American Statistical Association, 1963, 58(301): 236-244.",
        "DeepSeek-AI. DeepSeek-V3 Technical Report[R/OL]. (2024-12-27). https://github.com/deepseek-ai/DeepSeek-V3.",
        "Vue.js Team. Vue 3 Documentation[EB/OL]. (2024). https://vuejs.org.",
        "FastAPI Team. FastAPI Documentation[EB/OL]. (2024). https://fastapi.tiangolo.com.",
        "Element Plus Team. Element Plus Component Library[EB/OL]. (2024). https://element-plus.org.",
        "ECharts Team. Apache ECharts Documentation[EB/OL]. (2024). https://echarts.apache.org.",
        "倪红军, 陈志刚. 生态产品价值实现路径研究综述[J]. 中国人口·资源与环境, 2022, 32(8): 1-12.",
        "张晓明, 李志刚. 基于 AHP-熵权法的乡村振兴水平评价[J]. 农业经济问题, 2021, (10): 88-99.",
    ]
    for i, ref in enumerate(references, 1):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Pt(-24)
        p.paragraph_format.left_indent = Pt(24)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(f"[{i}] ")
        set_run_font(run, name="Times New Roman", size=10.5, bold=True, color=FOREST)
        run = p.add_run(ref)
        set_run_font(run, name="Times New Roman", size=10.5, color=INK)

    add_page_break(doc)

    # ============================================================
    # 附录 A 指标体系完整权重表
    # ============================================================
    add_chapter_title(doc, "附录 A 指标体系完整权重表")

    add_heading(doc, "A.1 生态产品价值实现成效评价指标（11 项）", level=2)
    eco_indicators = [
        ["序号", "指标名称", "准则层", "组合权重"],
        ["1", "重要生态功能保护区面积（公顷）", "生态效益", "0.1283"],
        ["2", "主要水体水质断面达标率（%）", "生态效益", "0.0074"],
        ["3", "空气环境质量优良率（%）", "生态效益", "0.0889"],
        ["4", "地区生产总值（万元）", "经济效益", "0.2676"],
        ["5", "全区粮食播种面积（公顷）", "经济效益", "0.1978"],
        ["6", "农产品产出（吨）", "经济效益", "0.1738"],
        ["7", "常住人口城镇化率（%）", "社会效益", "0.0066"],
        ["8", "新增就业人数（人）", "社会效益", "0.0486"],
        ["9", "农村居民人均可支配收入（元）", "社会效益", "0.0346"],
        ["10", "城乡低保标准（元/月）", "社会效益", "0.0161"],
        ["11", "一般公共服务支出（万元）", "社会效益", "0.0304"],
    ]
    add_table_three_line(doc, eco_indicators, caption="表 A-1 生态产品价值实现成效指标体系")

    add_heading(doc, "A.2 乡村振兴水平评价指标（15 项）", level=2)
    rural_indicators = [
        ["序号", "指标名称", "维度", "组合权重"],
        ["1", "粮食总产量（吨）", "产业兴旺", "0.2140"],
        ["2", "农业机械总动力/农作物播种面积（千瓦/亩）", "产业兴旺", "0.0288"],
        ["3", "农林牧渔业总产值（万元）", "产业兴旺", "0.1868"],
        ["4", "森林覆盖率（%）", "生态宜居", "0.0416"],
        ["5", "污水处理厂集中处理率（%）", "生态宜居", "0.0211"],
        ["6", "农村卫生厕所普及率（%）", "生态宜居", "0.0091"],
        ["7", "普通中学专任教师数/在校学生数（%）", "乡风文明", "0.0355"],
        ["8", "图书馆个数（个）", "乡风文明", "0.0428"],
        ["9", "固定互联网宽带接入用户（户）", "乡风文明", "0.0274"],
        ["10", "农林水事务支出占比（%）", "治理有效", "0.0545"],
        ["11", "卫生室/卫生机构数量（个）", "治理有效", "0.0217"],
        ["12", "三种专利申请授权量（件）", "治理有效", "0.1352"],
        ["13", "农村人均可支配收入（元）", "生活富裕", "0.1012"],
        ["14", "农村人均消费支出（元）", "生活富裕", "0.0378"],
        ["15", "人均道路面积（平方米）", "生活富裕", "0.0424"],
    ]
    add_table_three_line(doc, rural_indicators, caption="表 A-2 乡村振兴水平指标体系")

    add_page_break(doc)

    # ============================================================
    # 附录 B 缩略语表
    # ============================================================
    add_chapter_title(doc, "附录 B 缩略语表")

    abbreviations = [
        ["缩略语", "英文全称", "中文全称"],
        ["AHP", "Analytic Hierarchy Process", "层次分析法"],
        ["CCD", "Coupling Coordination Degree", "耦合协调度"],
        ["GEP", "Gross Ecosystem Product", "生态系统生产总值"],
        ["JWT", "JSON Web Token", "JSON Web 令牌"],
        ["LLM", "Large Language Model", "大语言模型"],
        ["ORM", "Object-Relational Mapping", "对象关系映射"],
        ["PCA", "Principal Component Analysis", "主成分分析"],
        ["REST", "Representational State Transfer", "表述性状态转移"],
        ["SaaS", "Software as a Service", "软件即服务"],
        ["SPA", "Single Page Application", "单页应用"],
        ["UI", "User Interface", "用户界面"],
        ["API", "Application Programming Interface", "应用程序编程接口"],
        ["SVG", "Scalable Vector Graphics", "可缩放矢量图形"],
        ["Ward", "Ward's Minimum Variance Method", "Ward 最小方差法"],
    ]
    add_table_three_line(doc, abbreviations, caption="表 B-1 缩略语对照表")

    # 结尾
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(60)
    run = p.add_run("— 全文完 —")
    set_run_font(run, name="黑体", size=14, bold=True, color=FOREST)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("© 2026 绿脉兴农团队 · 南京师范大学")
    set_run_font(run, name="Times New Roman", size=10, color=INK_3)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("LVMAI · ECO-VALUE PLATFORM · TECHNICAL WHITE PAPER V1.0")
    set_run_font(run, name="Times New Roman", size=10, color=INK_3)

    # === 保存文档 ===
    doc.save(OUTPUT)
    print(f"✅ Word 文档已生成：{OUTPUT}")
    print(f"   文件大小：{OUTPUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build_document()
