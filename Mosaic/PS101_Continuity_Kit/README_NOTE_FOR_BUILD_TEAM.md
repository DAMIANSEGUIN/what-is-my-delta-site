# PS101 Continuity & Disambiguation Hand-Off (2025-11-03)

This package is the definitive hand-off for the Mosaic PS101 build continuity system.
It contains manifests, CI/CD workflows, and helper scripts to maintain integrity across builds.

## Contents
- manifest.can.json — canonical manifest
- PS101_Continuity_Disambiguation_Plan_2025-11-03.md — rationale + diagnostic plan
- README_NOTE_FOR_BUILD_TEAM.md — quick setup & Nudge
- .github/workflows/ps101_gate.yml — mandatory CI gate
- .github/workflows/ps101_netlify_deploy.yml / ps101_railway_deploy.yml — CI deploys
- netlify.toml / RAILWAY_CONFIG_NOTE.md — platform configs
- inject_build_id.js / check_spec_hash.sh — helper scripts

## Nudge
Adopt the single gate + manifest + footer BUILD_ID immediately.
That one step prevents ≈ 90% of version drift and chaos across PS101 builds.
