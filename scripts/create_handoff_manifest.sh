#!/bin/bash
# Generate machine-readable handoff state

cat <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "outgoing_agent": "${AI_AGENT_NAME:-Claude-Code}",
  "git_state": {
    "commit": "$(git rev-parse HEAD)",
    "branch": "$(git rev-parse --abbrev-ref HEAD)",
    "uncommitted_changes": $(git status --porcelain | wc -l | tr -d ' ')
  },
  "critical_features": {
    "auth_ui_present": $(grep -c "authModal\|loginForm" frontend/index.html mosaic_ui/index.html 2>/dev/null || echo 0),
    "ps101_state_count": $(grep -c "PS101State" frontend/index.html mosaic_ui/index.html 2>/dev/null || echo 0),
    "api_base_configured": $(grep -c "API_BASE = ''" frontend/index.html mosaic_ui/index.html 2>/dev/null || echo 0)
  },
  "deployment_status": {
    "railway_health": "$(curl -s -m 5 https://what-is-my-delta-site-production.up.railway.app/health 2>/dev/null | jq -r '.ok' 2>/dev/null || echo 'unknown')",
    "production_auth_present": $(curl -s -m 5 https://whatismydelta.com/ 2>/dev/null | grep -c "authModal\|loginForm" || echo 0)
  },
  "last_commit": {
    "message": $(git log -1 --pretty=format:'"%s"'),
    "author": $(git log -1 --pretty=format:'"%an"'),
    "timestamp": "$(git log -1 --pretty=format:'%aI')"
  },
  "tasks_in_progress": [
    "See git status and recent commits for current work"
  ],
  "notes": "Next agent: Run ./scripts/verify_critical_features.sh before proceeding"
}
EOF
