const $ = id => document.getElementById(id);
let data = null, mode = 'text';
const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
document.querySelectorAll('[data-view]').forEach(button => button.onclick = () => {
  document.querySelectorAll('[data-view]').forEach(b => b.classList.toggle('active', b === button));
  $('workspace').hidden = button.dataset.view !== 'workspace'; $('method').hidden = button.dataset.view !== 'method';
  $('breadcrumb').textContent = button.dataset.view === 'method' ? 'How it works' : 'Overview';
});
document.querySelectorAll('[data-mode]').forEach(button => button.onclick = () => {
  mode = button.dataset.mode;
  document.querySelectorAll('[data-mode]').forEach(b => { b.classList.toggle('selected', b === button); b.setAttribute('aria-selected', b === button); });
  $('text-input').hidden = mode !== 'text'; $('file-input').hidden = mode !== 'file';
});
async function run(sample = false) {
  $('message').textContent = '';
  let options;
  if (!sample && mode === 'file') {
    if (!$('file').files[0]) { $('message').textContent = 'Choose a CSV file first.'; return; }
    const body = new FormData(); body.append('file', $('file').files[0]); options = {method:'POST', body};
  } else options = {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(sample ? {sample:true} : {text:$('posts').value})};
  $('analyze').disabled = $('sample').disabled = true; $('analyze').textContent = 'Analyzing…';
  try {
    const response = await fetch('/api/analyze', options);
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Analysis failed. Please try again.');
    data = result; render();
  } catch (error) { $('message').textContent = error.message === 'Failed to fetch' ? 'Cannot reach the local server. Start the app and try again.' : error.message; }
  finally { $('analyze').disabled = $('sample').disabled = false; $('analyze').textContent = 'Analyze posts'; }
}
function render() {
  $('source').textContent = data.source;
  $('total').textContent = $('chart-total').textContent = data.total;
  $('dedup').textContent = data.duplicates ? `${data.duplicates} exact duplicates removed` : 'Unique posts in this analysis';
  $('positive').textContent = Math.round(data.counts.Positive / data.total * 100) + '%';
  $('negative').textContent = Math.round(data.counts.Negative / data.total * 100) + '%';
  $('average').textContent = (data.average > 0 ? '+' : '') + data.average.toFixed(2);
  const positive = data.counts.Positive / data.total * 100, neutral = data.counts.Neutral / data.total * 100;
  $('donut').style.background = `conic-gradient(#389b81 0 ${positive}%,#b9c8d3 ${positive}% ${positive + neutral}%,#d9847b ${positive + neutral}% 100%)`;
  $('donut').setAttribute('aria-label', Object.entries(data.counts).map(([k,v])=>`${k}: ${v}`).join(', '));
  $('legend').innerHTML = Object.entries(data.counts).map(([label, count]) => `<div><i class="dot ${label.toLowerCase()}"></i>${label}<strong>${count}</strong></div>`).join('');
  $('topics').innerHTML = data.topics.length ? data.topics.map(topic => `<div class="topic"><div><span>${escapeHTML(topic.name)}</span><b>${topic.count}</b></div><div class="topic-track"><i style="width:${topic.count/data.total*100}%"></i></div></div>`).join('') : '<p>No meaningful topic terms found.</p>';
  $('export').disabled = false; renderRows();
}
function renderRows() {
  if (!data) return;
  const rows = data.rows.filter(row => ($('filter').value === 'All' || row.sentiment === $('filter').value) && row.text.toLowerCase().includes($('search').value.toLowerCase()));
  $('rows').innerHTML = rows.length ? rows.map(row=>`<tr><td>${escapeHTML(row.text)}</td><td><span class="pill ${row.sentiment}">${row.sentiment}</span></td><td>${row.score.toFixed(3)}</td><td>${escapeHTML(row.topic)}</td></tr>`).join('') : '<tr><td colspan="4">No posts match your filters.</td></tr>';
  $('row-count').textContent = `${rows.length} of ${data.total} posts`;
}
$('search').oninput = renderRows; $('filter').onchange = renderRows;
$('analyze').onclick = () => run(); $('sample').onclick = () => run(true);
$('export').onclick = () => {
  if (!data) return;
  const quote = value => {let s = String(value); if (/^[=+@\-\t\r]/.test(s)) s = "'"+s; return '"'+s.replaceAll('"','""')+'"';};
  const csv = ['text,sentiment,compound_score,topic', ...data.rows.map(r => [r.text,r.sentiment,r.score,r.topic].map(quote).join(','))].join('\r\n');
  const url = URL.createObjectURL(new Blob(['\ufeff'+csv],{type:'text/csv;charset=utf-8'}));
  const a = document.createElement('a'); a.href = url; a.download = 'signal-analysis.csv'; a.click(); setTimeout(()=>URL.revokeObjectURL(url),1000);
};
run(true);
