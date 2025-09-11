#!/usr/bin/env python3
"""
WIMD Scale Testing Pipeline
Automated testing of 100+ personas through complete WIMD discovery journey
Foundation compliance validation at scale
"""

import json
import requests
import time
import random
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
import pandas as pd
from pathlib import Path

@dataclass
class TestResult:
    """Single persona test result"""
    persona_id: str
    persona_name: str
    maslow_level: str
    self_efficacy_baseline: int
    
    # Test execution
    stages_completed: int
    total_interactions: int
    journey_time_minutes: int
    
    # Foundation compliance
    foundation_compliant: bool
    non_directive_maintained: bool
    user_agency_preserved: bool
    single_next_step: bool
    
    # Coaching quality
    pulse_progression: List[int]  # pulse scores throughout journey
    signals_detected: List[str]
    inflection_points: int
    coaching_responses: List[str]
    
    # Outcomes
    final_pulse_score: int
    pulse_improvement: int
    journey_completed: bool
    success_achieved: bool
    
    # Edge cases and failures
    error_encountered: bool
    error_type: str
    failure_stage: str
    
    # Performance metrics
    response_times: List[float]  # API response times
    token_usage: int

class WIMDScaleTester:
    """Automated testing pipeline for WIMD system"""
    
    def __init__(self, wimd_api_base: str = "http://localhost:8000"):
        self.api_base = wimd_api_base
        self.results: List[TestResult] = []
        self.start_time = datetime.now()
        
    def test_persona_cohort(self, persona_file: str = "persona_cohort_100.json") -> Dict:
        """Test complete cohort of personas through WIMD system"""
        
        print("🧪 STARTING WIMD SCALE TESTING PIPELINE")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Load persona cohort
        with open(persona_file, 'r') as f:
            cohort_data = json.load(f)
        
        personas = cohort_data['personas']
        total_personas = len(personas)
        
        print(f"📊 Testing {total_personas} personas...")
        print(f"🎯 API Endpoint: {self.api_base}")
        print()
        
        # Test each persona
        for i, persona_data in enumerate(personas, 1):
            print(f"🎭 Testing {i}/{total_personas}: {persona_data['name']} ({persona_data['maslow_level']})")
            
            try:
                result = self._test_single_persona(persona_data)
                self.results.append(result)
                
                # Progress indicator
                if result.foundation_compliant:
                    print(f"   ✅ Foundation compliant, {result.pulse_improvement}pt improvement")
                else:
                    print(f"   ❌ Foundation violation: {result.error_type}")
                
                # Rate limiting - don't overwhelm API
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   💥 Test failed: {str(e)}")
                # Create error result
                error_result = self._create_error_result(persona_data, str(e))
                self.results.append(error_result)
            
            # Progress update every 10 personas
            if i % 10 == 0:
                compliance_rate = sum(1 for r in self.results if r.foundation_compliant) / len(self.results)
                print(f"📈 Progress: {i}/{total_personas}, Compliance rate: {compliance_rate:.1%}")
        
        # Generate comprehensive results
        return self._analyze_results()
    
    def _test_single_persona(self, persona_data: Dict) -> TestResult:
        """Test single persona through complete WIMD journey"""
        
        start_time = time.time()
        persona_id = persona_data['persona_id']
        
        # Initialize result tracking
        pulse_scores = [persona_data['self_efficacy']]
        coaching_responses = []
        response_times = []
        signals_detected = []
        stages_completed = 0
        interactions = 0
        
        # Simulate realistic persona responses throughout journey
        journey_stages = self._generate_persona_journey(persona_data)
        
        foundation_compliant = True
        error_encountered = False
        error_type = ""
        failure_stage = ""
        
        # Execute journey stage by stage
        for stage_name, user_input in journey_stages:
            interactions += 1
            
            try:
                # API call
                api_start = time.time()
                response = self._call_wimd_api(user_input)
                api_time = time.time() - api_start
                response_times.append(api_time)
                
                # Extract coaching response and metrics
                if 'result' in response:
                    result = response['result']
                    coaching_response = result.get('coaching_response', '')
                    pulse_score = result.get('pulse_score', 0)
                    detected_signals = result.get('signals_detected', [])
                    
                    coaching_responses.append(coaching_response)
                    pulse_scores.append(pulse_score)
                    signals_detected.extend(detected_signals)
                    
                    # Foundation compliance checks
                    compliance_check = self._check_foundation_compliance(
                        coaching_response, user_input, stage_name
                    )
                    
                    if not compliance_check['compliant']:
                        foundation_compliant = False
                        error_type = compliance_check['violation']
                        failure_stage = stage_name
                        break
                    
                    stages_completed += 1
                    
                else:
                    # API error
                    error_encountered = True
                    error_type = "api_error"
                    failure_stage = stage_name
                    break
                    
            except Exception as e:
                error_encountered = True
                error_type = f"exception: {str(e)}"
                failure_stage = stage_name
                break
        
        # Calculate final metrics
        total_time = time.time() - start_time
        final_pulse = pulse_scores[-1] if pulse_scores else 0
        baseline_pulse = pulse_scores[0] if pulse_scores else 0
        pulse_improvement = final_pulse - baseline_pulse
        
        # Success criteria
        journey_completed = stages_completed >= 5  # Completed most stages
        success_achieved = (
            journey_completed and 
            pulse_improvement >= 10 and 
            foundation_compliant and 
            not error_encountered
        )
        
        return TestResult(
            persona_id=persona_id,
            persona_name=persona_data['name'],
            maslow_level=persona_data['maslow_level'],
            self_efficacy_baseline=baseline_pulse,
            
            stages_completed=stages_completed,
            total_interactions=interactions,
            journey_time_minutes=round(total_time / 60, 1),
            
            foundation_compliant=foundation_compliant,
            non_directive_maintained=foundation_compliant,  # Simplified
            user_agency_preserved=foundation_compliant,
            single_next_step=foundation_compliant,
            
            pulse_progression=pulse_scores,
            signals_detected=list(set(signals_detected)),
            inflection_points=len([s for s in signals_detected if s in ['helplessness', 'overwhelmed', 'stuck']]),
            coaching_responses=coaching_responses,
            
            final_pulse_score=final_pulse,
            pulse_improvement=pulse_improvement,
            journey_completed=journey_completed,
            success_achieved=success_achieved,
            
            error_encountered=error_encountered,
            error_type=error_type,
            failure_stage=failure_stage,
            
            response_times=response_times,
            token_usage=sum(len(r.split()) for r in coaching_responses) * 1.3  # Rough estimate
        )
    
    def _generate_persona_journey(self, persona_data: Dict) -> List[Tuple[str, str]]:
        """Generate realistic user inputs for persona throughout journey"""
        
        name = persona_data['name'].split()[0]  # First name
        maslow_level = persona_data['maslow_level']
        constraints = persona_data['primary_barriers']
        career_reason = persona_data['career_change_reason']
        self_efficacy = persona_data['self_efficacy']
        
        # Generate persona-specific journey stages
        journey_stages = []
        
        # Stage 1: Self-clarify - Varies by Maslow level and self-efficacy
        if maslow_level == "survival":
            stage1 = f"Hi, I'm {name}. I'm really struggling financially and need to find a stable job quickly. I have {', '.join(constraints)} which makes this challenging. I don't even know where to start."
        elif maslow_level == "safety":
            stage1 = f"I'm {name} and I need to make a career change because of {career_reason}. I'm worried about job security and making the wrong move. What should I focus on first?"
        elif maslow_level == "belonging":
            stage1 = f"Hi, I'm {name}. I feel disconnected in my current role and want to find work where I fit better. I'm not sure what that looks like though."
        elif maslow_level == "esteem":
            stage1 = f"I'm {name} and I'm ready for the next level in my career. I want recognition for my abilities but I'm not sure the best path forward."
        else:  # self_actualization
            stage1 = f"Hello, I'm {name}. I'm successful in my current role but I want work that's more aligned with my deeper values and purpose."
        
        journey_stages.append(("self_clarify", stage1))
        
        # Stage 2: Opportunity scan
        stage2 = f"That's helpful to think about. I've been looking into some different options. What should I be considering about the job market right now?"
        journey_stages.append(("opportunity_scan", stage2))
        
        # Stage 3: Option generation
        if "time_constraints" in constraints:
            stage3 = f"I've identified a few potential paths, but I only have limited time to pursue training or networking. What's realistic given my situation?"
        elif "financial_limitations" in constraints:
            stage3 = f"I see some interesting opportunities but many require additional training I can't afford. What are my options?"
        else:
            stage3 = f"I've narrowed down to 2-3 career directions that interest me. How do I decide which one to pursue?"
        
        journey_stages.append(("option_generation", stage3))
        
        # Stage 4: Fit & feasibility  
        stage4 = f"I'm leaning toward [specific option]. Given my constraints around {constraints[0] if constraints else 'time'}, what should I consider?"
        journey_stages.append(("fit_feasibility", stage4))
        
        # Stage 5: Plan experiments
        stage5 = f"I want to test this direction before fully committing. What kind of small experiment could I try?"
        journey_stages.append(("plan_experiments", stage5))
        
        # Stage 6: Market test (if journey progresses well)
        if self_efficacy > 60:
            stage6 = f"I've been testing the waters and getting some positive responses. How do I know if I'm on the right track?"
            journey_stages.append(("market_test", stage6))
        
        return journey_stages
    
    def _call_wimd_api(self, user_input: str) -> Dict:
        """Make API call to WIMD system"""
        
        response = requests.post(
            f"{self.api_base}/wimd",
            json={"prompt": user_input},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        response.raise_for_status()
        return response.json()
    
    def _check_foundation_compliance(self, coaching_response: str, user_input: str, stage: str) -> Dict:
        """Check if coaching response meets Foundation principles"""
        
        response_lower = coaching_response.lower()
        
        # Check for directive language (violations)
        directive_phrases = [
            "you should", "you must", "you need to", "i recommend",
            "the best approach is", "you have to", "do this",
            "follow these steps", "here's what you need to do"
        ]
        
        directive_violations = [phrase for phrase in directive_phrases if phrase in response_lower]
        
        # Check for question-asking (good)
        question_indicators = ["?", "what", "how", "which", "would you"]
        has_questions = any(indicator in response_lower for indicator in question_indicators)
        
        # Check for choice-offering (good)
        choice_indicators = ["you could", "you might", "options", "choices", "consider"]
        offers_choices = any(indicator in response_lower for indicator in choice_indicators)
        
        # Check for multiple next steps (violation)
        step_indicators = ["first,", "second,", "then", "next,", "1.", "2.", "3."]
        multiple_steps = sum(1 for indicator in step_indicators if indicator in response_lower)
        
        # Determine compliance
        compliant = True
        violation = ""
        
        if directive_violations:
            compliant = False
            violation = f"directive_language: {directive_violations[0]}"
        elif multiple_steps > 2:
            compliant = False
            violation = f"multiple_steps: {multiple_steps} steps detected"
        elif not has_questions and not offers_choices:
            compliant = False
            violation = "non_engaging: no questions or choices offered"
        elif len(coaching_response.split()) < 10:
            compliant = False
            violation = "response_too_brief"
        
        return {
            "compliant": compliant,
            "violation": violation,
            "has_questions": has_questions,
            "offers_choices": offers_choices,
            "directive_phrases": directive_violations,
            "multiple_steps": multiple_steps
        }
    
    def _create_error_result(self, persona_data: Dict, error_message: str) -> TestResult:
        """Create error result for failed test"""
        
        return TestResult(
            persona_id=persona_data['persona_id'],
            persona_name=persona_data['name'],
            maslow_level=persona_data['maslow_level'],
            self_efficacy_baseline=persona_data['self_efficacy'],
            
            stages_completed=0,
            total_interactions=0,
            journey_time_minutes=0,
            
            foundation_compliant=False,
            non_directive_maintained=False,
            user_agency_preserved=False,
            single_next_step=False,
            
            pulse_progression=[],
            signals_detected=[],
            inflection_points=0,
            coaching_responses=[],
            
            final_pulse_score=0,
            pulse_improvement=0,
            journey_completed=False,
            success_achieved=False,
            
            error_encountered=True,
            error_type=f"test_failure: {error_message}",
            failure_stage="initialization",
            
            response_times=[],
            token_usage=0
        )
    
    def _analyze_results(self) -> Dict:
        """Analyze complete test results and generate insights"""
        
        if not self.results:
            return {"error": "No results to analyze"}
        
        total_tests = len(self.results)
        
        # Foundation compliance metrics
        compliant_tests = sum(1 for r in self.results if r.foundation_compliant)
        compliance_rate = compliant_tests / total_tests
        
        # Success metrics
        successful_journeys = sum(1 for r in self.results if r.success_achieved)
        success_rate = successful_journeys / total_tests
        
        completed_journeys = sum(1 for r in self.results if r.journey_completed)
        completion_rate = completed_journeys / total_tests
        
        # Performance metrics
        avg_stages = sum(r.stages_completed for r in self.results) / total_tests
        avg_pulse_improvement = sum(r.pulse_improvement for r in self.results if r.pulse_improvement > 0) / max(1, len([r for r in self.results if r.pulse_improvement > 0]))
        
        # Error analysis
        error_tests = [r for r in self.results if r.error_encountered]
        error_rate = len(error_tests) / total_tests
        
        error_types = {}
        failure_stages = {}
        
        for result in error_tests:
            error_types[result.error_type] = error_types.get(result.error_type, 0) + 1
            failure_stages[result.failure_stage] = failure_stages.get(result.failure_stage, 0) + 1
        
        # Maslow level analysis
        maslow_performance = {}
        for level in ["survival", "safety", "belonging", "esteem", "self_actualization"]:
            level_results = [r for r in self.results if r.maslow_level == level]
            if level_results:
                maslow_performance[level] = {
                    "count": len(level_results),
                    "compliance_rate": sum(1 for r in level_results if r.foundation_compliant) / len(level_results),
                    "success_rate": sum(1 for r in level_results if r.success_achieved) / len(level_results),
                    "avg_pulse_improvement": sum(r.pulse_improvement for r in level_results) / len(level_results)
                }
        
        # Performance metrics
        all_response_times = [t for r in self.results for t in r.response_times]
        avg_response_time = sum(all_response_times) / len(all_response_times) if all_response_times else 0
        
        total_test_time = (datetime.now() - self.start_time).total_seconds() / 60  # minutes
        
        analysis = {
            "test_summary": {
                "total_personas_tested": total_tests,
                "test_duration_minutes": round(total_test_time, 1),
                "personas_per_minute": round(total_tests / max(total_test_time, 1), 2)
            },
            "foundation_compliance": {
                "compliance_rate": round(compliance_rate * 100, 1),
                "compliant_tests": compliant_tests,
                "non_compliant_tests": total_tests - compliant_tests
            },
            "journey_outcomes": {
                "success_rate": round(success_rate * 100, 1),
                "completion_rate": round(completion_rate * 100, 1),
                "avg_stages_completed": round(avg_stages, 1),
                "avg_pulse_improvement": round(avg_pulse_improvement, 1)
            },
            "error_analysis": {
                "error_rate": round(error_rate * 100, 1),
                "error_types": error_types,
                "failure_stages": failure_stages,
                "total_errors": len(error_tests)
            },
            "maslow_level_performance": maslow_performance,
            "performance_metrics": {
                "avg_api_response_time": round(avg_response_time, 2),
                "total_api_calls": sum(r.total_interactions for r in self.results),
                "estimated_token_usage": sum(r.token_usage for r in self.results)
            }
        }
        
        return analysis
    
    def export_results(self, filename: str = None) -> str:
        """Export detailed test results"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"wimd_scale_test_results_{timestamp}.json"
        
        # Analysis
        analysis = self._analyze_results()
        
        # Export data
        export_data = {
            "test_metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_personas": len(self.results),
                "test_duration_minutes": analysis["test_summary"]["test_duration_minutes"],
                "wimd_api_endpoint": self.api_base
            },
            "analysis_summary": analysis,
            "detailed_results": [asdict(result) for result in self.results]
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename

# Main execution
if __name__ == "__main__":
    print("🧪 WIMD SCALE TESTING PIPELINE")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Check if personas exist
    persona_file = "persona_cohort_100.json"
    if not Path(persona_file).exists():
        print(f"❌ Persona file not found: {persona_file}")
        print("Run persona_scale_generator.py first to generate test personas")
        exit(1)
    
    # Initialize tester
    tester = WIMDScaleTester()
    
    # Run test suite
    print("🚀 Starting automated testing...")
    results = tester.test_persona_cohort(persona_file)
    
    # Export results
    results_file = tester.export_results()
    
    # Display summary
    print("\\n" + "="*50)
    print("🎯 WIMD SCALE TESTING COMPLETE")
    print("="*50)
    print(f"📊 Foundation Compliance: {results['foundation_compliance']['compliance_rate']}%")
    print(f"🎯 Journey Success Rate: {results['journey_outcomes']['success_rate']}%") 
    print(f"⚡ Average API Response: {results['performance_metrics']['avg_api_response_time']}s")
    print(f"💾 Results exported to: {results_file}")
    
    if results['error_analysis']['total_errors'] > 0:
        print(f"\\n🚨 ISSUES DETECTED:")
        for error_type, count in results['error_analysis']['error_types'].items():
            print(f"   • {error_type}: {count} occurrences")
    
    print(f"\\n🏔️  MASLOW LEVEL PERFORMANCE:")
    for level, metrics in results['maslow_level_performance'].items():
        print(f"   • {level}: {metrics['success_rate']:.1%} success rate")
    
    print("\\n🎉 Testing pipeline complete! Analyze results for AI improvement insights.")