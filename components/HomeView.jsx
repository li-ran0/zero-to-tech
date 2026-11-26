"use client";

// 个人主页。这一节把它从"纯展示"改成了"会去后端取数据"。
// 打开页面时先用 site.js 的 home 打底，再用 useEffect 去 GET /api/profile，
// 拿到后端数据后 setData 更新界面。因为要在浏览器里发请求，所以顶上写了 "use client"。
// 请求失败时（比如后端没跑、跨源被拦）就保持打底数据、把错误打到控制台，页面不至于崩。
// 后端地址从 .env.local 的 NEXT_PUBLIC_API_BASE_URL 读（编译期内联，改了要重启 dev server）。
import { useEffect, useState } from "react";
import Link from "next/link";
import Nav from "./Nav.jsx";
import PageHeading from "./PageHeading.jsx";
import AnimatedCardGrid from "./AnimatedCardGrid.jsx";
import { home } from "../data/site.js";
const API = process.env.NEXT_PUBLIC_API_BASE_URL;


export default function HomeView() {
  const [data, setData] = useState(home);

  useEffect(() => {
    async function loadProfile() {
      try {
        // 兜底：变量名写错 / 忘了建 .env.local / 改了没重启，都会让 API 变成 undefined，
        // 然后被拼成 "undefined/api/profile" 这种相对路径，最后报一个莫名其妙的 404。
        // 在这里先拦一道，错误信息才说得清。
        // 用 === undefined 而不是 !API：部署时该变量会是空字符串（走同源相对路径），
        // 空字符串属于合法配置，不能误判成"未配置"。
        if (API === undefined) {
          throw new Error("NEXT_PUBLIC_API_BASE_URL 未配置：检查 .env.local 是否写了该变量，改完要重启 dev server 或重新 build");
        }

        const res = await fetch(`${API}/api/profile`);
        if (!res.ok) {
          throw new Error(`主页数据加载失败：${res.status}`);
        }
        setData(await res.json());
      } catch (error) {
        console.error(error);
      }
    }

    loadProfile();
  }, []);

  return (
    <AnimatedCardGrid className="dashboard-grid">
      <article className="hero-stage panel-full">
        <Nav />
        <PageHeading title={data.heroTitle} subtitle={data.heroSubtitle} />
      </article>

      <article className="panel panel-full featured-work-panel card">
        <p className="section-kicker">{data.featuredWork.kicker}</p>
        <p className="featured-title">{data.featuredWork.title}</p>
        <p className="featured-copy">{data.featuredWork.copy}</p>
        <Link className="featured-link" href="/text-lab">
          <span className="featured-link-label">{data.featuredWork.linkLabel}</span>
          <span className="arrow">›</span>
        </Link>
      </article>

      <article className="panel panel-full identity-panel card">
        <div className="identity-item">
          <p className="section-kicker">座右铭</p>
          <p className="identity-value identity-quote">{data.identity.motto}</p>
        </div>
        <div className="identity-item">
          <p className="section-kicker">正在学习</p>
          <p className="identity-value">{data.identity.learning}</p>
        </div>
      </article>
    </AnimatedCardGrid>
  );
}
