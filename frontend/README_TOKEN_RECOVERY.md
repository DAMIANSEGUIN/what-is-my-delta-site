# TOKEN RECOVERY README

## IMMEDIATE PRIORITY - SESSION CONTINUATION

**Status**: Ask functionality 100% broken due to CSV parsing failure in CoachVox AI system

## EXACT ISSUE LOCATION
- **File**: `/Users/damianseguin/Documents/what_is_my_delta_site/index.html`
- **Line**: 571 
- **Problem**: `line.split(',')` breaks CoachVox AI CSV with embedded commas

## 30-SECOND FIX
Replace line 571 with proper CSV parsing:

```javascript
// BROKEN:
const [prompt, completion, labels] = line.split(',').map(s => s.replace(/^"|"$/g, '').trim());

// FIX:
function parseCSVLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      result.push(current.trim().replace(/^"|"$/g, ''));
      current = '';
    } else {
      current += char;
    }
  }
  result.push(current.trim().replace(/^"|"$/g, ''));
  return result;
}
const [prompt, completion, labels] = parseCSVLine(line);
```

## DEPLOY
```bash
netlify deploy --site=bb594f69-4d23-4817-b7de-dadb8b4db874 --auth=nfp_KfjJx2FFoANpnQSyD9rnb8RWExzfkpLb65a0 --prod --dir=.
```

## TEST
- Go to https://whatismydelta.com
- Type "i need a job"
- Click ask
- Should get CoachVox AI coaching response

**Everything else works - only CSV parsing is broken.**

## FULL CONTEXT
- See: `SENIOR_ENGINEER_HANDOFF.md` for complete analysis
- See: `ARCHITECTURE_CONTEXT.md` for CoachVox AI details