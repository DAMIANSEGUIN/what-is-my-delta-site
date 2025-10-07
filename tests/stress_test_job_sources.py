#!/usr/bin/env python3
"""
Stress Test: 12 Job Sources with Synthetic Persona Cohort
Tests all job sources with realistic user queries based on persona framework
"""

import json
import sys
import time
import requests
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass, asdict

# Base API URL
API_BASE = "https://what-is-my-delta-site-production.up.railway.app"

@dataclass
class TestPersona:
    """Simplified persona for job search testing"""
    id: str
    name: str
    query: str  # Job search query
    location: str
    expected_sources: int  # Minimum sources that should return results
    maslow_level: str
    career_stage: str

@dataclass
class SourceTestResult:
    """Results from testing a single job source"""
    source_name: str
    query: str
    success: bool
    jobs_returned: int
    response_time_ms: float
    error_message: str = None

@dataclass
class PersonaTestResult:
    """Aggregated results for one persona's test run"""
    persona_id: str
    persona_name: str
    query: str
    location: str
    total_sources_tested: int
    sources_succeeded: int
    sources_failed: int
    total_jobs_found: int
    avg_response_time_ms: float
    source_results: List[SourceTestResult]

# Test persona cohort covering diverse search patterns
TEST_PERSONAS = [
    TestPersona(
        id="tech_professional",
        name="Sarah Chen - Senior Engineer",
        query="software engineer",
        location="San Francisco, CA",
        expected_sources=8,  # Most sources have tech jobs
        maslow_level="esteem",
        career_stage="senior"
    ),
    TestPersona(
        id="career_changer",
        name="Marcus Thompson - Career Transition",
        query="project manager",
        location="Austin, TX",
        expected_sources=6,
        maslow_level="belonging",
        career_stage="transition"
    ),
    TestPersona(
        id="remote_seeker",
        name="Elena Rodriguez - Remote Worker",
        query="data analyst remote",
        location="",
        expected_sources=7,  # Remote-focused sources should hit
        maslow_level="safety",
        career_stage="mid"
    ),
    TestPersona(
        id="entry_level",
        name="Jordan Kim - Recent Graduate",
        query="marketing coordinator",
        location="New York, NY",
        expected_sources=5,
        maslow_level="belonging",
        career_stage="entry"
    ),
    TestPersona(
        id="specialized",
        name="Dr. Aisha Patel - Specialist",
        query="data scientist machine learning",
        location="Seattle, WA",
        expected_sources=6,
        maslow_level="self_actualization",
        career_stage="senior"
    ),
    TestPersona(
        id="underemployed",
        name="James Martinez - Seeking Stability",
        query="full time warehouse",
        location="Chicago, IL",
        expected_sources=4,
        maslow_level="survival",
        career_stage="entry"
    ),
    TestPersona(
        id="returning",
        name="Michelle Anderson - Returning to Work",
        query="part time administrative",
        location="Denver, CO",
        expected_sources=5,
        maslow_level="safety",
        career_stage="returning"
    ),
    TestPersona(
        id="tech_specialist",
        name="Alex Wu - DevOps Engineer",
        query="devops kubernetes",
        location="Remote",
        expected_sources=6,
        maslow_level="esteem",
        career_stage="senior"
    ),
]

def test_job_search_endpoint(query: str, location: str = None, limit: int = 5) -> Dict:
    """Test the /jobs/search endpoint with persona query"""

    url = f"{API_BASE}/jobs/search"
    params = {
        "query": query,
        "limit": limit
    }

    if location:
        params["location"] = location

    try:
        start_time = time.time()
        response = requests.get(url, params=params, timeout=30)
        response_time_ms = (time.time() - start_time) * 1000

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "jobs": data.get("jobs", []),
                "sources_used": data.get("sources_used", []),
                "response_time_ms": response_time_ms
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "response_time_ms": response_time_ms
            }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}",
            "response_time_ms": 0
        }

def test_persona(persona: TestPersona) -> PersonaTestResult:
    """Run complete job search test for one persona"""

    print(f"\n🧪 Testing Persona: {persona.name}")
    print(f"   Query: '{persona.query}' | Location: '{persona.location or 'Any'}'")
    print(f"   Maslow: {persona.maslow_level} | Stage: {persona.career_stage}")

    result = test_job_search_endpoint(persona.query, persona.location, limit=10)

    if not result["success"]:
        print(f"   ❌ API request failed: {result['error']}")
        return PersonaTestResult(
            persona_id=persona.id,
            persona_name=persona.name,
            query=persona.query,
            location=persona.location,
            total_sources_tested=0,
            sources_succeeded=0,
            sources_failed=0,
            total_jobs_found=0,
            avg_response_time_ms=result["response_time_ms"],
            source_results=[]
        )

    jobs = result["jobs"]
    sources_used = result["sources_used"]
    response_time = result["response_time_ms"]

    # Analyze results by source
    source_job_counts = {}
    for job in jobs:
        source = job.get("source", "unknown")
        source_job_counts[source] = source_job_counts.get(source, 0) + 1

    source_results = []
    for source, count in source_job_counts.items():
        source_results.append(SourceTestResult(
            source_name=source,
            query=persona.query,
            success=True,
            jobs_returned=count,
            response_time_ms=response_time
        ))

    total_jobs = len(jobs)
    sources_succeeded = len(source_job_counts)

    print(f"   ✅ Found {total_jobs} jobs from {sources_succeeded} sources ({response_time:.0f}ms)")
    for source, count in sorted(source_job_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"      • {source}: {count} jobs")

    if sources_succeeded < persona.expected_sources:
        print(f"   ⚠️  Expected {persona.expected_sources} sources, got {sources_succeeded}")

    return PersonaTestResult(
        persona_id=persona.id,
        persona_name=persona.name,
        query=persona.query,
        location=persona.location,
        total_sources_tested=12,  # All 12 sources attempted
        sources_succeeded=sources_succeeded,
        sources_failed=12 - sources_succeeded,
        total_jobs_found=total_jobs,
        avg_response_time_ms=response_time,
        source_results=source_results
    )

def run_full_stress_test() -> Dict:
    """Run stress test with all personas"""

    print("=" * 80)
    print("🚀 STRESS TEST: 12 Job Sources with Synthetic Persona Cohort")
    print("=" * 80)
    print(f"📅 Started: {datetime.now().isoformat()}")
    print(f"🎯 API Base: {API_BASE}")
    print(f"👥 Test Personas: {len(TEST_PERSONAS)}")
    print("=" * 80)

    # Health check
    print("\n🏥 Health Check...")
    try:
        health = requests.get(f"{API_BASE}/health", timeout=10)
        if health.status_code == 200:
            print("   ✅ API is healthy")
        else:
            print(f"   ⚠️  API returned {health.status_code}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return {"error": "API health check failed"}

    # Run tests for each persona
    persona_results = []
    for i, persona in enumerate(TEST_PERSONAS, 1):
        print(f"\n{'─' * 80}")
        print(f"[{i}/{len(TEST_PERSONAS)}] Persona Test")

        result = test_persona(persona)
        persona_results.append(result)

        # Brief pause between requests
        time.sleep(1)

    # Aggregate results
    print("\n" + "=" * 80)
    print("📊 AGGREGATE RESULTS")
    print("=" * 80)

    total_jobs_found = sum(r.total_jobs_found for r in persona_results)
    avg_sources_per_query = sum(r.sources_succeeded for r in persona_results) / len(persona_results)
    avg_response_time = sum(r.avg_response_time_ms for r in persona_results) / len(persona_results)

    # Source performance analysis
    source_performance = {}
    for result in persona_results:
        for source_result in result.source_results:
            if source_result.source_name not in source_performance:
                source_performance[source_result.source_name] = {
                    "queries_served": 0,
                    "total_jobs": 0,
                    "success_rate": 0.0
                }
            source_performance[source_result.source_name]["queries_served"] += 1
            source_performance[source_result.source_name]["total_jobs"] += source_result.jobs_returned

    # Calculate success rates
    for source, stats in source_performance.items():
        stats["success_rate"] = (stats["queries_served"] / len(TEST_PERSONAS)) * 100

    print(f"\n✅ Total Jobs Found: {total_jobs_found}")
    print(f"📈 Avg Sources per Query: {avg_sources_per_query:.1f}")
    print(f"⏱️  Avg Response Time: {avg_response_time:.0f}ms")

    print(f"\n📊 Source Performance:")
    print(f"{'Source':<20} {'Queries':<10} {'Jobs':<10} {'Success Rate':<15}")
    print("─" * 60)

    for source, stats in sorted(source_performance.items(), key=lambda x: x[1]["total_jobs"], reverse=True):
        print(f"{source:<20} {stats['queries_served']:<10} {stats['total_jobs']:<10} {stats['success_rate']:.1f}%")

    # Identify issues
    print(f"\n⚠️  Issues Detected:")
    issues_found = False

    for result in persona_results:
        if result.sources_succeeded == 0:
            print(f"   • {result.persona_name}: NO SOURCES RETURNED JOBS")
            issues_found = True
        elif result.total_jobs_found < 3:
            print(f"   • {result.persona_name}: Only {result.total_jobs_found} jobs found")
            issues_found = True

    if not issues_found:
        print("   None! All personas received job results.")

    # Export results
    export_data = {
        "metadata": {
            "test_timestamp": datetime.now().isoformat(),
            "api_base": API_BASE,
            "total_personas_tested": len(TEST_PERSONAS),
            "total_jobs_found": total_jobs_found
        },
        "summary": {
            "avg_sources_per_query": avg_sources_per_query,
            "avg_response_time_ms": avg_response_time,
            "source_performance": source_performance
        },
        "persona_results": [asdict(r) for r in persona_results]
    }

    filename = f"stress_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"\n💾 Results exported to: {filename}")
    print("=" * 80)

    return export_data

if __name__ == "__main__":
    results = run_full_stress_test()

    # Exit code based on results
    if "error" in results:
        sys.exit(1)

    # Check if critical threshold met
    total_jobs = results["metadata"]["total_jobs_found"]
    if total_jobs < 20:  # Expect at least 20 jobs across all queries
        print("\n❌ CRITICAL: Insufficient jobs returned")
        sys.exit(1)

    print("\n✅ Stress test completed successfully!")
    sys.exit(0)
