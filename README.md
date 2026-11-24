# zero-to-tech

个人主页 + 文字实验室。前端 Next.js 15（App Router，静态导出），后端 FastAPI。

「文字实验室」把一句中文拆成两样东西：带声调的**拼音**，以及基于朴素贝叶斯的情感**得分**（0–1）。每次分析的结果按浏览器会话隔离存进 SQLite，点结果卡上的「历史记录」随时回看。

## 功能

- **首页 `/`** —— 个人简介与精选作品；先用 `data/site.js` 的文案渲染，后端可用时由 `GET /api/profile` 覆盖
- **文字实验室 `/text-lab`** —— 输入文本 → 拼音 + 情感得分与标签（偏积极 / 中性 / 偏消极）
- **历史记录** —— 用 cookie 里的会话 ID 隔离，只回本人最近 10 条
- 响应式布局、卡片入场动画（anime.js）

## 技术栈

| 层 | 选型 |
| --- | --- |
| 前端 | Next.js 15 (App Router) · React 19 · anime.js · 原生 CSS |
| 后端 | FastAPI · Uvicorn · pypinyin · snownlp |
| 存储 | SQLite（`backend/history.db`，运行时自动生成） |
| 配置 | python-dotenv（后端）· `NEXT_PUBLIC_*` 环境变量（前端） |

## 目录结构

```
app/                       ← 文件夹 = 路由
  layout.jsx               ← 全站外壳，统一 import 8 个 css
  page.jsx                 ← /          → <HomeView />
  text-lab/page.jsx        ← /text-lab  → <TextLabView />
components/                ← 页面与卡片组件（客户端组件都带 "use client"）
  Nav.jsx                  ← 导航（<Link> + usePathname）
  HomeView.jsx             ← 首页
  TextLabView.jsx          ← 文字实验室页
  PageHeading.jsx          ← 标题 + 副标题
  InputCard.jsx            ← 输入卡，POST /api/analyze
  ResultCard.jsx           ← 结果卡：拼音、得分、标签
  HistoryModal.jsx         ← 历史记录弹窗，GET /api/history
  AnimatedCardGrid.jsx     ← 卡片入场动画
css/                       ← 8 个 css，顺序在 layout.jsx 里固定
data/site.js               ← 全站文案数据（改文案只动这里）
backend/
  main.py                  ← FastAPI 应用：接口、CORS、会话 cookie
  storage.py               ← SQLite 建表 / 迁移 / 读写
  handmade.py              ← 最早用标准库 http.server 手写的版，仅作对照
  requirements.txt         ← Python 依赖（锁定版本）
  .env.example             ← 后端环境变量模板
next.config.mjs            ← output: 'export'（静态导出）
.env.example               ← 前端环境变量模板
requirements.txt           ← 与 backend/requirements.txt 内容相同的副本（UTF-8）
```

## 快速开始

前置：Node.js `^20.19.0 || >=22.12.0`（见 `package.json` 的 `engines`），Python 3.10+。

### 1. 前端

```bash
npm install
cp .env.example .env.local     # Windows PowerShell: Copy-Item .env.example .env.local
npm run dev                    # http://localhost:3000
```

`.env.example` 默认指向 `http://localhost:8000`；后端换了地址或端口记得同步修改。

### 2. 后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # 按需修改 ALLOWED_ORIGINS
fastapi dev --host :: --port 8000
# 或：uvicorn main:app --reload --host :: --port 8000
```

`--host ::` 是有意为之：前端在 `localhost:3000`，接口也必须走 `localhost:8000`，浏览器才认为两者同站，`session_id` cookie 才会被带上。默认只绑 IPv4 的 `127.0.0.1` 可能导致浏览器访问 `localhost` 连不上；如果想统一用 `127.0.0.1`，前端和后端要一起换，别混用。

## 环境变量

| 变量 | 文件 | 说明 |
| --- | --- | --- |
| `NEXT_PUBLIC_API_BASE_URL` | 根目录 `.env.local` | 后端地址。**编译期内联**，改完必须重启 dev server 或重新 build |
| `ALLOWED_ORIGINS` | `backend/.env` | CORS 白名单，英文逗号分隔；缺省 `http://localhost:3000,http://127.0.0.1:3000` |

`.env*` 均被 `.gitignore` 忽略，只有 `.env.example` 入库。

## 接口

Base URL 默认 `http://localhost:8000`。CORS 只放行 `ALLOWED_ORIGINS` 中的来源，允许方法为 `GET` / `POST`，并允许携带凭证（cookie）。

### `GET /api/profile`

返回首页文案：

```json
{
  "heroTitle": "关于我",
  "heroSubtitle": "项目，创意，灵感，心得，我的作品",
  "featuredWork": { "kicker": "作品", "title": "文字实验室", "copy": "拼音和情绪，挖掘中文里的细节", "linkLabel": "打开作品" },
  "identity": { "motto": "已识乾坤大，尤怜草木青", "learning": "零到全栈" }
}
```

### `POST /api/analyze`

请求体 `{"text": "今天心情不错"}`，响应示例：

```json
{
  "text": "今天心情不错",
  "score": 0.86,
  "label": "偏积极",
  "pinyin": "jīn tiān xīn qíng bù cuò",
  "created_at": "2026-11-24T13:21:16+00:00"
}
```

首次请求会通过 `Set-Cookie` 下发 `session_id`（HttpOnly、SameSite=Lax、30 天），之后的请求由浏览器自动带上。

### `GET /api/history?limit=10`

只返回当前 cookie 对应会话的记录，按 `created_at` 倒序，`limit` 默认 10：

```json
[
  {
    "id": 17,
    "text": "今天心情不错",
    "score": 0.86,
    "label": "偏积极",
    "pinyin": "jīn tiān xīn qíng bù cuò",
    "created_at": "2026-11-24T13:21:16+00:00",
    "session_id": "10d298fd666f49868d91ecf759024b69"
  }
]
```

没有记录时返回 `[]`；首次访问也会下发 `session_id` cookie。

## 数据与隐私

- 会话隔离靠 cookie 中的随机 `session_id`，没有账号体系；换浏览器或清 cookie 就是新会话
- 记录存在 `backend/history.db`（SQLite，已 gitignore）；`storage.py` 启动时自动建表，并给老库补 `session_id` 列
- 情感得分来自 SnowNLP 的通用语料模型，仅供娱乐参考，不构成严谨情感分析

## 构建与部署

前端是纯静态导出（`next.config.mjs` 中 `output: 'export'`）：

```bash
npm run build        # 产物在 out/
```

**注意**：`output: 'export'` 下 `next start` 不可用，需要用任意静态服务器托管 `out/`：

```bash
npx serve out        # serve 默认开启 clean URLs，/text-lab 会映射到 text-lab.html
```

用 nginx 托管时记得补上无扩展名映射，否则 `/text-lab` 会 404：

```nginx
location / {
    try_files $uri $uri.html $uri/ =404;
}
```

上线前检查：

1. 把 `NEXT_PUBLIC_API_BASE_URL` 指向线上后端，**然后重新 build**（值会被写死进静态文件）
2. 把 `backend/.env` 的 `ALLOWED_ORIGINS` 改成前端真实 origin（协议 + 域名 + 端口，不带路径）
3. 后端用 uvicorn 常驻，例如：
   `nohup uvicorn main:app --host 0.0.0.0 --port 8000 > ~/uvicorn.log 2>&1 &`

## 设计说明

- **数据与界面分离**：可展示的文案集中在 `data/site.js`，组件里不写死文案
- **两套后端**：`handmade.py` 是最早用标准库手写的 `/api/profile` 服务，保留下来做对照；实际使用的是 `main.py`
- 历史记录从本地 `history.json` 演进到 SQLite，再演进到按会话隔离，schema 变更由 `storage.py` 做兼容迁移
- 前端最早是 Vite + 手写路由（`useRoute`），现迁移到 App Router：文件夹即路由，`app/layout.jsx` 承接原 `App.jsx` 的外壳

## License

ISC（见 `package.json`）。
