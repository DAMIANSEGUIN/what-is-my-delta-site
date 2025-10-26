---
rubric_key: Mosaic_Redesign_AdaptiveFramework_v1
doc_role: holographic_readme
project: Mosaic
created: '2025-10-26 17:27:30'
holographic_structure: one-page source of truth; embeds a compact map so any copy can recreate the whole
placement:
  - Drive:/Mosaic/
  - Drive:/Planning/
principles:
  - minimal_docs_only
  - overwrite_obsolete_immediately
  - single_source_truth: HOLO_README.md + manifest.json
  - agent_discoverable: yaml front-matter + json-ld
  - calm_language_only
---

# Mosaic – Holographic README (Minimal & Overwrite-First)

This page is the **only required documentation**. Any agent or human can rebuild the doc tree from here.

## Canon (search by exact title)
- Strategic_Systems_Integration_Plan_v0.2 → architecture roadmap
- README_Plan_Archive_v1.1_full → restore & backup rules
- Planning_Responses_Rebuild_v1.2 → system-memory continuity
- Career_Pathing_Prompts → reflection prompts & evidence
- START Planning_Checklist_16.10.25 → task sequence
- Nate_Skills_Framework_v3.1.pdf → Adaptive Growth Matrix
- Nate_Skills_Framework_Notes_Mosaic_v2.pdf → Mosaic mapping
- Nate_Skills_Design_Cognition.pdf → cognitive ergonomics
- Nate_Skills_Objective_Matrix.xlsx → weighting matrix

## Overwrite Protocol (obsolescence control)
- Newer version present → **overwrite** filename in place.
- Only one README: **HOLO_README.md** (this file) in `/Mosaic/`.
- Only one manifest: **manifest.json** in `/Mosaic/`.
- Any extra docs are **staged** to `/Mosaic/Archive/` with a timestamp.

## Awareness Protocol (where things belong)
- `/Mosaic/` — active canon (current files only)
- `/Planning/` — planning mirrors (same filenames)
- `/Mosaic/Frameworks/` — Nate Framework artifacts
- `/Mosaic/Prompts/` — prompt bundles
- `/Mosaic/Archive/` — auto-moved superseded copies

## Holographic Map (compact)
If this file is all you have:
1. Create the directories above.
2. Fetch the canon by exact title (Drive or restore).
3. Place, then run `mosaic_auto_attach.command` to stamp metadata.

## UX Architecture (one-paragraph summary)
Sense → Decide → Render, with state tokens (calm, focus, recovery, explore). No UI forks. Feature flags gate density. Minimal motion. Calm.

---

<!-- JSON-LD for agent auto-attach -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CreativeWork",
  "name": "Mosaic – Holographic README",
  "identifier": "Mosaic_Redesign_AdaptiveFramework_v1",
  "dateCreated": "2025-10-26 17:27:30",
  "keywords": ["holographic", "overwrite-first", "minimal docs", "Mosaic", "calm UX"],
  "isPartOf": { "@type": "Dataset", "name": "Mosaic" }
}
</script>
