#!/bin/bash

# Claude Code Context Script
echo "🤖 Setting up Claude Code context..."
cd /Users/damianseguin/Documents/what_is_my_delta_site
pwd

echo ""
echo "📋 PROJECT CONTEXT:"
echo "==================="
cat CLAUDE.md 2>/dev/null || echo "No CLAUDE.md found - first time setup needed"

echo ""
echo "📝 RECENT GIT HISTORY:"
echo "====================="
git log --oneline -5 2>/dev/null || echo "Not a git repo"

echo ""
echo "🔍 CURRENT STATUS:"  
echo "=================="
git status 2>/dev/null || echo "Not a git repo"

echo ""
echo "✨ Ready! Claude should now be briefed on previous work."
echo "Just paste this output to Claude Code to get context."