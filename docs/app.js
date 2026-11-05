'use strict';
const transcript = JSON.parse(document.getElementById('transcript-data').textContent);
const storageKey = 'kangkang-transcript-' + transcript.version;
let state = { checks: {}, edits: {}, overall: '' };
let storageAvailable = true;
try {
  const saved = JSON.parse(localStorage.getItem(storageKey));
  if (saved && typeof saved === 'object') {
    state.checks = saved.checks && typeof saved.checks === 'object' ? saved.checks : {};
    state.edits = saved.edits && typeof saved.edits === 'object' ? saved.edits : {};
    state.overall = typeof saved.overall === 'string' ? saved.overall : '';
  }
} catch (_) { storageAvailable = false; }
let toastTimer;
function toast(message) {
  const el = document.getElementById('toast'); el.textContent = message; el.hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => { el.hidden = true; }, 5000);
}
function persist() {
  try { localStorage.setItem(storageKey, JSON.stringify(state)); }
  catch (_) { if (storageAvailable) toast('浏览器无法保存进度，请及时导出核对意见。'); storageAvailable = false; }
}
function progress() {
  const boxes = [...document.querySelectorAll('[data-check]')];
  const count = boxes.filter(el => el.checked).length;
  document.getElementById('progress-label').textContent = `${count} / ${boxes.length} 段已核对`;
  document.getElementById('progress-fill').style.width = `${count / boxes.length * 100}%`;
  boxes.forEach(el => el.closest('.answer-card').classList.toggle('confirmed', el.checked));
}
function selectTab(id, focus = false) {
  document.querySelectorAll('[data-tab]').forEach(el => {
    const active = el.dataset.tab === id; el.setAttribute('aria-selected', String(active));
    el.tabIndex = active ? 0 : -1; if (active && focus) el.focus();
  });
  document.querySelectorAll('.question-panel').forEach(el => { el.hidden = el.id !== 'panel-' + id; });
}
document.querySelectorAll('[data-tab]').forEach(el => {
  el.addEventListener('click', () => selectTab(el.dataset.tab));
  el.addEventListener('keydown', event => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    selectTab(event.key === 'Home' ? 'q1' : event.key === 'End' ? 'q2' : el.dataset.tab === 'q1' ? 'q2' : 'q1', true);
  });
});
document.querySelectorAll('[data-check]').forEach(el => {
  el.checked = state.checks[el.dataset.check] === true;
  el.addEventListener('change', () => { state.checks[el.dataset.check] = el.checked; persist(); progress(); });
});
document.querySelectorAll('.correction-toggle').forEach(el => {
  el.addEventListener('click', () => {
    const panel = document.getElementById(el.dataset.target); panel.hidden = !panel.hidden;
    el.setAttribute('aria-expanded', String(!panel.hidden));
    if (!panel.hidden) panel.querySelector('textarea').focus();
  });
});
document.querySelectorAll('[data-edit]').forEach(el => {
  el.value = typeof state.edits[el.dataset.edit] === 'string' ? state.edits[el.dataset.edit] : '';
  if (el.value) { el.parentElement.hidden = false; document.querySelector(`[data-target="${el.parentElement.id}"]`).setAttribute('aria-expanded', 'true'); }
  el.addEventListener('input', () => {
    state.edits[el.dataset.edit] = el.value;
    const box = document.querySelector(`[data-check="${el.dataset.edit}"]`);
    if (el.value.trim()) { box.checked = false; state.checks[el.dataset.edit] = false; progress(); }
    persist();
  });
});
const overall = document.getElementById('overall'); overall.value = state.overall;
overall.addEventListener('input', () => { state.overall = overall.value; persist(); });
document.getElementById('jump-uncertain').addEventListener('click', () => { selectTab('q1'); document.getElementById('q1-5').scrollIntoView({ block: 'start' }); });
const dialog = document.getElementById('original-dialog');
document.querySelectorAll('[data-original]').forEach(el => el.addEventListener('click', () => {
  const page = el.dataset.original; const src = `assets/page-${page}.jpg`;
  document.getElementById('dialog-image').src = src;
  document.getElementById('dialog-image').alt = `第${page}页手写答卷原稿`;
  document.getElementById('full-image').href = src;
  document.getElementById('original-title').textContent = `手写原稿 · 第${page}页`;
  dialog.showModal(); dialog.scrollTop = 0;
}));
document.getElementById('close-dialog').addEventListener('click', () => dialog.close());
function feedbackMarkdown() {
  const lines = [`# 康康手写答卷 · 核对反馈`, '', `转写版本：${transcript.version}`, `导出时间：${new Date().toISOString()}`, '', '勾选仅表示转写准确，不表示专业答案正确。未勾选表示尚未确认，不自动等于错误。', ''];
  for (const q of transcript.questions) {
    lines.push(`## ${q.title}`, '');
    for (const s of q.sections) {
      const edit = typeof state.edits[s.id] === 'string' ? state.edits[s.id].trim() : '';
      const label = edit ? (state.checks[s.id] ? '已复核，附说明' : '有修改意见') : state.checks[s.id] ? '转写准确' : '尚未确认';
      lines.push(`### ${s.id} ${s.title} — ${label}`, '');
      if (edit) lines.push(edit, '');
    }
  }
  lines.push('## 其他说明 / 完整题干 / 批注作者', '', state.overall.trim() || '未补充', '');
  return lines.join('\n');
}
document.getElementById('export').addEventListener('click', () => {
  const url = URL.createObjectURL(new Blob([feedbackMarkdown()], {type: 'text/markdown;charset=utf-8'}));
  const link = document.createElement('a'); link.href = url; link.download = 'kangkang-2026-11-05-feedback.md';
  document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  toast('已生成核对意见文件；请把文件发给 Berg 或判题 AI。');
});
document.getElementById('copy').addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(feedbackMarkdown()); toast('核对意见已复制，可以粘贴发送。'); }
  catch (_) { toast('当前浏览器不支持复制，请使用“导出核对意见”。'); }
});
progress();
if (!storageAvailable) toast('此浏览器无法恢复保存进度，请及时导出核对意见。');
