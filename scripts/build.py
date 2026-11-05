#!/usr/bin/env python3
"""Build the review page and Markdown from the same canonical transcript."""
import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'transcripts/2026-11-05.json').read_text())
assert len(data['questions']) == 2
ids = [s['id'] for q in data['questions'] for s in q['sections']]
assert len(ids) == len(set(ids)) == 16

md = [f"# {data['title']} · 手写转写核对稿", '',
      f"版本：{data['version']}｜状态：待康康核对", '', data['notice'], '',
      '## 用户补充与转写边界', '']
md += [f'- {x}' for x in data['clarifications']]
for q in data['questions']:
    md += ['', f"## {q['page']}. {q['title']}", '', q['subtitle'], '']
    for i, s in enumerate(q['sections'], 1):
        md += [f"### {i}. {s['title']}（{s['id']}）", '', s['text'], '']
        if s.get('note'): md += [f"> 转写说明：{s['note']}", '']
    md += ['### 红笔批注（作者未知，不作为标准答案）', '']
    md += [f'- {x}' for x in q['annotations']]
md += ['', '## 后续核对', '',
       '请优先核对第一题材料、学习阶段“空测”、测验时长和补写位置、红笔分值；补充完整题干与批注作者。',
       '转写不等于认可知识正确。正式判题另行记录于reviews目录。', '']
markdown = '\n'.join(md)
(ROOT/'transcripts/2026-11-05.md').write_text(markdown)
(ROOT/'docs/transcript.md').write_text(markdown)

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
template = (ROOT/'scripts/page.html').read_text()
template = template.replace('<!-- QUESTIONS -->', ''.join(cards))
template = template.replace('/* DATA */', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
(ROOT/'docs/index.html').write_text(template)
print(f'Built 2 questions / {len(ids)} sections; Markdown + HTML ready.')
