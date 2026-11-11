# Zero to Tech

一个纯静态的入门网页项目，用来练习 HTML、CSS 和 JavaScript 三件套的配合。

页面是一张居中的卡片：标题、一段说明文字，以及一个按钮。点击按钮后，JavaScript 会改写段落内容。

## 技术栈

- HTML5
- CSS3（Flexbox 布局）
- 原生 JavaScript（无框架）
- 无构建工具、无第三方依赖

## 项目结构

```
zero-to-tech/
├── index.html   # 页面结构
├── style.css    # 页面样式
├── script.js    # 按钮点击交互
├── README.md
└── .gitignore
```

## 运行

不需要安装任何东西，任选一种方式：

**方式一：直接打开**

双击 `index.html`，用浏览器打开即可。

**方式二：本地静态服务器**

```bash
# Python 3
python -m http.server 8000
```

然后访问 <http://localhost:8000>。

## 页面做了什么

| 元素 | 作用 | 相关文件 |
| --- | --- | --- |
| `body` | 用 Flexbox 把卡片在视口中水平垂直居中 | `style.css` |
| `.card` | 白色圆角卡片，带阴影和 40px 内边距 | `style.css` |
| `#msg` | 说明段落，也是脚本改写的目标 | `index.html` |
| `changeText()` | 把 `#msg` 的文字替换成「你刚刚触发了一段 JavaScript。」 | `script.js` |

## 修改建议

- 改标题：`index.html` 里的 `<h1>`。
- 改按钮文案或点击效果：`index.html` 的 `<button>` 与 `script.js` 的 `changeText()`。
- 改配色：`style.css` 中 `body` 的背景色和 `button` 的 `#3498db` / `#2980b9`。
- 按钮目前在 HTML 里用 `onclick` 绑定事件，后续可以改成 `addEventListener`，把行为与结构分开。

## 浏览器支持

使用了 Flexbox 和 `textContent`，所有现代浏览器均可正常运行。
