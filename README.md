# 康康 · 心理考研答题工作台

为财务管理跨考深圳大学应用心理研究生、正在二战的康康，整理手写答卷、专业批改与复习建议。

**当前阶段：第二题批改完成；第一题手写转写待核对。**

- [打开核对页面](https://bergpss.github.io/kangkang-psych-exam/)
- [第二题批改报告](https://bergpss.github.io/kangkang-psych-exam/review-q2.html)（以「三个和尚没水喝」为材料；多份独立审阅，模型名默认模糊，点击显示）
- [阅读转写 Markdown](transcripts/2026-11-05.md)
- [查看原始 PDF](docs/assets/2026-11-05-original.pdf)
- [AI Agent 接手入口](AGENTS.md)

## 康康如何核对

打开页面 → 切换两道题 → 对照原稿 → 勾选准确段落或填写修改 → 导出核对意见并发回。第二题已由康康确认，核对页顶部可直接进入批改报告；第一题仍待逐段核对。

网页只在当前浏览器保存核对进度，不会自动上传反馈。换设备前请导出。完整题干和红笔批注作者仍待补充。

## 内容结构

| 路径 | 用途 |
| --- | --- |
| `context/` | 用户提供的备考背景、项目目标、当前状态 |
| `transcripts/2026-11-05.json` | 唯一结构化转写源，保留不确定性 |
| `transcripts/2026-11-05.md` | 由JSON生成的人类可读转写 |
| `docs/` | GitHub Pages静态网页和原稿；`review-q2.html` 为第二题批改页 |
| `reviews/2026-11-05-q2.json` | 第二题批改的单一数据源（优先问题、其余问题、答题骨架、复习清单） |
| `reviews/2026-11-05-q2-deepseek-v4.1-flash-max.md` | 第二题批改报告（由 build.py 生成） |
| `reviews/TEMPLATE.md` | 后续判题报告模板 |
| `AGENTS.md` | 其他AI模型接手和独立审阅的流程 |
| `scripts/build.py` | 从JSON生成页面与Markdown |

## 本地更新

仅需Python 3，无第三方依赖：

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory docs
```

访问 http://localhost:8000 。修改转写请编辑JSON；修改核对页请编辑 `scripts/page.html`、`docs/style.css`、`docs/app.js`；修改第二题批改请编辑 `reviews/2026-11-05-q2.json` 与 `scripts/review-q2.html`、`docs/review.css`、`docs/review.js`。构建会同时生成 Markdown、核对页与批改页，构建后提交生成内容。

GitHub Pages从main分支的 `/docs` 发布，使用 `.nojekyll`。内容以学习核对为目的；原稿、转写与AI建议严格区分，不提供虚构的官方评分。
