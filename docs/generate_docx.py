"""
绿脉兴农平台功能说明书 · Word 文档生成脚本（含目录、截图、操作流程）

运行：python docs/generate_docx.py
输出：docs/绿脉兴农平台功能说明书.docx
"""
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path

OUTPUT = Path(__file__).parent / "绿脉兴农平台功能说明书.docx"
SHOTS = Path(__file__).parent / "screenshots"


# ===== 工具函数 =====
def set_run_font(run, name="宋体", name_ascii="Times New Roman", size=12, bold=False):
    run.font.name = name_ascii
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    run.font.size = Pt(size)
    run.font.bold = bold


def add_paragraph(doc, text="", align=WD_ALIGN_PARAGRAPH.LEFT,
                  first_line_indent=True, font_name="宋体", font_size=12,
                  bold=False, line_spacing=1.5, space_before=0, space_after=0):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = line_spacing
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    if first_line_indent:
        pf.first_line_indent = Pt(font_size * 2)
    if text:
        run = p.add_run(text)
        set_run_font(run, name=font_name, size=font_size, bold=bold)
    return p


def add_heading(doc, text, level=1, align=WD_ALIGN_PARAGRAPH.LEFT):
    sizes = {1: 16, 2: 14, 3: 12}
    s = sizes.get(level, 12)
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_before = Pt(12 if level <= 2 else 6)
    pf.space_after = Pt(6)
    run = p.add_run(text)
    set_run_font(run, name="黑体", name_ascii="Times New Roman", size=s, bold=True)
    return p


def add_chapter_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_before = Pt(0)
    pf.space_after = Pt(18)
    run = p.add_run(text)
    set_run_font(run, name="黑体", size=18, bold=True)
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), '000000')
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def add_table_three_line(doc, data, header=True, caption=None):
    if caption:
        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_before = Pt(6)
        cap_p.paragraph_format.space_after = Pt(3)
        run = cap_p.add_run(caption)
        set_run_font(run, name="黑体", size=10.5, bold=True)

    rows = len(data)
    cols = len(data[0]) if data else 0
    table = doc.add_table(rows=rows, cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for i, row_data in enumerate(data):
        for j, cell_text in enumerate(row_data):
            cell = table.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (i == 0 or j > 0) else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(cell_text))
            is_header = (i == 0 and header)
            set_run_font(run, name="黑体" if is_header else "宋体",
                         size=10.5, bold=is_header)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    tbl = table._element
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')

    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'none')
        tblBorders.append(border)
    tblPr.append(tblBorders)

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


def add_bullet(doc, text, font_size=12):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.left_indent = Pt(font_size * 2)
    pf.first_line_indent = Pt(-font_size)
    run = p.add_run("• " + text)
    set_run_font(run, size=font_size)
    return p


def add_page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(WD_BREAK.PAGE)


def add_figure(doc, img_path, num, caption, width=15):
    """插入图片 + 图题"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(str(img_path), width=Cm(width))
    # 图题
    cap_p = doc.add_paragraph()
    cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap_p.paragraph_format.space_before = Pt(3)
    cap_p.paragraph_format.space_after = Pt(12)
    run = cap_p.add_run(f"图 {num}  {caption}")
    set_run_font(run, name="黑体", size=10.5, bold=True)


def add_toc(doc):
    """插入自动目录域（在 Word 中按 F9 更新）"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("目  录")
    set_run_font(run, name="黑体", size=18, bold=True)

    # TOC 域
    p = doc.add_paragraph()
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
    t_run = OxmlElement('w:r')
    t_text = OxmlElement('w:t')
    t_text.text = '（请在 Word 中按 F9 或右键"更新域"生成目录）'
    t_run.append(t_text)
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(t_run)
    run._r.append(fldChar3)


# ============================================================
# 文档生成主流程
# ============================================================
def build_document():
    doc = Document()

    # === 页面设置 ===
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(3.17)
        section.right_margin = Cm(3.17)

    # ============================================================
    # 封面
    # ============================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(120)
    run = p.add_run("绿脉兴农  LVMAI · ECO-VALUE PLATFORM")
    set_run_font(run, name="黑体", size=22, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(60)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("绿脉兴农平台")
    set_run_font(run, name="黑体", size=36, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("功能说明书")
    set_run_font(run, name="黑体", size=36, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(120)
    run = p.add_run("生态产品价值实现赋能乡村振兴一体化智能系统")
    set_run_font(run, name="黑体", size=16)

    info_items = [
        ("文档版本", "V1.0"),
        ("发布日期", "2026 年 07 月"),
        ("编制单位", "南京师范大学 · 绿脉兴农团队"),
    ]
    for label, value in info_items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(f"{label}：")
        set_run_font(run, name="黑体", size=11, bold=True)
        run = p.add_run(value)
        set_run_font(run, name="宋体", size=11)

    add_page_break(doc)

    # ============================================================
    # 目录
    # ============================================================
    add_toc(doc)
    add_page_break(doc)

    # ============================================================
    # 第一章 平台简介
    # ============================================================
    add_chapter_title(doc, "第一章 平台简介")

    add_heading(doc, "1.1 平台是做什么的", level=2)
    add_paragraph(doc,
        '绿脉兴农平台是一款帮助地方政府"算清生态账、看清发展路、走好振兴步"的在线工具。'
        "用户只需输入一个地区的各项指标数据，平台就能自动算出生态产品价值实现得分、"
        "乡村振兴得分、两套系统的协调程度，并告诉用户这个地区属于哪种发展模式、"
        "当前最大的短板在哪里、下一步该怎么走。")

    add_heading(doc, "1.2 平台能做什么", level=2)
    add_table_three_line(doc, [
        ["功能", "一句话说明"],
        ["算分", "输入 26 项指标，自动算出生态得分和振兴得分（0—100 分）"],
        ["判模式", "根据数据特征，识别该地区属于 5 种发展模式中的哪一种"],
        ["找短板", "自动列出制约发展的前 5 个主要障碍因子"],
        ["给建议", "AI 生成 500—800 字的个性化路径优化建议"],
        ["看数据", "6 类图表直观展示 10 个区县 5 年的数据规律"],
        ["出报告", "一键导出 PDF 评估报告，可直接用于汇报"],
    ], caption="表 1-1  平台核心功能")

    add_heading(doc, "1.3 数据覆盖范围", level=2)
    add_table_three_line(doc, [
        ["项目", "数量", "说明"],
        ["样本区县", "10 个", "江苏 6、浙江 2、安徽 1、四川 1"],
        ["时间跨度", "5 年", "2020—2024 年"],
        ["发展模式", "5 种", "由数据聚类得出，非人为划分"],
        ["评估指标", "26 项", "生态 11 项 + 振兴 15 项"],
        ["路径建议", "27 条", "每种模式 5—6 条"],
    ], caption="表 1-2  数据覆盖范围")

    add_page_break(doc)

    # ============================================================
    # 第二章 功能模块详解
    # ============================================================
    add_chapter_title(doc, "第二章 功能模块详解")

    add_paragraph(doc,
        "平台共 7 个功能模块。下面逐一介绍每个模块能看到什么、能做什么、怎么操作。")

    # ---- 2.1 首页 ----
    add_heading(doc, "2.1 首页", level=2)
    add_paragraph(doc, "首页是平台门户，展示平台全貌与核心入口。")
    add_figure(doc, SHOTS / "01_home.png", "2-1", "首页界面")
    add_paragraph(doc, "操作说明：")
    add_bullet(doc, "顶部导航栏点击任意菜单可进入对应模块")
    add_bullet(doc, "向下滚动可查看核心方法论、四大功能入口、五种模式展示")
    add_bullet(doc, "底部展示完整评估流程图，了解从数据到报告的全过程")

    # ---- 2.2 政策中心 ----
    add_heading(doc, "2.2 政策中心", level=2)
    add_paragraph(doc, "汇集国家、省、地市三级乡村振兴与生态产品价值实现相关政策。")
    add_figure(doc, SHOTS / "02_policy.png", "2-2", "政策中心界面")
    add_paragraph(doc, "操作说明：")
    add_bullet(doc, "左侧可按主题分类、政策级别筛选")
    add_bullet(doc, "顶部搜索框输入关键词检索政策")
    add_bullet(doc, "每条政策卡片展示序号、分类、级别、地区、日期与摘要")
    add_bullet(doc, "点击卡片可查看政策全文")
    add_bullet(doc, "底部支持翻页，每页 10 条")

    # ---- 2.3 智能分析中心 ----
    add_heading(doc, "2.3 智能分析中心", level=2)
    add_paragraph(doc,
        "这是平台最核心的模块。用户在这里输入数据，平台自动完成全部计算并给出结果。"
        "界面分为左右两栏：左边填数据，右边看结果。下方有 4 个标签页切换不同功能。")
    add_figure(doc, SHOTS / "03_analysis.png", "2-3", "智能分析中心界面")

    add_heading(doc, "2.3.1 智能评估（第一个标签）", level=3)
    add_paragraph(doc, "操作流程：")
    add_bullet(doc, "第 1 步：在左侧输入区填写地区名称、评估年份")
    add_bullet(doc, "第 2 步：填写 11 项生态指标 + 15 项振兴指标的数据")
    add_bullet(doc, '第 3 步：也可点击"加载模板"按钮一键填充示例数据')
    add_bullet(doc, '第 4 步：点击"开始评估"按钮，等待 3 秒')
    add_bullet(doc, "第 5 步：右侧自动展示全部结果")
    add_paragraph(doc, "结果包含以下卡片：")
    add_table_three_line(doc, [
        ["卡片", "看到什么"],
        ["综合得分", "生态得分 / 振兴得分（0—100 分）+ 进度条"],
        ["协调程度", 'D 值（0—1）+ 10 级等级标签（如"初级协调"）'],
        ["模式识别", "判定为 5 种模式中的哪一种 + 识别理由"],
        ["雷达图", "8 个维度双系统对比，一眼看出强弱项"],
        ["障碍图", "前 5 个最大短板横向条形图"],
        ["建议", "27 条结构化建议 + AI 生成的综合建议"],
        ["导出", "一键下载 PDF 评估报告"],
    ], caption="表 2-1  评估结果说明")

    add_heading(doc, "2.3.2 模式识别标准（第二个标签）", level=3)
    add_paragraph(doc,
        "这里展示 5 种发展模式的量化识别标准。点击任意模式可展开详情，"
        "包含代表区县、模式定义、核心要素、识别阈值表。")

    add_heading(doc, "2.3.3 协调度计算器（第三个标签）", level=3)
    add_paragraph(doc, "快速测算工具，无需填全部数据：")
    add_bullet(doc, "输入生态得分 U1（0—100）")
    add_bullet(doc, "输入振兴得分 U2（0—100）")
    add_bullet(doc, "系统实时算出协调度 D 值并显示等级")
    add_bullet(doc, "仪表盘动态展示 D 值落点")

    add_heading(doc, "2.3.4 障碍度诊断（第四个标签）", level=3)
    add_paragraph(doc, "独立诊断工具，找出制约发展的关键短板：")
    add_bullet(doc, "输入 26 项指标数据与权重")
    add_bullet(doc, "系统自动算出每项指标的障碍度")
    add_bullet(doc, "按从大到小排序，取前 10 项展示")
    add_bullet(doc, "横向条形图直观展示，附诊断结论")

    # ---- 2.4 数据大屏 ----
    add_heading(doc, "2.4 数据大屏", level=2)
    add_paragraph(doc, "10 个区县 5 年数据的可视化中心，一眼看清规律。")
    add_figure(doc, SHOTS / "04_dashboard.png", "2-4", "数据大屏界面")
    add_paragraph(doc, "操作说明：")
    add_bullet(doc, "顶部选择对比指标（生态得分 / 振兴得分 / 协调度 / 森林率 / 收入 / GDP）")
    add_bullet(doc, "选择年份（2020—2024）")
    add_bullet(doc, "图表自动更新，按模式分色显示")
    add_paragraph(doc, "提供 6 类图表：")
    add_table_three_line(doc, [
        ["图表", "能看到什么"],
        ["横向柱状图", "当年 10 个区县按指标排名"],
        ["时间折线图", "5 年趋势变化，按模式分色"],
        ["雷达图", "5 种模式代表区县五维对比"],
        ["散点图", "生态得分 vs 振兴得分，离对角线越远越失调"],
        ["权重条形图", "26 项指标的重要性排序"],
        ["聚类散点图", "10 个区县按相似度自动分群"],
    ], caption="表 2-2  数据大屏图表")

    # ---- 2.5 农产品商城 ----
    add_heading(doc, "2.5 农产品商城", level=2)
    add_paragraph(doc, "生态农产品交易市场，商家可上架、用户可购买。")
    add_figure(doc, SHOTS / "05_mall.png", "2-5", "农产品商城界面")
    add_paragraph(doc, "操作说明：")
    add_bullet(doc, "左侧按分类筛选（果蔬 / 粮油 / 水产 / 食用菌 / 茶叶 / 畜禽 / 加工品）")
    add_bullet(doc, "顶部搜索框输入商品名")
    add_bullet(doc, '商品卡片点击"加入购物车"')
    add_bullet(doc, "右上角购物车图标可查看已选商品、改数量、删除")
    add_bullet(doc, '点击"结算"填写收货信息后提交订单')

    # ---- 2.6 案例中心 ----
    add_heading(doc, "2.6 案例中心", level=2)
    add_paragraph(doc, "5 种发展模式的典型案例展示，学习他人经验。")
    add_figure(doc, SHOTS / "06_case.png", "2-6", "案例中心界面")
    add_paragraph(doc, "操作说明：")
    add_bullet(doc, "顶部 5 个模式标签，点击切换案例列表")
    add_bullet(doc, "每个案例卡片展示图片、标题、地区、摘要")
    add_bullet(doc, '点击"查看详情"弹出图文详情、关键数据、经验启示')

    # ---- 2.7 用户中心 ----
    add_heading(doc, "2.7 用户中心", level=2)
    add_paragraph(doc, "管理个人账户与历史数据。")
    add_figure(doc, SHOTS / "07_user.png", "2-7", "用户中心界面")
    add_paragraph(doc, "操作说明：")
    add_bullet(doc, "未登录时显示登录 / 注册卡片，支持普通用户与商家两种角色")
    add_bullet(doc, "登录后显示个人面板：头像、用户名、角色、邮箱")
    add_bullet(doc, "商家角色可发布新商品（含分类、产地、价格、库存、图片、认证）")
    add_bullet(doc, "评估记录表格展示历史评估，可查看详情、下载 PDF")
    add_bullet(doc, "订单列表展示购买记录与状态")

    add_page_break(doc)

    # ============================================================
    # 第三章 五种发展模式
    # ============================================================
    add_chapter_title(doc, "第三章 五种发展模式")

    add_paragraph(doc,
        "平台通过数据分析，把 10 个样本区县自动归为 5 种发展模式。"
        "每种模式都有自己的特征和适合的发展方向。")

    add_table_three_line(doc, [
        ["模式", "代表区县", "怎么识别的", "适合干什么"],
        ["生态康养型", "黟县、蒲江", "森林多（≥65%）、城镇化低（≤55%）、空气好（≥80%）", "森林康养、气候疗养、康养小镇"],
        ["湿地水域型", "合肥、雄安", "水质好（≥95%）、生态保护区大", "湿地公园、保水渔业、碳汇交易"],
        ["农业品牌型", "盱眙、兴化", "粮田多（≥10万公顷）、产量高（≥90万吨）", "区域品牌、三品一标、精深加工"],
        ["农文旅融合型", "五指山、嘉定", "森林≥15%、空气好、文化丰富", "研学、文创、节庆、特色民宿"],
        ["城郊消费型", "高淳、溧水", "城镇化高（≥70%）、GDP 高（≥1000亿）", "都市农园、采摘、城郊综合体"],
    ], caption="表 3-1  五种发展模式识别与发展方向")

    add_paragraph(doc, "每种模式都配有 5—6 条具体建议：")
    add_table_three_line(doc, [
        ["模式", "建议数", "举例"],
        ["生态康养型", "6 条", "森林康养基地、气候疗养产品、康养小镇品牌"],
        ["湿地水域型", "5 条", "湿地公园、保水渔业、水权交易、碳汇交易"],
        ["农业品牌型", "6 条", "区域公用品牌、三品一标、精深加工、电商直播"],
        ["农文旅融合型", "5 条", "研学线路、文创工坊、乡村节庆、特色民宿"],
        ["城郊消费型", "5 条", "都市农园、采摘体验、城郊综合体、周末经济"],
    ], caption="表 3-2  路径优化建议")

    add_page_break(doc)

    # ============================================================
    # 第四章 操作流程
    # ============================================================
    add_chapter_title(doc, "第四章 操作流程")

    add_heading(doc, "4.1 完整评估流程", level=2)
    add_paragraph(doc, "从打开平台到拿到报告，完整步骤如下：")
    steps = [
        "打开浏览器，访问平台首页。",
        '点击导航栏"智能分析"进入分析中心。',
        '在左侧输入区填写地区名称、评估年份。',
        "填写 11 项生态产品价值实现指标数据。",
        "填写 15 项乡村振兴水平指标数据。",
        '（可选）点击"加载模板"一键填充示例数据。',
        '点击"开始评估"按钮，等待约 3 秒。',
        "右侧自动展示综合得分、协调度、模式判定、障碍因子、建议等全部结果。",
        "查看雷达图了解各维度强弱项。",
        "查看障碍因子图了解最大短板。",
        '阅读 AI 生成的综合路径优化建议。',
        '点击"下载 PDF"按钮，保存完整评估报告。',
    ]
    for i, step in enumerate(steps, 1):
        add_paragraph(doc, f"第 {i} 步：{step}", first_line_indent=True)

    add_heading(doc, "4.2 商城购买流程", level=2)
    mall_steps = [
        '点击导航栏"农产品商城"进入商城。',
        "左侧选择商品分类或搜索商品名。",
        "浏览商品卡片，查看价格、产地、认证信息。",
        '点击"加入购物车"。',
        "右上角购物车图标查看已选商品。",
        "调整数量或移除商品。",
        '点击"结算"。',
        "填写收货信息，提交订单。",
        "订单创建成功，库存自动扣减。",
        '在用户中心"我的订单"查看订单状态。',
    ]
    for i, step in enumerate(mall_steps, 1):
        add_paragraph(doc, f"第 {i} 步：{step}", first_line_indent=True)

    add_heading(doc, "4.3 商家上架商品流程", level=2)
    merchant_steps = [
        '注册账号时选择"商家"角色。',
        "登录后进入用户中心。",
        '点击"发布商品"按钮。',
        "填写商品名称、分类、产地、价格、库存。",
        "填写商品图片 URL。",
        "选择生态认证类型（有机 / 绿色 / 地理标志 / 无公害）。",
        "填写商品描述。",
        '点击"发布"提交。',
        "商品进入待审核状态。",
        "审核通过后在商城上架展示。",
    ]
    for i, step in enumerate(merchant_steps, 1):
        add_paragraph(doc, f"第 {i} 步：{step}", first_line_indent=True)

    add_page_break(doc)

    # ============================================================
    # 第五章 协调度等级说明
    # ============================================================
    add_chapter_title(doc, "第五章 协调度等级说明")

    add_paragraph(doc,
        "协调度 D 值在 0 到 1 之间，分 10 个等级。D 值越高，说明生态与振兴越协调。"
        "下表帮助理解自己地区的 D 值含义：")

    add_table_three_line(doc, [
        ["D 值", "等级", "说明"],
        ["0.0—0.1", "极度失调", "生态与振兴严重失衡，亟需干预"],
        ["0.1—0.2", "严重失调", "失衡明显"],
        ["0.2—0.3", "中度失调", "失衡，需重点改进"],
        ["0.3—0.4", "轻度失调", "轻度失衡"],
        ["0.4—0.5", "濒临失调", "接近失调边缘"],
        ["0.5—0.6", "勉强协调", "初步协调，基础薄弱"],
        ["0.6—0.7", "初级协调", "协调水平较低"],
        ["0.7—0.8", "中级协调", "协调水平中等"],
        ["0.8—0.9", "良好协调", "协调水平较好"],
        ["0.9—1.0", "优质协调", "高度协同发展"],
    ], caption="表 5-1  协调度 10 级划分")

    add_page_break(doc)

    # ============================================================
    # 第六章 接口与启动
    # ============================================================
    add_chapter_title(doc, "第六章 接口与启动")

    add_heading(doc, "6.1 后台接口一览", level=2)
    add_paragraph(doc, "平台后台提供以下接口供前端调用：")
    add_table_three_line(doc, [
        ["接口", "方法", "功能"],
        ["/auth/register", "POST", "用户注册"],
        ["/auth/login", "POST", "用户登录"],
        ["/auth/me", "GET", "查看当前用户"],
        ["/policy/list", "GET", "政策列表"],
        ["/analysis/evaluate", "POST", "提交评估"],
        ["/analysis/{id}/report", "GET", "下载 PDF"],
        ["/dashboard/compare", "GET", "大屏对比数据"],
        ["/mall/products", "GET", "商品列表"],
        ["/mall/orders", "POST", "提交订单"],
        ["/case/list", "GET", "案例列表"],
    ], caption="表 6-1  主要接口")

    add_heading(doc, "6.2 如何启动平台", level=2)
    add_paragraph(doc, "后台启动：")
    add_paragraph(doc, "cd backend", first_line_indent=False)
    add_paragraph(doc, "pip install -r requirements.txt", first_line_indent=False)
    add_paragraph(doc, "python run.py", first_line_indent=False)
    add_paragraph(doc, "地址：http://localhost:8000")
    add_paragraph(doc, "前台启动：")
    add_paragraph(doc, "cd frontend", first_line_indent=False)
    add_paragraph(doc, "npm install", first_line_indent=False)
    add_paragraph(doc, "npm run dev", first_line_indent=False)
    add_paragraph(doc, "地址：http://localhost:5173")

    add_page_break(doc)

    # ============================================================
    # 附录 指标体系
    # ============================================================
    add_chapter_title(doc, "附录  指标体系")

    add_heading(doc, "附.1 生态产品价值实现指标（11 项）", level=2)
    add_table_three_line(doc, [
        ["类别", "指标", "单位", "权重"],
        ["生态效益", "森林覆盖率", "%", "0.2857"],
        ["生态效益", "空气质量优良率", "%", "0.1429"],
        ["生态效益", "水质达标率", "%", "0.1429"],
        ["经济效益", "地区生产总值", "万元", "0.2676"],
        ["经济效益", "生态产业增加值", "万元", "0.1850"],
        ["经济效益", "生态补偿金额", "万元", "0.0866"],
        ["社会效益", "生态就业人数", "人", "0.0303"],
        ["社会效益", "公众满意度", "分", "0.0303"],
        ["社会效益", "生态产品认知度", "%", "0.0152"],
        ["社会效益", "参与生态保护人次", "人次", "0.0114"],
        ["社会效益", "生态培训覆盖", "人次", "0.0021"],
    ], caption="表 附-1  生态产品价值实现指标")

    add_heading(doc, "附.2 乡村振兴指标（15 项）", level=2)
    add_table_three_line(doc, [
        ["类别", "指标", "单位", "权重"],
        ["产业兴旺", "粮食播种面积", "公顷", "0.0978"],
        ["产业兴旺", "农产品产量", "吨", "0.0512"],
        ["产业兴旺", "农业机械化率", "%", "0.0236"],
        ["生态宜居", "农村绿化率", "%", "0.0386"],
        ["生态宜居", "生活垃圾处理率", "%", "0.0159"],
        ["生态宜居", "污水处理率", "%", "0.0124"],
        ["乡风文明", "文化设施覆盖率", "%", "0.0186"],
        ["乡风文明", "文明村镇占比", "%", "0.0074"],
        ["治理有效", "村民自治率", "%", "0.0164"],
        ["治理有效", "网格化管理覆盖率", "%", "0.0065"],
        ["生活富裕", "农村人均可支配收入", "元", "0.3528"],
        ["生活富裕", "城乡居民收入比", "—", "0.1494"],
        ["生活富裕", "恩格尔系数", "—", "0.0633"],
        ["生活富裕", "互联网普及率", "%", "0.0268"],
        ["生活富裕", "每千人医疗床位数", "张", "0.0113"],
    ], caption="表 附-2  乡村振兴指标")

    # === 保存 ===
    doc.save(str(OUTPUT))
    print(f"✅ Word 文档已生成：{OUTPUT}")
    print(f"   文件大小：{OUTPUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build_document()
