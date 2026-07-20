# 绿脉兴农 · 部署指南

本文档介绍如何将项目部署到 **Vercel（前端）+ Railway（后端+数据库）**，全程免费，约 30 分钟完成。

---

## 架构总览

```
┌─────────────────┐         ┌─────────────────────────┐
│   Vercel        │  HTTPS  │   Railway                │
│   前端 SPA      │ ──────> │   FastAPI 后端           │
│   green-pulse   │         │   + PostgreSQL 数据库    │
│   .vercel.app   │ <────── │   .up.railway.app       │
└─────────────────┘         └─────────────────────────┘
       │                              │
       │ 静态资源 CDN                  │ 持久化数据
       │                              │
       ▼                              ▼
   自动 HTTPS                    Railway Volume
```

| 服务 | 用途 | 费用 |
|---|---|---|
| Vercel | 前端 SPA 静态托管 | 免费 |
| Railway | 后端容器 + PostgreSQL | 免费 500 小时/月 |
| Unsplash CDN | 商品/案例图片 | 免费 |
| DeepSeek API | AI 智能分析 | 用户自备 Key |

---

## 准备工作

### 1. 注册账号（都要 GitHub 登录）

- **GitHub**：https://github.com/ （如果还没注册）
- **Vercel**：https://vercel.com/
- **Railway**：https://railway.app/
- **GitHub 仓库**：把项目推到 GitHub（公开或私有都行）

### 2. 把代码推到 GitHub

```bash
cd "g:/汪戈/科技强农竞赛/greenpulse"

# 初始化 git（如果还没初始化）
git init
git add .
git commit -m "Initial commit: 绿脉兴农参赛版"

# 在 GitHub 创建仓库后，关联并推送
git remote add origin https://github.com/你的用户名/greenpulse.git
git branch -M main
git push -u origin main
```

> ⚠ 注意：`.env` 文件已经在 `.gitignore` 里，**不会**被推到 GitHub，DeepSeek API Key 安全。

---

## 第一部分：部署后端到 Railway

### 步骤 1：创建 Railway 项目

1. 打开 https://railway.app/new
2. 选择 **Deploy from GitHub repo**
3. 选择你刚推送的 `greenpulse` 仓库
4. **Root Directory 设置为 `backend`**（重要！）
   - 进入 Settings → General → Root Directory
   - 填入 `backend`
   - 保存

### 步骤 2：添加 PostgreSQL 数据库

1. 在 Railway 项目页面点 **New → Database → Add PostgreSQL**
2. Railway 会自动创建一个数据库，并给你连接字符串
3. 在数据库的 **Connect** 标签下，找到 **Postgres Connection URL**
   - 形如：`postgresql://postgres:password@host:port/railway`

### 步骤 3：配置后端环境变量

进入后端服务的 **Variables** 标签，添加以下环境变量：

| 变量名 | 值 | 说明 |
|---|---|---|
| `DATABASE_URL` | `postgresql://...` | 从上一步的 PostgreSQL 服务复制（必填）|
| `SECRET_KEY` | 随便填一个长字符串 | JWT 加密用，例如 `my-super-secret-2024` |
| `DEEPSEEK_API_KEY` | `sk-ee246c8...` | 你的 DeepSeek API Key |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com/v1` | DeepSeek API 地址 |
| `DEEPSEEK_MODEL` | `deepseek-chat` | 模型名 |
| `CORS_ORIGINS` | `*` | 跨域（演示用 `*`，生产建议填具体域名） |

> 提示：Railway 会自动注入 `PORT` 环境变量，不用手动设置。

### 步骤 4：等待部署

Railway 会自动检测 `requirements.txt` 和 `Procfile`，安装依赖并启动：
- 安装命令：`pip install -r requirements.txt`
- 启动命令（来自 Procfile）：`gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
- 部署前会自动运行：`python seed_data.py`（初始化25条政策、5个案例、10个商品）

### 步骤 5：获取后端公网地址

部署完成后，Railway 会给你一个公网地址，形如：
```
https://greenpulse-backend-production.up.railway.app
```

**测试访问**：在浏览器打开上面的地址，应该看到：
```json
{
  "app": "绿脉兴农",
  "version": "0.1.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

再访问 `/health` 应该返回 `{"status":"ok"}`。

---

## 第二部分：部署前端到 Vercel

### 步骤 1：创建 Vercel 项目

1. 打开 https://vercel.com/new
2. 选择你刚推送的 GitHub 仓库
3. **配置项目**：
   - **Framework Preset**：Vue
   - **Root Directory**：`frontend`（重要！）
   - **Build Command**：`npm run build`（默认即可）
   - **Output Directory**：`dist`（默认即可）
   - **Install Command**：`npm install`（默认即可）

### 步骤 2：添加环境变量

在 **Environment Variables** 区域，添加：

| 名称 | 值 |
|---|---|
| `VITE_API_BASE` | `https://你的后端地址.up.railway.app/api` |

例如：
```
VITE_API_BASE=https://greenpulse-backend-production.up.railway.app/api
```

> ⚠ 注意：URL 后面要带 `/api`，不要带末尾的 `/`

### 步骤 3：部署

点 **Deploy**，等 1-2 分钟构建完成。

Vercel 会给你一个公网地址，形如：
```
https://green-pulse.vercel.app
```

### 步骤 4：测试访问

打开 Vercel 给的地址，应该看到完整的绿脉兴农系统。

**测试清单**：
- [ ] 首页能正常显示
- [ ] 政策页能显示25条政策
- [ ] 案例页能显示5个案例（图片能加载）
- [ ] 商城页能显示10个商品（图片能加载）
- [ ] 用户页能注册新账号
- [ ] 登录后能下单
- [ ] 智能分析页能提交评估（10-15秒等AI响应）

---

## 常见问题

### Q1: 后端部署失败，提示找不到模块

**原因**：Root Directory 没设置对。

**解决**：进入 Railway → 后端服务 → Settings → General → Root Directory → 填 `backend` → 保存。

### Q2: 前端访问后端报 CORS 错误

**解决**：确保后端环境变量 `CORS_ORIGINS` 设置为 `*`（演示期）或具体的 Vercel 域名。

### Q3: 商品图片不显示

**解决**：图片用的是 Unsplash 公网链接，应该正常。如果个别图片 404，运行：
```bash
cd backend
python fix_images.py
```

### Q4: DeepSeek API 不响应

**原因**：
1. API Key 失效 → 重新申请
2. 余额不足 → 充值
3. 网络问题 → 检查 Railway 后端日志

### Q5: 数据库数据丢失

**原因**：Railway 免费层重启容器时 SQLite 会丢失。

**解决**：必须用 PostgreSQL（Railway 自带），通过 `DATABASE_URL` 环境变量配置。`seed_data.py` 会在每次部署时自动初始化数据。

### Q6: Vercel 路由 404

**原因**：Vue Router 的 history 模式需要 SPA fallback。

**解决**：`frontend/vercel.json` 已经配置好了 rewrites 规则，所有路径都会回到 `index.html`。

---

## 演示用账号

数据库初始化后会自动创建商户账号：

| 用户名 | 密码 | 角色 |
|---|---|---|
| `merchant001` | `123456` | 商家 |

也可以自己注册新账号。

---

## 后续运维

### 更新代码

```bash
git add .
git commit -m "update: ..."
git push
```

推送到 GitHub 后：
- Vercel 自动重新构建前端（1-2分钟）
- Railway 自动重新部署后端（2-3分钟）

### 查看日志

- **Vercel**：项目页面 → Deployments → 点击最新部署 → Logs
- **Railway**：项目页面 → 后端服务 → Deployments → 点击最新部署 → Logs

### 自定义域名（可选）

- **Vercel**：项目 → Settings → Domains → 添加自己的域名
- **Railway**：后端服务 → Settings → Networking → Generate Domain

国内域名需要备案。如果只是参赛演示，用 `xxx.vercel.app` 子域名就够了。

---

## 费用说明

| 服务 | 免费额度 | 超出后 |
|---|---|---|
| Vercel Hobby | 100GB 流量/月 | 需升级 Pro $20/月 |
| Railway Trial | $5 试用额度 | $5 后需充值 |
| DeepSeek API | 注册送 ¥10 | 按调用付费 |

参赛期间完全够用。如果演示当天访问量较大，建议提前 1 小时测试，避免免费额度耗尽。
