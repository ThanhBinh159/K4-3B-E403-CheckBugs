import {spawn} from 'node:child_process';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const output=fileURLToPath(new URL('../tmp/ui-review/',import.meta.url));
await mkdir(output,{recursive:true});
const browser=spawn('C:/Program Files/Google/Chrome/Application/chrome.exe',['--headless=new','--disable-gpu','--no-first-run','--remote-debugging-port=9327',`--user-data-dir=${output}/chrome-profile`,'about:blank'],{windowsHide:true,stdio:'ignore'});
let socket;
try {
  let tabs;
  for(let i=0;i<50;i++){try{tabs=await (await fetch('http://127.0.0.1:9327/json')).json();if(tabs.length)break;}catch{}await new Promise(r=>setTimeout(r,200));}
  assert(tabs?.length,'Headless browser did not start');
  socket=new WebSocket(tabs.find(t=>t.type==='page').webSocketDebuggerUrl);await new Promise((resolve,reject)=>{socket.onopen=resolve;socket.onerror=reject;});
  let seq=0;const pending=new Map();socket.onmessage=({data})=>{const v=JSON.parse(data);if(v.id&&pending.has(v.id)){const {resolve,reject}=pending.get(v.id);pending.delete(v.id);v.error?reject(new Error(JSON.stringify(v.error))):resolve(v.result);}};
  const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));});
  const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  const wait=async expression=>{for(let i=0;i<100;i++){if(await evaluate(expression))return;await new Promise(r=>setTimeout(r,100));}throw new Error('UI wait failed: '+expression);};
  const screenshot=async name=>{const {data}=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true});await writeFile(`${output}/${name}.png`,Buffer.from(data,'base64'));};
  await send('Page.enable');await send('Runtime.enable');await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:'http://127.0.0.1:8765/'});
  await wait("document.querySelector('#source')?.options.length===3");
  await screenshot('desktop-idle');
  await evaluate("document.querySelector('#askForm').requestSubmit()");assert.match(await evaluate("document.querySelector('#formError').textContent"),/Chọn/);
  await evaluate("document.querySelector('#source').value='slides-d1';document.querySelector('#source').dispatchEvent(new Event('change'))");
  await wait("document.querySelectorAll('.page-row').length===29");
  await evaluate("[...document.querySelectorAll('.page-row input')].slice(0,3).forEach(x=>x.click())");
  assert.equal(await evaluate("document.querySelectorAll('.page-row input:checked').length"),3);
  assert.equal(await evaluate("document.querySelectorAll('.page-row input:disabled').length"),26);
  await evaluate("document.querySelector('#pageSearch').value='Token';document.querySelector('#pageSearch').dispatchEvent(new Event('input'))");
  assert.equal(await evaluate("document.querySelector('#selectionCount').textContent"),'3 / 3');
  await evaluate("document.querySelector('#clearPages').click();document.querySelector('#pageSearch').value='13';document.querySelector('#pageSearch').dispatchEvent(new Event('input'));document.querySelector('#page-S01-013').click();document.querySelector('#preview').click()");
  await wait("!document.querySelector('#sourceView').hidden");assert.match(await evaluate("document.querySelector('#sourcePdf a').getAttribute('href')"),/#page=13/);
  // Mock only /api/ask in this test tab. Production code and source GETs are unchanged.
  await evaluate(`window.realFetch=window.fetch;window.mockAction='answer';window.fetch=async(url,opts)=>{if(url!='/api/ask')return window.realFetch(url,opts);await new Promise(r=>setTimeout(r,250));if(window.mockAction==='error')return new Response(JSON.stringify({error:'Test timeout'}),{status:502});const action=window.mockAction;return new Response(JSON.stringify({action,answer:action==='answer'?'Token là các mảnh văn bản [S01-013].':'',citations:action==='answer'?['S01-013']:[],clarifying_question:action==='clarify'?'Bạn muốn hỏi về khái niệm nào?':'',reason:action==='answer'?'':'Lý do giới hạn trong test.',model:'TEST FIXTURE',latency_ms:250,request_id:'fixture-only'}),{status:200});};document.querySelector('#question').value='Token là gì?';document.querySelector('#question').dispatchEvent(new Event('input'))`);
  for(const action of ['answer','clarify','no_grounding','out_of_scope','error']){
    await evaluate(`window.mockAction='${action}';document.querySelector('#askForm').requestSubmit()`);
    await wait("document.querySelector('#output').dataset.state==='loading'");assert.equal(await evaluate("document.querySelector('#question').disabled"),true);
    await wait(`document.querySelector('#output').dataset.state==='${action}'&&!document.querySelector('#ask').disabled`);
    assert.equal(await evaluate("document.querySelector('#question').value"),'Token là gì?');assert.equal(await evaluate("document.querySelector('#selectionCount').textContent"),'1 / 3');
    if(action==='answer'){await evaluate("document.querySelector('#citations button').click()");await wait("!document.querySelector('#sourceView').hidden");assert.equal(await evaluate("document.querySelector('#step4').getAttribute('aria-current')"),'step');await screenshot('desktop-answer-fixture');}
    if(action==='out_of_scope')assert.equal(await evaluate("document.querySelectorAll('[data-reason]').length"),0);
  }
  await evaluate("window.mockAction='answer';document.querySelector('#actions button').click()");await wait("document.querySelector('#output').dataset.state==='answer'");
  await send('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
  await screenshot('mobile-answer-fixture');assert.equal(await evaluate('document.documentElement.scrollWidth<=390'),true,'Mobile horizontal overflow');
  await evaluate("window.fetch=window.realFetch;document.querySelector('#source').value='slides-d2';document.querySelector('#source').dispatchEvent(new Event('change'))");await wait("document.querySelectorAll('.page-row').length===29");assert.equal(await evaluate("document.querySelector('#selectionCount').textContent"),'0 / 3');
  if(process.argv.includes('--live')) {
    await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
    await evaluate("document.querySelector('#source').value='slides-d1';document.querySelector('#source').dispatchEvent(new Event('change'))");await wait("document.querySelectorAll('.page-row').length===29");
    await evaluate("document.querySelector('#askForm').requestSubmit()");
    for(let i=0;i<400;i++){if(await evaluate("!document.querySelector('#ask').disabled"))break;await new Promise(r=>setTimeout(r,100));}
    console.log('Live UI outcome:',await evaluate("document.querySelector('#output').dataset.state+' | '+document.querySelector('#meta').textContent"));
    assert.equal(await evaluate("document.querySelector('#output').dataset.state"),'answer','Live AI did not return answer');
    await evaluate("document.querySelector('#citations button').click()");await wait("!document.querySelector('#sourceView').hidden");await screenshot('desktop-live-answer');
  }
  console.log('UI browser checks passed: source validation, 3-page limit, filtered selection retention, real PDF link, loading lock, 4 actions, error/retry input retention, stale clarify cleanup, source switch, mobile overflow. Ask responses were TEST FIXTURES, no quality/live AI claim.');
} finally {if(socket)socket.close();browser.kill();}
