(function(){
  const missing = typeof window.__ENV === 'undefined' || !window.__ENV.SUPABASE_URL || !window.__ENV.SUPABASE_ANON_KEY;
  let supa = null;
  async function ensure(){
    if(missing) return null;
    if(supa) return supa;
    await new Promise((res, rej)=>{
      const s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js';
      s.onload = res; s.onerror = rej; document.head.appendChild(s);
    });
    supa = window.supabase.createClient(window.__ENV.SUPABASE_URL, window.__ENV.SUPABASE_ANON_KEY);
    return supa;
  }
  async function submitAnswer(payload){
    const client = await ensure();
    if(!client) return { ok:false, queued:true, reason:'no-env' };
    const { data, error } = await client.from('contributions').insert(payload).select('*').single();
    if(error) return { ok:false, error };
    return { ok:true, data };
  }
  async function suggestPrompt(payload){
    const client = await ensure();
    if(!client) return { ok:false, queued:true, reason:'no-env' };
    const { data, error } = await client.from('prompt_suggestions').insert(payload).select('*').single();
    if(error) return { ok:false, error };
    return { ok:true, data };
  }
  async function aggregate(){
    try {
      const res = await fetch('/api/aggregate');
      if(!res.ok) return {ok:false};
      return { ok:true, data: await res.json() };
    } catch(_) { return {ok:false}; }
  }
  window.DeltaDB = { submitAnswer, suggestPrompt, aggregate, hasEnv: !missing };
})();