# 康康 · 心理考研答题工作台

为财务管理跨考深圳大学应用心理研究生、正在二战的康康，整理手写答卷、专业批改与复习建议。

**当前阶段：手写转写待核对，尚未发布正式判题报告。**

- [打开核对页面](https://bergpss.github.io/kangkang-psych-exam/)
- [阅读转写 Markdown](transcripts/2026-11-05.md)
- [查看原始 PDF](docs/assets/2026-11-05-original.pdf)
- [AI Agent 接手入口](AGENTS.md)

## 康康如何核对

打开页面 → 切换两道题 → 对照原稿 → 勾选准确段落或填写修改 → 导出核对意见并发回。

网页只在当前浏览器保存核对进度，不会自动上传反馈。换设备前请导出。完整题干和红笔批注作者仍待补充。

## 内容结构

| 路径 | 用途 |
| --- | --- |
| `context/` | 用户提供的备考背景、项目目标、当前状态 |
| `transcripts/2026-11-05.json` | 唯一结构化转写源，保留不确定性 |
| `transcripts/2026-11-05.md` | 由JSON生成的人类可读转写 |
| `docs/` | GitHub Pages静态网页和原稿 |
| `reviews/` | 后续判题报告与统一模板 |
| `AGENTS.md` | 其他AI模型接手和独立审阅的流程 |
| `scripts/build.py` | 从JSON生成页面与Markdown |

## 本地更新

仅需Python 3，无第三方依赖：

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory docs
```

访问 http://localhost:8000 。修改转写请编辑JSON；修改页面请编辑 `scripts/page.html`、`docs/style.css`、`docs/app.js`。构建后提交生成内容。

GitHub Pages从main分支的 `/docs` 发布，使用 `.nojekyll`。内容以学习核对为目的；原稿、转写与AI建议严格区分，不提供虚构的官方评分。
