(function(){
  const qs = (s)=>document.querySelector(s);

  const params = new URLSearchParams(location.search);
  const state = {
    prompts: [], idx: 0, answers: {}, 
    variant: params.get('variant')||'A',
    widget: params.get('widget')||'none',
    queue: { answers: [], prompts: [] }
  };
  const storageKey = 'delta_ps101_progress_v2';

  function loadSaved(){
    try{ const raw = localStorage.getItem(storageKey); if(!raw) return;
      const saved = JSON.parse(raw); Object.assign(state, saved);
    }catch(_){}
  }
  function save(){ localStorage.setItem(storageKey, JSON.stringify({idx:state.idx, answers:state.answers, variant:state.variant, widget:state.widget, queue:state.queue})); renderSaved(); }
  function setStatus(m){ qs('#status').textContent = m||''; }
  function setCounter(){ qs('#counter').textContent = `${Math.min(state.idx+1,state.prompts.length)} / ${state.prompts.length}`; }
  function showPrompt(){ const p = state.prompts[state.idx] || "Done!"; qs('#prompt').textContent = p; qs('#answer').value = state.answers[state.idx]||''; setCounter(); }
  function renderSaved(){ qs('#savedDump').textContent = JSON.stringify({idx: state.idx, answers: state.answers}, null, 2); }

  async function loadPrompts(){
    try{
      const res = await fetch('data/prompts.ps101.json'); const json = await res.json();
      state.prompts = json.prompts || [];
      qs('#variantCode').textContent = state.variant;
      setStatus(`Loaded ${state.prompts.length} prompts.`);
      showPrompt(); renderSaved();
    }catch(e){ setStatus('Failed to load prompts file.'); }
  }

  function next(){
    const val = qs('#answer').value.trim();
    if(val) state.answers[state.idx] = val;
    if(state.idx < state.prompts.length - 1) state.idx++;
    save(); showPrompt();
  }
  function start(){ state.idx = 0; save(); showPrompt(); }
  function support(){
    const val = qs('#answer').value.trim();
    alert(window.DeltaCoach.nudge(val));
  }
  function exportJSON(){
    const blob = new Blob([JSON.stringify({answers: state.answers, variant: state.variant, timestamp: new Date().toISOString()}, null, 2)], {type:'application/json'});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'delta_progress.json'; a.click();
  }
  function fileSelected(file){
    const el = qs('#fileStatus'); if(!file){ el.textContent=''; return; }
    el.textContent = `Attached: ${file.name} (${(file.size/1024).toFixed(1)} KB)`;
  }

  async function submitAnswer(){
    const val = qs('#answer').value.trim();
    if(!val){ alert('Write something first.'); return; }
    const payload = {
      display_name: qs('#displayName').value || null,
      prompt_index: state.idx,
      prompt_text: state.prompts[state.idx] || null,
      answer_text: val,
      variant: state.variant,
      widget: state.widget
    };
    const res = await window.DeltaDB.submitAnswer(payload);
    if(res.ok){ alert('Submitted to community.'); }
    else if(res.queued){ state.queue.answers.push(payload); save(); alert('Saved locally. Will submit when DB is configured.'); }
    else { alert('Submission failed. See console.'); console.log(res.error); }
  }
  async function suggestPrompt(){
    const text = prompt('Enter your suggested prompt:'); if(!text) return;
    const payload = { display_name: qs('#displayName').value || null, suggestion: text, variant: state.variant, widget: state.widget };
    const res = await window.DeltaDB.suggestPrompt(payload);
    if(res.ok){ alert('Prompt suggestion submitted.'); }
    else if(res.queued){ state.queue.prompts.push(payload); save(); alert('Saved locally. Will submit when DB is configured.'); }
    else { alert('Suggestion failed.'); console.log(res.error); }
  }
  async function refreshInsights(){
    const res = await window.DeltaDB.aggregate();
    if(!res.ok){ qs('#insights').textContent = 'No serverless aggregate available yet.'; return; }
    qs('#insights').textContent = JSON.stringify(res.data, null, 2);
  }

  window.addEventListener('DOMContentLoaded', ()=>{
    loadSaved(); loadPrompts();
    qs('#btnStart').onclick = start;
    qs('#btnNext').onclick = next;
    qs('#btnSupport').onclick = support;
    qs('#btnExport').onclick = exportJSON;
    qs('#btnReset').onclick = ()=>{ localStorage.removeItem(storageKey); location.reload(); };
    qs('#fileInput').onchange = (e)=>fileSelected(e.target.files[0]);
    qs('#btnSubmitAnswer').onclick = submitAnswer;
    qs('#btnSuggestPrompt').onclick = suggestPrompt;
    qs('#btnRefreshInsights').onclick = refreshInsights;
  });
})();