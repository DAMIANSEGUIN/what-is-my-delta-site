window.DeltaCoach = (function(){
  function nudge(text){
    const len = (text||'').trim().length;
    if(len === 0) return "Try writing 1–2 sentences describing your current state.";
    if(len < 60) return "Name your desired state in one sentence, then the obstacle in one more.";
    if(len < 160) return "Good. Add one concrete action you can take in the next 48 hours.";
    return "Solid depth. Now add a measurable outcome and a date.";
  }
  function summarize(text){
    const s = (text||'').trim();
    if(!s) return "No input yet.";
    return s.split(/[.!?]/).slice(0,2).join('. ').trim();
  }
  return { nudge, summarize };
})();