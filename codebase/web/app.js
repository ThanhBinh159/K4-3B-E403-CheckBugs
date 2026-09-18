const $ = id => document.getElementById(id);
let busy = false, sourceVersion = 0, viewVersion = 0, pages = [], sources = [], selected = new Set();
const names = {answer:'Có căn cứ',clarify:'Cần làm rõ',no_grounding:'Chưa đủ nguồn',out_of_scope:'Ngoài phạm vi',error:'Lỗi kết nối',loading:'Đang hỏi AI',idle:'Sẵn sàng'};
async function api(url, options) {
  const response = await fetch(url, options);
  const value = await response.json();
  if (!response.ok) throw new Error(value.error || 'Không xử lý được yêu cầu.');
  return value;
}
function progress(step) {
  for (let i=1;i<=4;i++) { const node=$('step'+i); node.classList.toggle('current',i===step); node.classList.toggle('done',i<step); if(i===step) node.setAttribute('aria-current','step'); else node.removeAttribute('aria-current'); }
}
function hideSource() { viewVersion++; $('sourceView').hidden=true; }
function show(state,title,text) {
  document.querySelectorAll('[data-reason]').forEach(node=>node.remove());
  $('output').dataset.state=state; $('state').textContent=names[state]||state;
  $('resultTitle').textContent=title; $('answer').textContent=text;
  $('resultSymbol').textContent={answer:'✓',clarify:'?',no_grounding:'…',out_of_scope:'↗',error:'!',loading:'✦',idle:'✦'}[state];
  $('citations').replaceChildren(); $('actions').replaceChildren(); $('citationsSection').hidden=true; $('metaDetails').hidden=true; hideSource();
}
function button(target,label,action,className='secondary-button') { const b=document.createElement('button'); b.type='button'; b.className=className; b.textContent=label; b.onclick=action; $(target).append(b); }
function error(text) { $('formError').textContent=text; $('formError').hidden=!text; }
function selectedInfo() {
  $('selectionCount').textContent=selected.size+' / 3'; $('preview').disabled=busy||!selected.size; $('clearPages').disabled=busy||!selected.size;
  document.querySelectorAll('.page-row input').forEach(c=>c.disabled=busy||(!c.checked&&selected.size>=3));
}
function renderPages() {
  const query=$('pageSearch').value.trim().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').toLowerCase();
  const rows=pages.filter(p=>(p.id+' '+p.preview).normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').toLowerCase().includes(query));
  $('pageList').replaceChildren();
  for(const row of rows) {
    const item=document.createElement('div');item.className='page-row';
    const check=document.createElement('input');check.type='checkbox';check.id='page-'+row.id;check.value=row.id;check.checked=selected.has(row.id);
    const label=document.createElement('label');label.htmlFor=check.id;
    const title=document.createElement('strong');title.textContent='Trang '+Number(row.id.split('-').pop())+' · '+row.id;
    const subtitle=document.createElement('span');subtitle.textContent=row.preview;label.title=row.preview;label.append(title,subtitle);
    check.onchange=()=>{ if(check.checked&&selected.size>=3){check.checked=false;error('Bạn chỉ có thể chọn tối đa 3 trang.');return;} check.checked?selected.add(row.id):selected.delete(row.id);error('');selectedInfo();progress(2); };
    item.append(check,label);$('pageList').append(item);
  }
  if(!rows.length){const p=document.createElement('p');p.className='page-empty';p.textContent=pages.length?'Không tìm thấy trang. Thử số trang hoặc từ khóa khác.':'Danh sách trang sẽ hiện khi bạn chọn bài học.';$('pageList').append(p);}
  selectedInfo();
}
function lock(value) {
  busy=value;
  for(const id of ['source','question','ask']) $(id).disabled=value;
  $('pageSearch').disabled=value||!pages.length; selectedInfo();
  document.querySelectorAll('[data-question]').forEach(b=>b.disabled=value);
  $('output').setAttribute('aria-busy',String(value)); $('ask').firstElementChild.textContent=value?'Đang hỏi AI…':'Hỏi tutor';
}
async function openSegment(sourceId,id,advance=true) {
  const version=++viewVersion;
  try {
    const value=await api('/api/segment?source_id='+encodeURIComponent(sourceId)+'&id='+encodeURIComponent(id));
    if(version!==viewVersion)return;
    $('sourceTitle').textContent='Trang '+value.page_number+' · '+id;
    $('sourceHint').textContent=value.heading+' · Số trang tính theo PDF, có thể khác số in ở chân slide.';
    $('sourceText').textContent=value.text; $('sourceWarning').hidden=!value.extraction_warning;
    $('sourceWarning').textContent='Có ký tự trích xuất lỗi. Mở PDF gốc để đối chiếu; tutor chưa đọc hình hoặc sơ đồ bằng OCR.';
    $('sourcePdf').replaceChildren();
    if(value.pdf_url){const a=document.createElement('a');a.href=value.pdf_url;a.target='_blank';a.rel='noopener';a.textContent='Mở PDF gốc · trang '+value.page_number+' ↗';$('sourcePdf').append(a);}
    $('sourceView').hidden=false;if(advance)progress(4);$('sourceView').scrollIntoView({behavior:'smooth',block:'nearest'});
  } catch(e){error(e.message);}
}
$('source').onchange=async()=>{
  const version=++sourceVersion,source=$('source').value;
  pages=[];selected.clear();$('pageSearch').value='';$('pageSearch').disabled=true;renderPages();error('');
  show('idle','Đặt câu hỏi theo bài đã chọn.','Câu hỏi của bạn được giữ lại. Lượt hỏi tiếp theo sẽ dùng bộ slide mới.');progress(source?2:1);
  const info=sources.find(s=>s.id===source);$('sourceInfo').textContent=info?info.page_count+' trang PDF · '+info.segment_count+' trang có chữ để tìm kiếm.':'Chọn Day 1 hoặc Day 2 để bắt đầu.';
  if(!source)return;
  $('pageList').firstElementChild.textContent='Đang tải các trang bài học…';
  try{const rows=await api('/api/segments?source_id='+encodeURIComponent(source));if(version!==sourceVersion)return;pages=rows;$('pageSearch').disabled=busy||!pages.length;renderPages();}
  catch(e){if(version!==sourceVersion)return;error(e.message);}
};
$('pageSearch').oninput=renderPages;
$('preview').onclick=()=>{if(selected.size)openSegment($('source').value,[...selected][0],false);};
$('clearPages').onclick=()=>{selected.clear();renderPages();};
$('closeSource').onclick=hideSource;
$('question').oninput=()=>{$('counter').textContent=$('question').value.length+' / 2.000';error('');if(!busy)progress($('source').value?2:1);};
document.querySelectorAll('[data-question]').forEach(b=>b.onclick=()=>{$('question').value=b.dataset.question;$('question').oninput();$('question').focus();});
function editQuestion(){progress(2);$('question').focus();$('question').select();$('question').scrollIntoView({behavior:'smooth',block:'center'});}
$('askForm').onsubmit=async event=>{
  event.preventDefault();if(busy)return;
  const input={source_id:$('source').value,question:$('question').value.trim(),selected_segment_ids:[...selected]};
  if(!input.source_id){error('Chọn bộ slide bài học trước khi hỏi tutor.');$('source').focus();progress(1);return;}
  if(!input.question){error('Nhập câu hỏi bạn muốn tìm hiểu.');$('question').focus();progress(2);return;}
  error('');lock(true);progress(3);show('loading','Tutor đang đọc phần nguồn liên quan…','Đang tạo lời giải thích cho câu hỏi của bạn. Nếu nguồn chưa đủ hoặc câu hỏi chưa rõ, tutor sẽ gợi ý bước tiếp theo.');
  try{
    const value=await api('/api/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(input)});
    const titles={answer:'Đây là lời giải thích từ slide.',clarify:'Làm rõ thêm một chút nhé.',no_grounding:'Chưa có đủ căn cứ để giải thích.',out_of_scope:'Câu hỏi này cần một nguồn khác.'};
    const text=value.answer||value.clarifying_question||value.reason;show(value.action,titles[value.action],text);
    if(value.action==='clarify'&&value.reason){const p=document.createElement('p');p.className='field-help';p.textContent=value.reason;$('actions').before(p);p.dataset.reason='true';}
    $('citationsSection').hidden=!value.citations.length;
    value.citations.forEach(id=>button('citations','Trang '+Number(id.split('-').pop())+' · '+id+' ↗',()=>openSegment(input.source_id,id),'citation-button'));
    button('actions',value.action==='clarify'?'Bổ sung câu hỏi':'Sửa câu hỏi',editQuestion);
    if(value.action!=='answer')button('actions','Chọn trang hoặc đổi bài',()=>{progress(1);$('source').focus();$('source').scrollIntoView({behavior:'smooth',block:'center'});});
    $('meta').textContent=value.model+' · '+(value.latency_ms/1000).toFixed(1)+' giây · Mã lượt hỏi '+value.request_id;$('metaDetails').hidden=false;
  }catch(e){show('error','Chưa nhận được kết quả AI.',e.message+' Câu hỏi và các trang đã chọn vẫn được giữ.');button('actions','Thử lại',()=>$('askForm').requestSubmit());button('actions','Sửa câu hỏi',editQuestion);}
  finally{lock(false);}
};
(async()=>{
  try{
    const health=await api('/api/health');if(!health.source_ready)throw new Error(health.error||'Chưa tải được bộ slide bài học.');
    sources=await api('/api/sources');sources.forEach(s=>$('source').add(new Option((s.id==='slides-d1'?'Day 1 · Nền tảng AI':s.id==='slides-d2'?'Day 2 · Thiết kế sản phẩm AI':s.name)+' · '+s.segment_count+' trang',s.id)));
    $('healthText').textContent=health.model_configured?'Slide đã sẵn sàng · Kết nối AI được kiểm tra khi bạn gửi câu hỏi.':'Slide đã sẵn sàng · Chưa cấu hình AI. Điền API trong .env rồi khởi động lại server.';$('health').classList.toggle('error',!health.model_configured);
  }catch(e){$('healthText').textContent=e.message;$('health').classList.add('error');}
})();
