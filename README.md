# zero-to-tech · Next.js 版

个人主页 + 文字实验室，使用 Next.js App Router。网站长相与之前的 React 版一致；路由层从手写的 `useRoute` 换成了「文件夹 = 路由」，入口从 `index.html` + `main.jsx` + `App.jsx` 换成了 `app/`。

## 跑起来

```bash
npm install
npm run dev          # http://localhost:3000   （Next 默认端口是 3000）
```

另一个终端跑后端：

```bash
cd backend
.venv\Scripts\fastapi dev --host ::
```

<!-- --host :: 是必须的：接口要走 localhost:8000 才能和前端的 localhost:3000 同站，
     浏览器的 session cookie 才会被带上。理由见 .env.local 里的注释。 -->


生产构建：

```bash
npm run build
npm start
```

## 项目结构

```
app/                     ← 文件夹 = 路由
  layout.jsx             ← 全站外壳（页面包裹 + import 8 个 css）
  page.jsx               ← /         → 渲染 <HomeView />
  text-lab/page.jsx      ← /text-lab → 渲染 <TextLabView />
components/
  Nav.jsx                ← <Link> + usePathname（"use client"）
  HomeView.jsx           ← 首页
  TextLabView.jsx        ← 文字实验室页
  PageHeading.jsx        ← 标题 + 副标题
  InputCard.jsx          ← 输入卡（"use client"）
  ResultCard.jsx         ← 结果卡（"use client"）
  AnimatedCardGrid.jsx   ← 卡片入场动画（"use client"）
css/                     ← 8 个 css
data/site.js             ← 全站文案数据
next.config.mjs          ← 空 {}
```

相比 Vite 版，没了 `index.html`、`src/main.jsx`、`src/App.jsx`、`src/router/useRoute.js`——这一坨被 `app/` 取代了。
