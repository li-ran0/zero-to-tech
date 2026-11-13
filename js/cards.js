// 从 npm 依赖里按包名导入，Vite 会解析 node_modules 并打包进构建产物。
// 不再依赖 CDN，也不用维护 js/vendor 里的副本。
import { animate, stagger } from "animejs";

export function initCardsAnim() {
  animate(".card", {
    opacity: [0, 1],
    translateY: [24, 0],
    delay: stagger(120),
    duration: 700,
    ease: "outBack",
  });
}