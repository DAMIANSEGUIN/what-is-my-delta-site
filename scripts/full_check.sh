#!/bin/bash
# Full system check including tests
# Usage: ./scripts/full_check.sh

set -e

echo "=== Mosaic 2.0 Full System Check ==="

# Run pre-deploy sanity check
echo "Running pre-deploy sanity check..."
./scripts/predeploy_sanity.sh

# Run test suite
echo "Running test suite..."
cd tests
python3 -m unittest discover -v
cd ..

# Check cost controls
echo "Checking cost controls..."
python3 -c "
from api.cost_controls import get_usage_analytics
analytics = get_usage_analytics()
print(f'Cost controls status: {analytics[\"status\"]}')
"

# Check RAG engine
echo "Checking RAG engine..."
python3 -c "
from api.rag_engine import get_rag_health
health = get_rag_health()
print(f'RAG engine status: {health[\"status\"]}')
"

# Check job sources
echo "Checking job sources..."
python3 -c "
from api.job_sources import GreenhouseSource, SerpApiSource, RedditSource
sources = [GreenhouseSource(), SerpApiSource(), RedditSource()]
for source in sources:
    health = source.get_health_status()
    print(f'{source.name}: {health[\"name\"]} - Rate limited: {health[\"rate_limited\"]}')
"

echo "=== Full system check complete ==="
