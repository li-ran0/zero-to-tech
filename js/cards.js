// 用本地文件，不再从 jsdelivr 下载。
// 之前从 CDN 顶层 import：网络稍差（国内访问 jsdelivr 常要 20 秒以上甚至超时）
// 整个 main.js 都跑不起来，卡片会一直停在 opacity: 0。
import { animate, stagger } from "./vendor/anime.esm.min.js";

export function initCardsAnim() {
  animate(".card", {
    opacity: [0, 1],
    translateY: [24, 0],
    delay: stagger(120),
    duration: 700,
    ease: "outBack",
  });
}