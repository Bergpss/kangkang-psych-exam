#!/usr/bin/env python3
"""Build the isolated Astra Q2 report; never reads another model's review."""
from pathlib import Path
import json
from html import escape as e

ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'reviews/2026-11-05-q2-gpt-6-astra-high.json').read_text())
# Markdown is generated solely from this review's own source.
lines=['# 第二题独立判题 · GPT-6 Astra High','',f"日期：{r['date']}｜转写：v{r['transcript']}",'',r['summary'],'','## 资料与审阅范围','',r['context']['scope'],'',f"补充材料：{r['context']['material']}",'',r['context']['source'],'','## 三个优先修改项','']
for p in r['priorities']:
    lines += ['### '+p['title'],'']
    for key,label in [('nature','性质'),('risk','风险（非官方扣分）'),('original','原句'),('problem','问题'),('why','分析'),('fix','最小修改'),('exam','考场表达'),('depends','边界')]:
        lines += [f"**{label}**：{p[key]}",'']
    lines += ['**依据**：','']
    for ref in p['evidence']:
        lines += [(f"- [{ref['text']}]({ref['url']})" if ref['url'] else '- '+ref['text'])]
    lines += ['']
lines += ['## 其他检查','']
for x in r['otherIssues']:
    lines += ['### '+x['area'],'',f"风险：{x['risk']}",'',f"原句：{x['original']}",'',x['issue'],'','修改：'+x['fix'],'']
lines += ['## 修订示范','']
for a in r['modelAnswer']: lines += ['### '+a['part'],'',a['text'],'']
lines += ['## 复习动作','']
for s in r['studyPlan']: lines += ['### '+s['topic'],'',s['action'],'','验收：'+s['check'],'']
lines += ['## 审阅边界与独立判断','']+[('- '+x) for x in r['disagreements']]+['']
(ROOT/'reviews/2026-11-05-q2-gpt-6-astra-high.md').write_text('\n'.join(lines))
cards=[]
for i,p in enumerate(r['priorities'],1):
    refs=''.join(f'<li><a href="{e(x["url"])}" target="_blank" rel="noopener">{e(x["text"])}</a></li>' if x['url'] else f'<li>{e(x["text"])}</li>' for x in p['evidence'])
    cards.append(f'''<article class="review-card"><div class="card-top"><span class="rank">0{i}</span><span class="tag amber">{e(p['nature'])}</span></div>
      <h2>{e(p['title'])}</h2><blockquote>{e(p['original'])}</blockquote><p class="finding">{e(p['problem'])}</p>
      <div class="replace"><span class="eyebrow">考场改写</span><p>{e(p['exam'])}</p></div>
      <details><summary>为什么这样判？看分析与修改边界</summary><p>{e(p['why'])}</p><p><b>最小修改：</b>{e(p['fix'])}</p><p><b>判断边界：</b>{e(p['depends'])}</p><p><b>失分风险：</b>{e(p['risk'])}（辅导判断）</p><ul>{refs}</ul></details></article>''')
issues=''.join(f'''<details class="issue-row"><summary><span>{e(x['area'])}</span><small>{e(x['risk'])}</small></summary><blockquote>{e(x['original'])}</blockquote><p>{e(x['issue'])}</p><div class="replace"><b>建议怎么写</b><p>{e(x['fix'])}</p></div></details>''' for x in r['otherIssues'])
answer=''.join(f'<li><h3>{e(a["part"])}</h3><p>{e(a["text"])}</p></li>' for a in r['modelAnswer'])
plan=''.join(f'<article class="plan-item"><span class="number">0{i}</span><h3>{e(x["topic"])}</h3><p>{e(x["action"])}</p><p class="checkpoint"><b>做到什么算会了</b><br>{e(x["check"])}</p></article>' for i,x in enumerate(r['studyPlan'],1))
boundaries=''.join(f'<li>{e(x)}</li>' for x in r['disagreements'])
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#203f36"><title>第二题独立判题 · GPT-6 Astra High</title><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="astra-review.css"></head><body>
<header class="topbar"><a class="brand" href="./"><span class="brand-icon">康</span><span>康康的备考手记<span class="brand-small">INDEPENDENT REVIEW · Q2 ONLY</span></span></a><a class="repo-link" href="./">返回转写核对 ↗</a></header>
<main><section class="review-hero"><div class="eyebrow"><span class="dot"></span> 仅第二题 · 独立审阅</div><h1>设计框架成立，<br><em>把证据说严谨。</em></h1><p class="lead">团体人数与社会惰性 · 不推倒重写，先修最影响结论的三处。</p><div class="review-badges"><span class="model-name">GPT-6 Astra High</span><span>2026.11.05</span><span>转写 v0.1.0</span><span>无官方评分细则 · 不估分</span></div></section>
<section class="strength"><span class="eyebrow">值得保留</span><h2>你的答案已经有一副可用的骨架。</h2><div class="keep-list"><span>✓ 单因素被试间设计</span><span>✓ 随机分派</span><span>✓ 行为指标：点击数</span><span>✓ 时长统一为5分钟</span></div><p>需要修的是变量、程序与推断的衔接。以下仅评第二题黑笔答案；原文与修订示范分开保留。</p></section>
<nav class="review-nav" aria-label="报告导航"><a href="#priorities">三个优先问题</a><a href="#clarify">别误判的两件事</a><a href="#more">其余检查</a><a href="#rewrite">修订示范</a><a href="#practice">复习动作</a></nav>
<section id="priorities"><div class="section-heading"><span class="eyebrow">FIRST THINGS FIRST</span><h2>先改这三处</h2></div><!-- CARDS --></section>
<section id="clarify" class="clarify"><div class="section-heading"><span class="eyebrow">KEEP THE DISTINCTIONS</span><h2>这两个地方，不能简单判错。</h2></div><div class="two-columns"><article><h3>30名被试 ≠ 30人团体</h3><p>若操纵的是感知人数，每个条件都可以有30名被试。</p><table><caption>可成立的模拟团体分配</caption><thead><tr><th>条件</th><th>被试数</th><th>告知规模</th></tr></thead><tbody><tr><td>A</td><td>30名</td><td>5人</td></tr><tr><td>B</td><td>30名</td><td>15人</td></tr><tr><td>C</td><td>30名</td><td>30人</td></tr></tbody></table><small>这只是原方案的一种合理解释，需在答案里明确，不可假定已经写清。</small></article><article><h3>基线是否必需，要看研究问题</h3><div class="case"><span>只比较不同规模的贡献</span><p>可用5 / 15 / 30三个条件；缺少单独作业条件不是直接否定理由。</p></div><div class="case"><span>证明相对独立作业发生惰性</span><p>需有适当的独立作业基线，才能直接比较努力减少。</p></div><small>加入基线后要同步调整设计和统计，不能只在最后补一句“设控制组”。</small></article></div></section>
<section class="logic-lab"><div><span class="eyebrow">A LOGICAL COUNTEREXAMPLE</span><h2>30低于两组，<br>不等于逐级下降。</h2><p>右侧均值中，30人条件最低，<br>但5→15的方向是上升。</p></div><div><table><caption>假想均值 · 非实验数据 · 不代表显著性</caption><thead><tr><th>人数条件</th><th>假想平均点击数</th></tr></thead><tbody><tr><td>5人</td><td><span class="bar" style="--w:83%">100</span></td></tr><tr><td>15人</td><td><span class="bar" style="--w:100%">120</span></td></tr><tr><td>30人</td><td><span class="bar" style="--w:50%">60</span></td></tr></tbody></table><p class="tiny">这里只演示逻辑方向。显著性还需要变异、样本量和实际检验；不能由条形图直接判断。</p></div></section>
<section id="more"><div class="section-heading"><span class="eyebrow">CHECK THE DETAILS</span><h2>还有六处，逐项展开看。</h2></div><!-- ISSUES --></section>
<section id="rewrite" class="rewrite"><details><summary><span class="eyebrow">EXAM-READY REVISION</span><h2>保留原思路的修订示范 <span>＋</span></h2></summary><p>适用于题干允许模拟团体的情况，不是标准答案。原来的90人、三个人数条件、点击任务和5分钟均保留。</p><ol><!-- ANSWER --></ol></details></section>
<section id="practice"><div class="section-heading"><span class="eyebrow">NEXT STUDY SESSION</span><h2>下一次复习，用55分钟练清楚。</h2><p>建议分配，并非考试规定用时。</p></div><div class="practice-grid"><!-- PLAN --></div></section>
<details class="scope-notes"><summary>审阅边界、依据与独立性说明</summary><ul><!-- BOUNDARIES --></ul><p>概念核对使用Latané等（1979）原始研究、APA术语定义、NIST与Minitab官方统计文档。具体规则推导和改写为本报告判断，不是深大官方评分意见。</p></details>
<div class="report-links"><a href="review-q2-astra.md" download>下载本份批改 Markdown ↓</a><a href="assets/page-2.jpg" target="_blank" rel="noopener">查看第二页原稿 ↗</a><a href="review-q2.html#review-2">返回多模型审阅页 ↗</a></div>
</main><footer><span>独立审阅 · 仅第二题</span><span>GPT-6 Astra High</span><span>先把逻辑接上，再把句子压短。</span></footer></body></html>'''
for key,value in [('CARDS',''.join(cards)),('ISSUES',issues),('ANSWER',answer),('PLAN',plan),('BOUNDARIES',boundaries)]:
    page=page.replace('<!-- '+key+' -->',value)
page=page.replace('review-q2.html#review-2','review-q2.html')
page=page.replace('<nav class="review-nav"', '<aside class="note">材料更新：共享项目记录补充了“一个和尚挑水喝，二个和尚抬水喝，三个和尚没水喝”。若设问要求验证该现象，应优先加入独立作业对照；完整设问仍缺失，不能据谚语直接断定只能用1/2/3人。备选修订见下文。</aside><nav class="review-nav"')
(ROOT/'docs/review-q2-astra.html').write_text(page)
md=ROOT/'reviews/2026-11-05-q2-gpt-6-astra-high.md'
if md.exists(): (ROOT/'docs/review-q2-astra.md').write_text(md.read_text())
print('Built isolated GPT-6 Astra High Q2 report.')
