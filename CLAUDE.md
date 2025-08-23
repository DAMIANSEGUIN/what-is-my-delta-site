# Claude Context File

## Current Session Work (2025-08-23)
- Working on: Vercel deployment sync and widget functionality issues  
- Status: 🚨 **CRITICAL ISSUE**: Vercel serving wrong/old index.html file
- Next steps: Fix deployment sync - live site doesn't match repository code

## Development Commands
- Test locally: Open index.html in browser
- Deploy: Auto-deploys via Vercel on git push
- Widget testing URLs:
  - Clean: https://what-is-my-delta.vercel.app/
  - Crisp: https://what-is-my-delta.vercel.app/?widget=crisp
  - Tidio: https://what-is-my-delta.vercel.app/?widget=tidio
  - Tawk: https://what-is-my-delta.vercel.app/?widget=tawk

## Previous Issues RESOLVED
- ✅ Vercel deployment configuration (converted from Next.js to static)
- ✅ GitHub Actions workflow conflicts (removed empty workflow)
- ✅ vercel.json routing conflicts (simplified config)

## Widget Implementation Status
- ✅ Dynamic widget loader implemented
- ✅ CSP configuration per widget
- ✅ URL parameter detection
- ✅ Three widgets: Crisp, Tidio, Tawk.to
- ❓ Need to verify widgets display correctly on live site

## Recent Git History
- 8b3fcce: Force correct index.html deployment - update title
- 79f5376: Force deployment refresh - update README with widget testing info  
- da9fc80: Configure vercel.json for static site deployment