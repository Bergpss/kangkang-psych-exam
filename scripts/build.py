#!/usr/bin/env python3
"""Build the transcript page, the Q2 review report and Markdown from structured data."""
import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]

TRANSCRIPT = ROOT / 'transcripts/2026-11-05.json'
data = json.loads(TRANSCRIPT.read_text())
assert len(data['questions']) == 2
ids = [s['id'] for q in data['questions'] for s in q['sections']]
assert len(ids) == len(set(ids)) == 16
status_label = data.get('statusLabel', '待康康核对')

# ---------------------------------------------------------------- transcript
md = [f"# {data['title']} · 手写转写核对稿", '',
      f"版本：{data['version']}｜状态：{status_label}", '', data['notice'], '',
      '## 用户补充与转写边界', '']
md += [f'- {x}' for x in data['clarifications']]
for q in data['questions']:
    md += ['', f"## {q['page']}. {q['title']}", '', q['subtitle'], '']
    for i, s in enumerate(q['sections'], 1):
        md += [f"### {i}. {s['title']}（{s['id']}）", '', s['text'], '']
        if s.get('note'):
            md += [f"> 转写说明：{s['note']}", '']
    md += ['### 红笔批注（作者未知，不作为标准答案）', '']
    md += [f'- {x}' for x in q['annotations']]
md += ['', '## 后续核对', '',
       '请优先核对第一题材料、学习阶段“空测”、测验时长和补写位置、红笔分值；补充完整题干与批注作者。',
       '转写不等于认可知识正确。第二题批改见 reviews/2026-11-05-q2-*.md。', '']
markdown = '\n'.join(md)
(ROOT / 'transcripts/2026-11-05.md').write_text(markdown)
(ROOT / 'docs/transcript.md').write_text(markdown)

cards = []
for qi, q in enumerate(data['questions']):
    sections = []
    for i, s in enumerate(q['sections'], 1):
        tag = '<span class="tag amber">字句待核</span>' if s.get('uncertain') else ''
        note = f'<aside class="note">{escape(s["note"])}</aside>' if s.get('note') else ''
        sections.append(f'''<article class="answer-card" id="{s['id']}" data-section="{s['id']}">
          <div class="card-heading"><div class="section-label"><span class="number">{i:02}</span><h3>{escape(s['title'])}</h3></div>{tag}</div>
          <div class="transcription">{escape(s['text'])}</div>{note}
          <div class="card-controls"><label class="check"><input type="checkbox" data-check="{s['id']}"><span>这段转写准确</span></label>
          <button type="button" class="text-button correction-toggle" data-target="edit-{s['id']}" aria-expanded="false">修改这段 <span aria-hidden="true">↗</span></button></div>
          <div id="edit-{s['id']}" class="edit-area" hidden><label for="text-{s['id']}">请写原稿实际文字，或指出识别有误的位置</label><textarea id="text-{s['id']}" data-edit="{s['id']}" rows="3" placeholder="例如：这里写的是……"></textarea></div>
        </article>''')
    annotations = ''.join(f'<li>{escape(t)}</li>' for t in q['annotations'])
    cards.append(f'''<section class="question-panel" id="panel-{q['id']}" aria-labelledby="tab-{q['id']}" role="tabpanel" {"hidden" if qi else ""}>
      <div class="question-heading"><div><span class="eyebrow">QUESTION 0{qi+1}</span><h2>{escape(q['title'])}</h2><p>{escape(q['subtitle'])} · 原稿第{q['page']}页</p></div><button type="button" class="outline-button" data-original="{q['page']}">查看手写原稿 ↗</button></div>
      <div class="answer-layout"><div class="answers">{''.join(sections)}
      <details class="annotations"><summary>红笔批注 <span>作者待确认 · 与原答案分开</span></summary><ul>{annotations}</ul></details></div>
      <aside class="original-preview"><div class="preview-heading"><span>原稿对照</span><span>第 {q['page']} / 2 页</span></div><button class="image-button" type="button" data-original="{q['page']}" aria-label="放大第{q['page']}页原稿"><img src="assets/page-{q['page']}.jpg" alt="第{q['page']}页手写心理实验设计答卷" loading="lazy"></button><p>点击放大，黑笔与红笔均保留。</p><a href="assets/2026-11-05-original.pdf" target="_blank" rel="noopener">打开原始 PDF ↗</a></aside></div>
      </section>''')

template = (ROOT / 'scripts/page.html').read_text()
template = template.replace('<!-- QUESTIONS -->', ''.join(cards))
template = template.replace('/* DATA */', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
(ROOT / 'docs/index.html').write_text(template)

# ------------------------------------------------------------------ Q2 review
REVIEW_JSON = ROOT / 'reviews/2026-11-05-q2.json'
if not REVIEW_JSON.exists():
    raise SystemExit('Missing reviews/2026-11-05-q2.json')


def risk_slug(risk):
    return 'high' if risk.startswith('高') else 'mid' if risk.startswith('中') else 'low'


def evidence_items(items):
    out = []
    for item in items:
        text = escape(item['text'])
        if item.get('url'):
            out.append(f'<li><a href="{escape(item["url"])}" target="_blank" rel="noopener">{text} ↗</a></li>')
        else:
            out.append(f'<li>{text}</li>')
    return ''.join(out)


def model_stamp(model):
    name = escape(model)
    return ('<span class="model-stamp"><span class="stamp-label">审阅模型</span>'
            f'<button type="button" class="model-id" data-model="{name}" aria-expanded="false" '
            'aria-label="模型 ID 已模糊，点击显示">'
            f'<span class="model-text" aria-hidden="true">{name}</span>'
            '<span class="model-hint" aria-hidden="true">点击显示</span></button></span>')


def priority_card(p, i):
    return f'''<li class="priority-card">
      <div class="priority-head"><span class="rank">{i:02}</span><div class="priority-title"><h3>{escape(p['title'])}</h3><p>{escape(p['nature'])}</p></div><span class="risk risk-{risk_slug(p['risk'])}">风险 {escape(p['risk'])}</span></div>
      <blockquote class="quote">{escape(p['original'])}</blockquote>
      <dl class="fix-grid">
        <div class="wide"><dt>问题</dt><dd>{escape(p['problem'])}</dd></div>
        <div><dt>为什么</dt><dd>{escape(p['why'])}</dd></div>
        <div><dt>最小修改</dt><dd>{escape(p['fix'])}</dd></div>
        <div class="wide"><dt>考场可直接写</dt><dd class="exam-line">{escape(p['exam'])}</dd></div>
      </dl>
      <details class="evidence"><summary>依据与说明</summary><ul>{evidence_items(p.get('evidence', []))}</ul><p>{escape(p['depends'])}</p></details>
    </li>'''


def issue_card(o):
    return f'''<article class="issue">
      <div class="issue-head"><h4>{escape(o['area'])}</h4><span class="risk risk-{risk_slug(o['risk'])}">风险 {escape(o['risk'])}</span></div>
      <p><span class="mini-label">原句</span>{escape(o['original'])}</p>
      <p><span class="mini-label">问题</span>{escape(o['issue'])}</p>
      <p><span class="mini-label">最小修改</span>{escape(o['fix'])}</p>
    </article>'''


def review_html(r):
    priorities = ''.join(priority_card(p, i) for i, p in enumerate(r['priorities'], 1))
    issues = ''.join(issue_card(o) for o in r['otherIssues'])
    answer = ''.join(f'<li><h4>{escape(a["part"])}</h4><p>{escape(a["text"])}</p></li>'
                     for a in r['modelAnswer'])
    plan = ''.join(f'<li><h4>{escape(s["topic"])}</h4><p>{escape(s["action"])}</p>'
                   f'<p class="plan-check">验收：{escape(s["check"])}</p></li>'
                   for s in r['studyPlan'])
    disputes = ''.join(f'<li>{escape(x)}</li>' for x in r['disagreements'])
    return f'''<article class="review" id="review-{r['index']}">
      <header class="review-head">
        <div><h2>审阅 {r['index']:02} · {escape(r['role'])}</h2><p>{escape(r['date'])} · 转写 {escape(r['transcript'])}</p></div>
        {model_stamp(r['model'])}
      </header>
      <p class="review-summary">{escape(r['summary'])}</p>

      <h3 class="subhead"><span>01</span>优先处理的三件事</h3>
      <ol class="priority-list">{priorities}</ol>

      <details class="other-block"><summary><span>02</span>其余 {len(r['otherIssues'])} 个问题（展开）</summary>{issues}</details>

      <section class="answer-section"><h3 class="subhead"><span>03</span>答题骨架（修订示范）</h3>
        <p class="section-note">修订示范，不是原答案，也不是标准答案；省略号处按真实数据填。</p>
        <ol class="answer-outline">{answer}</ol></section>

      <section class="plan-section"><h3 class="subhead"><span>04</span>复习清单（可验收）</h3>
        <ul class="plan-list">{plan}</ul></section>

      <section class="disagreement"><h3 class="subhead"><span>05</span>边界与分歧</h3><ul>{disputes}</ul></section>
    </article>'''


review_data = json.loads(REVIEW_JSON.read_text())
assert review_data['questionId'] == 'q2'
q2 = next(q for q in data['questions'] if q['id'] == 'q2')

hero = f'''<section class="review-hero">
  <div class="eyebrow"><span class="dot"></span> Q2 · 批改报告</div>
  <h1>{escape(review_data['questionTitle'])}</h1>
  <p class="review-lede">{escape(review_data['intro'])}</p>
  <div class="review-meta">
    <span class="meta-chip">作答第 {review_data['page']} / 2 页</span>
    <span class="meta-chip">转写 v{escape(review_data['transcriptVersion'])} · 已确认</span>
    <span class="meta-chip">更新 {escape(review_data['updated'])}</span>
    <span class="meta-chip">{len(review_data['reviews'])} 份独立审阅</span>
  </div>
  <p class="blur-note">模型名默认模糊，点击后显示。先看判断，再看是谁写的。</p>
</section>'''

scope = f'''<section class="scope-card"><h2>先划边界</h2><ul>{''.join(f'<li>{escape(x)}</li>' for x in review_data['scope'])}</ul><p class="legend">{escape(review_data['legend'])}</p></section>'''

prompt = review_data.get('prompt')
prompt_block = ''
if prompt:
    prompt_block = f'''<section class="prompt-card"><span class="prompt-label">题目材料 · 用户补充</span><div><blockquote>{escape(prompt['text'])}</blockquote><p>{escape(prompt['note'])}</p></div></section>'''

answer_text = ''.join(f'<div class="answer-item"><h4>{escape(s["title"])}</h4><p>{escape(s["text"])}</p></div>'
                      for s in q2['sections'])
answer_block = f'''<details class="original-answer"><summary>第二题已确认转写（{len(q2['sections'])} 段）</summary><div class="answer-text">{answer_text}</div></details>'''

reviews_html = ''.join(review_html(r) for r in review_data['reviews'])

review_template = (ROOT / 'scripts/review-q2.html').read_text()
review_template = review_template.replace('<!-- HERO -->', hero)
review_template = review_template.replace('<!-- SCOPE -->', scope)
review_template = review_template.replace('<!-- PROMPT -->', prompt_block)
review_template = review_template.replace('<!-- ANSWER -->', answer_block)
review_template = review_template.replace('<!-- REVIEWS -->', reviews_html)
(ROOT / 'docs/review-q2.html').write_text(review_template)

# ------------------------------------------------------------- review Markdown
for r in review_data['reviews']:
    if r.get('generateMarkdown', True) is False:
        continue
    lines = [f"# 第二题批改 · {review_data['questionTitle']}", '',
             f"- 审阅者/模型：{r['model']}",
             f"- 日期：{r['date']}",
             f"- 转写版本/commit：v{review_data['transcriptVersion']} / {review_data['commit']}",
             "- 题干是否齐全：部分。用户补充了谚语材料，但完整设问、分值要求与官方评分细则未提供。",
             "- 题目标题：由答案内容概括，不是原题干文字。",
             "- 已确认/存疑内容：第二题转写经康康确认（Berg 于 2026-11-05 对话转述）；第一题不在本文范围。",
             "- 结论适用范围：仅第二题；无官方评分细则，风险等级为辅导判断。", '',
             f"> {r['summary']}", '']
    if prompt:
        lines += ["## 题目材料（用户补充）", '',
                  f"> {prompt['text']}", '',
                  prompt['note'], '']
    lines += ["## 优先处理的三个问题", '']
    for i, p in enumerate(r['priorities'], 1):
        lines += [f"### {i}. {p['title']}", '',
                  f"- 性质：{p['nature']}",
                  f"- 失分风险：{p['risk']}（辅导判断，非官方扣分）",
                  f"- 原句：{p['original']}",
                  f"- 问题：{p['problem']}",
                  f"- 为什么：{p['why']}",
                  f"- 最小修改：{p['fix']}",
                  f"- 考场可直接使用：{p['exam']}",
                  f"- 是否依赖题干：{p['depends']}",
                  "- 依据："]
        for e in p.get('evidence', []):
            if e.get('url'):
                lines.append(f"  - [{e['text']}]({e['url']})")
            else:
                lines.append(f"  - {e['text']}")
        lines.append('')
    lines += ["## 其余问题", '']
    for o in r['otherIssues']:
        lines += [f"### {o['area']}", '',
                  f"- 风险：{o['risk']}",
                  f"- 原句：{o['original']}",
                  f"- 问题：{o['issue']}",
                  f"- 最小修改：{o['fix']}", '']
    lines += ["## 答题结构示范", '',
              "> 修订示范，不是原答案，也不是标准答案；括号与省略号处按真实数据填。", '']
    for i, a in enumerate(r['modelAnswer'], 1):
        lines.append(f"{i}. **{a['part']}**：{a['text']}")
    lines += ['', "## 复习行动", '']
    for i, s in enumerate(r['studyPlan'], 1):
        lines += [f"### {i}. {s['topic']}", '',
                  f"- 动作：{s['action']}",
                  f"- 验收：{s['check']}", '']
    lines += ["## 与其他审阅意见的分歧", '']
    lines += [f"- {x}" for x in r['disagreements']]
    lines += ['', '---', '',
              '本报告由 `scripts/build.py` 从 `reviews/2026-11-05-q2.json` 生成；模型名在网页上默认模糊，点击后显示，避免先入为主。', '']
    out = ROOT / f"reviews/{review_data['updated']}-q2-{r['slug']}.md"
    out.write_text('\n'.join(lines))
    print(f"Wrote {out.relative_to(ROOT)}")

print(f"Built 2 questions / {len(ids)} sections, {len(review_data['reviews'])} Q2 review(s); Markdown + HTML ready.")
