# 绿脉兴农 — 生态产品价值实现赋能乡村振兴一体化智能系统

> 中国研究生乡村振兴科技强农+创新大赛参赛作品
> 南京师范大学"三色绘三农"乡村振兴实践团队

## 项目结构

```
greenpulse/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── main.py          # FastAPI 入口
│   │   ├── config.py        # 配置（.env 读取）
│   │   ├── database.py      # SQLAlchemy + SQLite
│   │   ├── models/          # 用户/政策/商品/订单/案例/评估
│   │   ├── api/             # 5 个路由：auth/policy/analysis/mall/case
│   │   ├── core/            # 核心算法：indicators/ccd_model/obstacle/ai_advisor
│   │   ├── pdf/             # reportlab 报告生成
│   │   └── data/            # 初始化数据（待补）
│   ├── uploads/             # 上传文件 + 生成的 PDF
│   ├── requirements.txt
│   ├── .env                 # 配置文件
│   └── run.py               # 启动脚本
├── frontend/                # Vue3 前端
│   ├── src/
│   │   ├── main.js          # 入口（注册 Element Plus、Pinia、Router）
│   │   ├── App.vue
│   │   ├── router/          # 路由
│   │   ├── api/             # axios 封装
│   │   ├── layouts/         # 主布局
│   │   ├── views/           # 6 个页面：Home/Policy/Analysis/Mall/Case/User
│   │   └── assets/main.css
│   └── vite.config.js       # 含 /api 代理到后端 8000
└── docs/                    # 项目文档
```

## 快速启动

### 1. 后端（FastAPI）

```bash
cd greenpulse/backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
python run.py                  # 默认 http://localhost:8000
```

后端启动后：
- API 文档：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

### 2. 前端（Vue3 + Vite）

```bash
cd greenpulse/frontend
npm install                    # 已完成
npm run dev                    # 默认 http://localhost:5173
```

### 3. DeepSeek API（可选，用于 AI 智能建议）

```bash
# 编辑 backend/.env
DEEPSEEK_API_KEY=sk-your-key-here
```

未配置时使用规则版建议兜底，仍可完整演示。

## 核心功能

| 功能 | 状态 | 说明 |
|---|---|---|
| 首页（三色融合） | ✅ 骨架 | "党建红+产业金+生态绿"理论展示 |
| 政策中心 | ✅ 骨架 | 按主题/级别/关键词检索 |
| 智能分析中心 | ✅ 骨架 | 4 模型评估 + AI 模式识别 + PDF 报告 |
| 农产品商城 | ✅ 骨架 | 商品列表 + 加入购物车（订单流程待完善） |
| 案例中心 | ✅ 骨架 | 5 种模式案例展示 |
| 用户中心 | ✅ 骨架 | 注册/登录/JWT + 评估历史 |

## 评估模型

### 1. 生态产品价值实现成效评价
9 项指标，分生态/经济/社会 3 个子系统，加权综合评分。

### 2. 乡村振兴水平评价
18 项指标，按产业兴旺/生态宜居/乡风文明/治理有效/生活富裕 5 维度评分。

### 3. 耦合协调度（CCD 模型）
```
C = 2·√(U1·U2) / (U1 + U2)
T = α·U1 + β·U2  (α=β=0.5)
D = √(C·T)
```
协调等级分 10 档（极度失调 → 优质协调）。

### 4. 障碍度模型
基于指标偏离度 × 权重，取 Top N 障碍因子。

### 5. AI 模式识别（5 种模式）
- 生态康养型
- 湿地水域型
- 农业品牌型
- 农文旅融合型
- 城郊消费型

规则兜底 + DeepSeek 大模型生成 500-800 字差异化路径建议。

## 待办（按优先级）

- [ ] 填充初始数据：25 条政策、5 个案例、10 个农产品
- [ ] 调通 DeepSeek API（用户拿到 Key 后）
- [ ] 完善商城订单流程与购物车
- [ ] 校赛演示视频录制
- [ ] 接入团队真实权重表与指标阈值

## 技术栈

| 层 | 选型 |
|---|---|
| 前端 | Vue3 + Element Plus + Vite + Pinia + Vue Router + ECharts |
| 后端 | Python FastAPI + SQLAlchemy + Pydantic |
| 数据库 | SQLite（校赛）→ MySQL（国赛） |
| AI | DeepSeek API（OpenAI 兼容） |
| PDF | reportlab |
| 鉴权 | JWT (python-jose + passlib) |
