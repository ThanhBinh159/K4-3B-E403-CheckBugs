const $ = id => document.getElementById(id);
let busy = false, sourceVersion = 0;
async function api(url, options) {
  const response = await fetch(url, options);
  const value = await response.json();
  if (!response.ok) throw new Error(value.error || 'Không xử lý được yêu cầu.');
  return value;
}
function selectedIds() { return [...$('segments').selectedOptions].map(o => o.value); }
function show(state, title, text) {
  $('state').textContent = state; $('resultTitle').textContent = title; $('answer').textContent = text;
  $('citations').replaceChildren(); $('actions').replaceChildren(); $('meta').textContent = ''; $('sourceView').hidden = true;
}
function button(target, label, action) {
  const b = document.createElement('button'); b.type = 'button'; b.className = 'secondary'; b.textContent = label; b.onclick = action; $(target).append(b);
}
function lock(value) {
  busy = value;
  for (const id of ['source','segments','question','ask','preview']) $(id).disabled = value;
  document.querySelectorAll('[data-question]').forEach(b => b.disabled = value);
  $('output').setAttribute('aria-busy', String(value)); $('ask').textContent = value ? 'Đang hỏi AI…' : 'Hỏi tutor →';
}
async function openSegment(sourceId, id) {
  try {
    const value = await api('/api/segment?source_id=' + encodeURIComponent(sourceId) + '&id=' + encodeURIComponent(id));
    $('sourceTitle').textContent = id + ' · ' + value.heading;
    $('sourceText').textContent = value.text; $('sourceView').hidden = false;
    $('sourcePdf').replaceChildren();
    if (value.pdf_url) {
      const link = document.createElement('a'); link.href = value.pdf_url;
      link.target = '_blank'; link.rel = 'noopener';
      link.textContent = 'Mở PDF gốc · trang ' + value.page_number;
      $('sourcePdf').append(link);
    }
    if (value.extraction_warning) $('sourcePdf').append(document.createTextNode(' · Có ký tự trích xuất lỗi; đối chiếu PDF gốc.'));
  } catch (e) { $('meta').textContent = e.message; }
}
$('source').onchange = async () => {
  const version = ++sourceVersion, source = $('source').value;
  $('segments').replaceChildren(); $('sourceView').hidden = true;
  show('NGUỒN ĐÃ ĐỔI', 'Đặt câu hỏi theo bài mới', 'Lượt hỏi tiếp theo sẽ dùng nguồn mới; câu hỏi của bạn vẫn được giữ.');
  if (!source) return;
  try {
    const rows = await api('/api/segments?source_id=' + encodeURIComponent(source));
    if (version !== sourceVersion) return;
    rows.forEach(row => $('segments').add(new Option(row.id + ' · ' + row.preview, row.id)));
  } catch (e) { show('LỖI NGUỒN', 'Chưa tải được đoạn', e.message); }
};
$('preview').onclick = () => {
  const ids = selectedIds();
  if (ids.length) openSegment($('source').value, ids[0]);
  else $('meta').textContent = 'Hãy chọn một đoạn để đọc trước.';
};
$('closeSource').onclick = () => $('sourceView').hidden = true;
$('question').oninput = () => $('counter').textContent = $('question').value.length + ' / 2.000';
document.querySelectorAll('[data-question]').forEach(b => b.onclick = () => { $('question').value = b.dataset.question; $('question').oninput(); $('question').focus(); });
$('askForm').onsubmit = async event => {
  event.preventDefault(); if (busy) return;
  const input = {source_id: $('source').value, question: $('question').value.trim(), selected_segment_ids: selectedIds()};
  if (input.selected_segment_ids.length > 3) { show('CẦN ĐIỀU CHỈNH', 'Chọn tối đa 3 đoạn', 'Bỏ bớt đoạn rồi gửi lại.'); return; }
  if (!input.source_id || !input.question) return;
  lock(true); show('ĐANG GỌI AI', 'Đang tìm lời giải thích trong nguồn…', 'Câu hỏi và các đoạn liên quan được gửi đến provider đã cấu hình.');
  try {
    const value = await api('/api/ask', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(input)});
    const titles = {answer:'Giải thích từ nguồn đã chọn', clarify:'Cần làm rõ một chút', no_grounding:'Chưa đủ căn cứ trong phần đã tìm', out_of_scope:'Yêu cầu ngoài phạm vi bài học'};
    show(value.action.toUpperCase(), titles[value.action], value.answer || value.clarifying_question || value.reason);
    value.citations.forEach(id => button('citations', 'Mở [' + id + ']', () => openSegment(input.source_id, id)));
    button('actions','Sửa câu hỏi', () => { $('question').focus(); $('question').select(); });
    if (value.action !== 'answer') button('actions','Đổi nguồn hoặc chọn đoạn', () => $('source').focus());
    $('meta').textContent = value.model + ' · ' + (value.latency_ms / 1000).toFixed(1) + ' giây · Trace ' + value.request_id;
  } catch(e) {
    show('LỖI HỆ THỐNG', 'Chưa có kết quả AI', e.message);
    button('actions','Thử lại', () => $('askForm').requestSubmit());
    button('actions','Sửa câu hỏi', () => $('question').focus());
  } finally { lock(false); }
};
(async () => {
  try {
    const health = await api('/api/health');
    if (!health.source_ready) throw new Error(health.error || 'Chưa có nguồn bài học.');
    const sources = await api('/api/sources');
    sources.forEach(s => $('source').add(new Option(s.name + ' · ' + s.segment_count + (s.kind === 'slides' ? ' trang có chữ' : ' đoạn'), s.id)));
    $('health').textContent = health.model_configured ? 'Nguồn đã tải. AI đã cấu hình; khả năng kết nối sẽ được xác minh khi gửi câu hỏi.' : 'Nguồn đã tải. Cần điền provider, model và API key trong .env rồi khởi động lại server để hỏi AI thật.';
    $('health').classList.toggle('error', !health.model_configured);
  } catch(e) { $('health').textContent = e.message; $('health').classList.add('error'); }
})();
