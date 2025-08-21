
(function(){
  const params = new URLSearchParams(location.search);
  let variant = (params.get('variant') || 'A').toUpperCase() === 'B' ? 'B' : 'A';
  const variantLabel = document.getElementById('variant-label');
  variantLabel.textContent = variant;
  document.getElementById('setA').onclick = ()=>{ location.search='?variant=A' }
  document.getElementById('setB').onclick = ()=>{ location.search='?variant=B' }

  // Core PS101 steps (summarized prompts)
  const STEPS = [
    { id:'problem', title:'1) Problem Identification & Delta', fields:[
      {key:'challenge', label:'What specific challenge are you facing?', type:'textarea'},
      {key:'why_problem', label:'Why is it a problem?', type:'textarea'},
      {key:'problem_statement', label:'Reduce to a simple problem statement', type:'textarea'},
      {key:'miracle', label:'Miracle Question: If it were solved tomorrow, what would be different?', type:'textarea'},
      {key:'delta', label:'What is the gap (delta) between current and desired?', type:'textarea'},
      {key:'alignment', label:'How does solving this align with your long-term goals/values?', type:'textarea'}
    ]},
    { id:'current', title:'2) Current Situation', fields:[
      {key:'current_desc', label:'Describe your current situation. What factors contribute?', type:'textarea'},
      {key:'attempts', label:'What have you tried so far? Outcomes?', type:'textarea'},
      {key:'patterns', label:'Patterns or recurring themes?', type:'textarea'},
      {key:'impact', label:'Impact on career/relationships/personal growth?', type:'textarea'}
    ]},
    { id:'root', title:'3) Root Cause (5 Whys)', fields:[
      {key:'root_causes', label:'What do you believe are the underlying causes?', type:'textarea'},
      {key:'assumptions', label:'Any assumptions you might be making?', type:'textarea'},
      {key:'beliefs', label:'Beliefs/habits/experiences contributing?', type:'textarea'},
      {key:'outsider', label:'If you were an outsider, what would you notice?', type:'textarea'}
    ]},
    { id:'selfeff', title:'4) Self-Efficacy', fields:[
      {key:'confidence', label:'Confidence (1–10) and why?', type:'text'},
      {key:'past_skills', label:'Past experiences or skills to draw on', type:'textarea'},
      {key:'capability_view', label:'How does your capability perception affect approach?', type:'textarea'},
      {key:'micro_wins', label:'Past small wins you can build on', type:'textarea'}
    ]},
    { id:'solutions', title:'5) Solutions Brainstorm', fields:[
      {key:'ideas', label:'List at least five potential solutions (one per line)', type:'textarea'},
      {key:'benefits_drawbacks', label:'Benefits and drawbacks of each (map line-by-line if possible)', type:'textarea'},
      {key:'aligned_choice', label:'Which solution aligns most with your values/goals?', type:'textarea'},
      {key:'hybrid', label:'Combine elements into a comprehensive approach', type:'textarea'}
    ]},
    { id:'experiment', title:'6) Experimental Design', fields:[
      {key:'small_experiment', label:'Define a small, low-risk experiment', type:'textarea'},
      {key:'success_metric', label:'Measurable outcome indicating success', type:'textarea'},
      {key:'resources', label:'Resources/support needed', type:'textarea'},
      {key:'duration', label:'How long will you run the experiment?', type:'text'}
    ]},
    { id:'obstacles', title:'7) Obstacles', fields:[
      {key:'external', label:'External factors that could hinder progress', type:'textarea'},
      {key:'internal', label:'Internal obstacles (self-doubt, fear, knowledge gaps)', type:'textarea'},
      {key:'mitigations', label:'Strategies to overcome/mitigate obstacles', type:'textarea'},
      {key:'reframe', label:'Reframe obstacles as opportunities for growth', type:'textarea'}
    ]},
    { id:'action', title:'8) Action Plan', fields:[
      {key:'steps', label:'Specific steps to implement the experiment', type:'textarea'},
      {key:'tracking', label:'How you will measure/track progress', type:'textarea'},
      {key:'milestones', label:'Milestones to celebrate small wins', type:'textarea'},
      {key:'accountability', label:'Who will support or hold you accountable?', type:'textarea'}
    ]},
    { id:'reflection', title:'9) Reflection & Iteration', fields:[
      {key:'results', label:'Results and learnings', type:'textarea'},
      {key:'confidence_change', label:'Effect on your confidence', type:'textarea'},
      {key:'adjustments', label:'Adjustments you will make', type:'textarea'},
      {key:'new_actions', label:'New experiments/actions you will take', type:'textarea'}
    ]},
    { id:'mastery', title:'10) Mastery & Commitment', fields:[
      {key:'skills_gained', label:'New skills or knowledge gained', type:'textarea'},
      {key:'apply_future', label:'How you will apply this in future', type:'textarea'},
      {key:'momentum', label:'Strategies to maintain momentum', type:'textarea'},
      {key:'self_view', label:'How has your self-view changed?', type:'textarea'},
      {key:'commitment', label:'What specific actions will you commit to this week?', type:'textarea'},
      {key:'hold_accountable', label:'How will you hold yourself accountable?', type:'textarea'},
      {key:'share_plan', label:'Who will you share your plan with?', type:'textarea'}
    ]}
  ];

  // Session state
  let state = JSON.parse(localStorage.getItem('delta_session') || '{}');

  function save(){
    localStorage.setItem('delta_session', JSON.stringify(state));
  }

  function el(tag, attrs={}, children=[]){
    const n = document.createElement(tag);
    for (const [k,v] of Object.entries(attrs)){
      if (k==='class') n.className = v;
      else if (k==='text') n.textContent = v;
      else n.setAttribute(k,v);
    }
    (Array.isArray(children)?children:[children]).forEach(c => {
      if (c==null) return;
      if (typeof c === 'string') n.appendChild(document.createTextNode(c));
      else n.appendChild(c);
    });
    return n;
  }

  function renderField(stepId, f){
    const id = `${stepId}.${f.key}`;
    const val = state[id] || '';
    const label = el('label', {for:id, text:f.label});
    let input;
    if (f.type==='textarea'){
      input = el('textarea', {id, rows:'5'});
      input.value = val;
      input.oninput = () => { state[id] = input.value; save(); };
    } else {
      input = el('input', {id, type:f.type || 'text', class:'input'});
      input.value = val;
      input.oninput = () => { state[id] = input.value; save(); };
    }
    return el('div', {}, [label, input]);
  }

  function renderStep(step, index){
    const wrap = el('div', {class:'step'});
    wrap.appendChild(el('div', {class:'step-title'}, [
      el('span', {class:'badge', text:`Step ${index+1}`}), ' ',
      el('span', {text:' ' + step.title})
    ]));
    step.fields.forEach(f => wrap.appendChild(renderField(step.id, f)));
    return wrap;
  }

  function renderWizard(){
    const root = document.getElementById('flow-root');
    root.innerHTML = '';

    if (variant === 'A'){
      // Linear multi-step with next/back
      let i = 0;
      const total = STEPS.length;

      function show(){
        root.innerHTML = '';
        root.appendChild(renderStep(STEPS[i], i));

        const nav = el('div', {class:'nav'}, [
          el('div', {}, [
            el('button', {class:'btn btn-secondary', id:'back'}, 'Back'),
          ]),
          el('div', {}, [
            el('button', {class:'btn', id:'ask'}, 'Ask my own question'),
            el('button', {class:'btn', id:'clarify'}, 'AI clarifying questions'),
            el('button', {class:'btn', id:'next'}, i===total-1 ? 'Finish' : 'Next')
          ])
        ]);
        root.appendChild(nav);

        document.getElementById('back').onclick = ()=>{ i=Math.max(0, i-1); show(); }
        document.getElementById('next').onclick = ()=>{ i=Math.min(total-1, i+1); show(); }
        document.getElementById('ask').onclick = ()=> openPrompt('ask');
        document.getElementById('clarify').onclick = ()=> openPrompt('clarify');
      }
      show();
    } else {
      // Variant B: conversational cards (progressive disclosure)
      const intro = el('div', {class:'step'}, [
        el('div', {class:'step-title', text:'Let’s locate your Delta.'}),
        el('p', {}, 'We’ll move in small, clear steps. You can switch tracks anytime.')
      ]);
      root.appendChild(intro);

      const choices = el('div', {class:'row'}, [
        el('button', {class:'btn', id:'start-problem'}, 'Start with Problem Statement'),
        el('button', {class:'btn', id:'start-experiment'}, 'Jump to Small Experiment'),
        el('button', {class:'btn', id:'start-ask'}, 'Ask my own question'),
        el('button', {class:'btn', id:'start-clarify'}, 'AI clarifying questions')
      ]);
      root.appendChild(choices);

      document.getElementById('start-problem').onclick = ()=> mountSubset(['problem','current','root']);
      document.getElementById('start-experiment').onclick = ()=> mountSubset(['experiment','action','obstacles']);
      document.getElementById('start-ask').onclick = ()=> openPrompt('ask');
      document.getElementById('start-clarify').onclick = ()=> openPrompt('clarify');
    }
  }

  function mountSubset(ids){
    const root = document.getElementById('flow-root');
    const subset = STEPS.filter(s => ids.includes(s.id));
    subset.forEach((s, i) => root.appendChild(renderStep(s, i)));
  }

  function openPrompt(mode){
    const q = prompt(mode==='ask' ? 'Type your question:' : 'Tell me a bit more, and I’ll suggest the next clarifying questions:');
    if (!q) return;
    const key = `prompt.${mode}`;
    const arr = JSON.parse(state[key] || '[]');
    arr.push({t: Date.now(), text: q});
    state[key] = JSON.stringify(arr);
    save();
    alert('Saved. (This is a placeholder — your chat embed will handle real-time AI responses once added.)');
  }

  function exportMarkdown(){
    const lines = [];
    const dt = new Date().toISOString();
    lines.push(`# What is my Delta?`);
    lines.push(`_Exported: ${dt}_`);
    lines.push('');

    const groups = {};
    Object.keys(state).forEach(k=>{
      if (k.startsWith('prompt.')) return;
      const [stepKey, fieldKey] = k.split('.');
      groups[stepKey] = groups[stepKey] || {};
      groups[stepKey][fieldKey] = state[k];
    });

    const stepMap = Object.fromEntries(STEPS.map(s => [s.id, s.title]));

    Object.keys(groups).forEach(stepId => {
      lines.push(`## ${stepMap[stepId] || stepId}`);
      const fields = groups[stepId];
      Object.keys(fields).forEach(fk => {
        const val = (fields[fk]||'').trim();
        if (val) {
          lines.push(`**${fk.replace(/_/g,' ')}**`);
          lines.push('');
          lines.push(val);
          lines.push('');
        }
      });
      lines.push('');
    });

    // Prompts
    const ask = JSON.parse(state['prompt.ask'] || '[]');
    const clarify = JSON.parse(state['prompt.clarify'] || '[]');
    if (ask.length || clarify.length){
      lines.push('## Prompts');
      if (ask.length){
        lines.push('### Asked Questions');
        ask.forEach((p,i)=> lines.push(`- ${new Date(p.t).toLocaleString()}: ${p.text}`));
      }
      if (clarify.length){
        lines.push('### Clarifying Inputs');
        clarify.forEach((p,i)=> lines.push(`- ${new Date(p.t).toLocaleString()}: ${p.text}`));
      }
    }

    const blob = new Blob([lines.join('\n')], {type:'text/markdown'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'what_is_my_delta_session.md';
    a.click();
    setTimeout(()=>URL.revokeObjectURL(url), 5000);
  }

  // ---- CSV Library (local or bundled) ----
  const csvFile = document.getElementById('csv-file');
  const csvStatus = document.getElementById('csv-status');
  const csvPreview = document.getElementById('csv-preview');
  const clearCsvBtn = document.getElementById('clear-csv');

  function csvRenderPreview(rows){
    csvPreview.innerHTML = '';
    if (!rows || !rows.length){ return; }
    const table = el('table', {class:'table'});
    const thead = el('thead');
    const headerRow = el('tr');
    const cols = Object.keys(rows[0]);
    cols.forEach(c => headerRow.appendChild(el('th', {text:c})));
    thead.appendChild(headerRow);
    table.appendChild(thead);
    const tbody = el('tbody');
    rows.slice(0,5).forEach(r => {
      const tr = el('tr');
      cols.forEach(c => tr.appendChild(el('td', {text: (r[c]||'').toString().slice(0,200)})));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    csvPreview.appendChild(table);
  }

  function csvLoadFromState(){
    try {
      const saved = JSON.parse(state['csv.prompts'] || '[]');
      if (saved.length){
        if (csvStatus) csvStatus.textContent = `Loaded ${saved.length} rows from previous session.`;
        if (csvPreview) csvRenderPreview(saved);
      } else {
        if (csvStatus) csvStatus.textContent = `No CSV loaded.`;
      }
    } catch(e){
      if (csvStatus) csvStatus.textContent = `No CSV loaded.`;
    }
  }

  async function tryLoadBundledCsv(){
    try{
      const resp = await fetch('assets/prompts.csv', { cache: 'no-store' });
      if (!resp.ok) return;
      const text = await resp.text();
      if (!text || !text.trim()) return;
      if (window.Papa){
        const parsed = Papa.parse(text, { header: true, skipEmptyLines: true });
        const rows = (parsed && parsed.data) ? parsed.data : [];
        if (rows.length){
          state['csv.prompts'] = JSON.stringify(rows);
          save();
          if (csvStatus) csvStatus.textContent = `Auto-loaded ${rows.length} rows from bundled CSV.`;
          if (csvPreview) csvRenderPreview(rows);
        }
      }
    } catch(e){
      // ignore if missing
    }
  }

  if (csvFile){
    csvFile.addEventListener('change', (e)=>{
      const file = e.target.files && e.target.files[0];
      if (!file){ return; }
      if (csvStatus) csvStatus.textContent = 'Parsing...';
      if (window.Papa){
        Papa.parse(file, {
          header: true,
          skipEmptyLines: true,
          complete: (res)=>{
            const rows = (res && res.data) ? res.data : [];
            state['csv.prompts'] = JSON.stringify(rows);
            save();
            if (csvStatus) csvStatus.textContent = `Loaded ${rows.length} rows.`;
            if (csvPreview) csvRenderPreview(rows);
          },
          error: (err)=>{
            if (csvStatus) csvStatus.textContent = `Parse error: ${err && err.message ? err.message : err}`;
          }
        });
      } else {
        if (csvStatus) csvStatus.textContent = 'Papa Parse not available.';
      }
    });
  }

  if (clearCsvBtn){
    clearCsvBtn.addEventListener('click', ()=>{
      delete state['csv.prompts'];
      save();
      if (csvStatus) csvStatus.textContent = 'Cleared.';
      if (csvPreview) csvPreview.innerHTML = '';
      if (csvFile) csvFile.value = '';
    });
  }

  document.getElementById('export-md').onclick = exportMarkdown;
  document.getElementById('reset').onclick = ()=>{
    if (confirm('Clear saved session?')){
      localStorage.removeItem('delta_session');
      location.reload();
    }
  };

  csvLoadFromState();
  tryLoadBundledCsv();

  // ---- Consent & Data Use ----
  const optPersonal = document.getElementById('opt-personal');
  const optShare = document.getElementById('opt-share');
  const optEmail = document.getElementById('opt-email');
  const consentStatus = document.getElementById('consent-status');

  function consentLoad(){
    const c = JSON.parse(localStorage.getItem('delta_consent') || '{}');
    if (optPersonal) optPersonal.checked = !!c.personal;
    if (optShare) optShare.checked = !!c.share;
    if (optEmail) optEmail.checked = !!c.email;
    if (consentStatus) consentStatus.textContent = 'Preferences are saved locally and can be changed anytime.';
  }
  function consentSave(){
    const c = {
      personal: optPersonal && optPersonal.checked,
      share: optShare && optShare.checked,
      email: optEmail && optEmail.checked
    };
    localStorage.setItem('delta_consent', JSON.stringify(c));
  }
  [optPersonal,optShare,optEmail].forEach(el=> el && el.addEventListener('change', consentSave));
  consentLoad();

  // ---- Extra Exports ----
  function exportJSON(){
    const blob = new Blob([JSON.stringify(state, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'what_is_my_delta_session.json'; a.click();
    setTimeout(()=>URL.revokeObjectURL(url), 5000);
  }
  function exportTranscript(){
    const lines = [];
    const dt = new Date().toISOString();
    lines.push(`# What is my Delta — Transcript`);
    lines.push(`_Exported: ${dt}_`);
    lines.push('');

    function addBlock(title, arr){
      if (!arr || !arr.length) return;
      lines.push(`## ${title}`);
      arr.forEach(p => {
        const ts = new Date(p.t || Date.now()).toLocaleString();
        lines.push(`- **${ts}** — ${p.text}`);
      });
      lines.push('');
    }

    // Build from state
    const ask = JSON.parse(state['prompt.ask'] || '[]');
    const clarify = JSON.parse(state['prompt.clarify'] || '[]');
    addBlock('Asked Questions', ask);
    addBlock('Clarifying Inputs', clarify);

    // Include key PS101 fields as a compact summary
    const important = ['problem.challenge','problem.problem_statement','root.root_causes','experiment.small_experiment','action.steps'];
    lines.push('## Summary');
    important.forEach(key => {
      const v = (state[key] || '').trim();
      if (v) lines.push(`- **${key.replace('.',' → ')}**: ${v}`);
    });

    const blob = new Blob([lines.join('\n')], {type:'text/markdown'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'Transcript.md'; a.click();
    setTimeout(()=>URL.revokeObjectURL(url), 5000);
  }

  const exportJsonBtn = document.getElementById('export-json');
  const exportMd2Btn = document.getElementById('export-md2');
  exportJsonBtn && (exportJsonBtn.onclick = exportJSON);
  exportMd2Btn && (exportMd2Btn.onclick = exportTranscript);

  // ---- Prompt Library Viewer ----
  const pvSearch = document.getElementById('pv-search');
  const pvTable = document.getElementById('pv-table');
  const pvCount = document.getElementById('pv-count');

  function getPrompts(){
    try { return JSON.parse(state['csv.prompts'] || '[]'); }
    catch(e){ return []; }
  }
  function renderPromptTable(rows){
    pvTable.innerHTML = '';
    const table = el('table', {class:'table'});
    const thead = el('thead');
    const hr = el('tr');
    ['prompt','completion'].forEach(h => hr.appendChild(el('th', {text:h})));
    thead.appendChild(hr);
    table.appendChild(thead);
    const tbody = el('tbody');
    rows.forEach(r => {
      const tr = el('tr');
      tr.appendChild(el('td', {text: (r.prompt||'').toString().slice(0,500)}));
      tr.appendChild(el('td', {text: (r.completion||'').toString().slice(0,500)}));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    pvTable.appendChild(table);
  }
  function updateViewer(){
    const all = getPrompts();
    const q = (pvSearch && pvSearch.value || '').toLowerCase();
    const filtered = q ? all.filter(r => (r.prompt||'').toLowerCase().includes(q) || (r.completion||'').toLowerCase().includes(q)) : all;
    if (pvCount) pvCount.textContent = `${filtered.length} / ${all.length} rows`;
    renderPromptTable(filtered.slice(0, 500)); // cap to keep UI snappy
  }
  pvSearch && pvSearch.addEventListener('input', updateViewer);

  // Initialize viewer after CSV loads
  setTimeout(updateViewer, 300);

  renderWizard();
})();
