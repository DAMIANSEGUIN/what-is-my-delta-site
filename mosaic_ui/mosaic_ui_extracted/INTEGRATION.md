# INTEGRATION.md

## Backend base
`https://mosaic-platform.vercel.app`

## Chat (coach)
POST `/wimd`
Body:
```json
{ "prompt": "..." }
```
Client snippet (replace in index.html):
```js
async function askCoach(prompt){
  const res = await fetch('https://mosaic-platform.vercel.app/wimd', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ prompt })
  });
  const data = await res.json();
  return data?.result?.message || '(no response)';
}
```

## Upload
POST `/wimd/upload` (FormData; field `file`)
```js
document.getElementById('filePick').addEventListener('change', async (e) => {
  const f = e.target.files?.[0]; if(!f) return;
  const form = new FormData(); form.append('file', f);
  const res = await fetch('https://mosaic-platform.vercel.app/wimd/upload', { method:'POST', body: form });
  const data = await res.json();
  // do something with response
});
```

## Opportunities & Job Search (optional later)
- POST `/wimd/opportunities`
- POST `/jobsearch`
