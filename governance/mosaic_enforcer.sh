#!/bin/zsh
set -euo pipefail

input="$(cat)"

forbidden="Translation Engine acknowledged. Session bootstrapped. Awaiting deterministic input."
if /usr/bin/printf "%s" "$input" | /usr/bin/grep -Fq "$forbidden"; then
  /usr/bin/printf "%s\n" "REJECT"
  exit 2
fi

need_headers=("CURRENT STATE" "PLAN" "ACCEPTANCE GATES" "CHECKPOINT PACKET")
for h in "${need_headers[@]}"; do
  /usr/bin/printf "%s" "$input" | /usr/bin/grep -Fq "$h" || { /usr/bin/printf "%s\n" "REJECT"; exit 2; }
done

/usr/bin/printf "%s\n" "ALLOW"
exit 0

