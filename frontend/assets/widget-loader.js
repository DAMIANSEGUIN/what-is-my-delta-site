(function(){
  const params = new URLSearchParams(location.search);
  const widget = params.get('widget') || 'none';
  
  // Display current widget in footer
  const widgetCode = document.getElementById('widgetCode');
  if (widgetCode) widgetCode.textContent = widget;

  // Widget loading functions
  function loadCrispWidget() {
    window.$crisp = [];
    window.CRISP_WEBSITE_ID = "37669e51-8fd7-4b2b-8c69-9a008bb9b0c6";
    const script = document.createElement("script");
    script.src = "https://client.crisp.chat/l.js";
    script.async = true;
    document.getElementsByTagName("head")[0].appendChild(script);
    console.log('Crisp widget loaded');
  }

  function loadTidioWidget() {
    const script = document.createElement("script");
    script.src = "//code.tidio.co/n1vonfqtzyrhkdd2k4k9k9oq7ve6p7dv.js";
    script.async = true;
    document.body.appendChild(script);
    console.log('Tidio widget loaded');
  }

  function loadTawkWidget() {
    var Tawk_API = Tawk_API || {};
    var Tawk_LoadStart = new Date();
    const script = document.createElement("script");
    script.async = true;
    script.src = "https://embed.tawk.to/68a767d97ebce11927982120/1j36uravb";
    script.charset = "UTF-8";
    script.setAttribute("crossorigin", "*");
    document.body.appendChild(script);
    window.Tawk_API = Tawk_API;
    window.Tawk_LoadStart = Tawk_LoadStart;
    console.log('Tawk.to widget loaded');
  }

  // Voiceflow removed - requires paid plan for external embedding

  // Load selected widget
  switch (widget) {
    case 'crisp':
      loadCrispWidget();
      break;
    case 'tidio':
      loadTidioWidget();
      break;
    case 'tawk':
      loadTawkWidget();
      break;
    case 'none':
    default:
      console.log('No chat widget loaded');
      break;
  }

  // Update CSP dynamically based on widget
  function updateCSP() {
    const meta = document.querySelector('meta[http-equiv="Content-Security-Policy-Report-Only"]');
    if (!meta) return;

    let csp = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'";
    
    switch (widget) {
      case 'crisp':
        csp += " https://client.crisp.chat https://*.crisp.chat";
        csp += "; connect-src 'self' https://*.supabase.co wss://*.crisp.chat https://*.crisp.chat";
        csp += "; img-src 'self' data: https://*.crisp.chat";
        csp += "; frame-src https://*.crisp.chat";
        break;
      case 'tidio':
        csp += " https://code.tidio.co https://*.tidio.co";
        csp += "; connect-src 'self' https://*.supabase.co wss://*.tidio.co https://*.tidio.co";
        csp += "; img-src 'self' data: https://*.tidio.co";
        break;
      case 'tawk':
        csp += " https://embed.tawk.to https://*.tawk.to";
        csp += "; connect-src 'self' https://*.supabase.co wss://*.tawk.to https://*.tawk.to";
        csp += "; img-src 'self' data: https://*.tawk.to";
        break;
      default:
        csp += "; connect-src 'self' https://*.supabase.co";
    }
    
    csp += "; style-src 'self' 'unsafe-inline'; img-src 'self' data:; report-uri /csp-report";
    meta.setAttribute('content', csp);
  }

  updateCSP();

  // Expose widget info globally
  window.DeltaWidget = {
    current: widget,
    available: ['none', 'crisp', 'tidio', 'tawk'],
    switchTo: function(newWidget) {
      const url = new URL(location);
      if (newWidget === 'none') {
        url.searchParams.delete('widget');
      } else {
        url.searchParams.set('widget', newWidget);
      }
      location.href = url.toString();
    }
  };
})();