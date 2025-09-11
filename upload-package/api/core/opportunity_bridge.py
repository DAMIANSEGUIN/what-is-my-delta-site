# === OpportunityBridge - Values-Aligned Career Matching ===
import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from openai import OpenAI
from .mosaic import get_openai_client

# OpportunityBridge configuration
OPPORTUNITY_CONFIG = {
    "job_sources": ["remotive", "remoteok", "greenhouse_selected"],
    "values_extraction_model": "gpt-4",
    "character_resonance_threshold": 0.75,
    "max_opportunities_per_batch": 50
}

def run_opportunity_bridge(wimd_profile: Dict, search_parameters: Optional[Dict] = None) -> Dict:
    """
    Main OpportunityBridge function - takes WIMD output and finds character-resonant opportunities
    """
    try:
        # Extract key information from WIMD profile
        values = extract_values_from_wimd(wimd_profile)
        constraints = extract_constraints_from_wimd(wimd_profile)
        validated_roles = extract_validated_roles_from_wimd(wimd_profile)
        
        # Configure search parameters
        search_config = configure_search_parameters(values, constraints, validated_roles, search_parameters)
        
        # Mock job aggregation (in production, this would call real APIs)
        job_pool = aggregate_jobs_from_sources(search_config)
        
        # Analyze character resonance for each opportunity
        resonant_opportunities = []
        for job in job_pool[:OPPORTUNITY_CONFIG["max_opportunities_per_batch"]]:
            character_score = analyze_character_resonance(job, wimd_profile)
            
            if character_score["overall_score"] >= OPPORTUNITY_CONFIG["character_resonance_threshold"] * 100:
                opportunity = create_opportunity_report(job, character_score, wimd_profile)
                resonant_opportunities.append(opportunity)
        
        # Sort by character resonance score
        resonant_opportunities.sort(key=lambda x: x["character_resonance"]["overall_score"], reverse=True)
        
        return {
            "wimd_profile_id": wimd_profile.get("user_id", "unknown"),
            "search_timestamp": datetime.now().isoformat(),
            "total_jobs_analyzed": len(job_pool),
            "resonant_opportunities": resonant_opportunities[:10],  # Top 10
            "search_parameters": search_config,
            "foundation_principles_applied": [
                "evidence_required",
                "assume_resourcefulness", 
                "preserve_user_agency"
            ]
        }
        
    except Exception as e:
        return {
            "error": f"OpportunityBridge error: {str(e)}",
            "fallback": "Manual opportunity exploration recommended"
        }

def run_wimd_to_opportunities(wimd_result: Dict, search_preferences: Optional[Dict] = None) -> Dict:
    """
    Seamless integration: Takes fresh WIMD output and immediately finds opportunities
    """
    try:
        # Transform WIMD result into OpportunityBridge profile format
        bridge_profile = {
            "user_id": "wimd_session_" + str(datetime.now().timestamp()),
            "coaching_response": wimd_result.get("coaching_response", ""),
            "signals_detected": wimd_result.get("signals_detected", []),
            "pulse_score": wimd_result.get("pulse_score", 70),
            "experiment_card": wimd_result.get("experiment_card"),
            "timestamp": wimd_result.get("timestamp"),
            "foundation_compliant": wimd_result.get("foundation_compliant", True),
            # Extract inferred preferences from coaching response
            "inferred_values": infer_values_from_coaching_response(wimd_result.get("coaching_response", "")),
            "search_preferences": search_preferences or {}
        }
        
        # Run OpportunityBridge on the WIMD output
        opportunities = run_opportunity_bridge(bridge_profile, search_preferences)
        
        return {
            "wimd_integration": "successful",
            "wimd_summary": {
                "pulse_score": wimd_result.get("pulse_score", 70),
                "signals_detected": wimd_result.get("signals_detected", []),
                "foundation_compliant": wimd_result.get("foundation_compliant", True)
            },
            "opportunity_bridge_results": opportunities,
            "integration_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": f"WIMD→OpportunityBridge integration error: {str(e)}",
            "wimd_result": wimd_result,
            "recommendation": "Complete WIMD journey first, then explore opportunities manually"
        }

def extract_values_from_wimd(wimd_profile: Dict) -> List[str]:
    """Extract core values from WIMD profile"""
    # This would typically parse rich WIMD output
    # For now, infer from coaching response and signals
    coaching_text = wimd_profile.get("coaching_response", "")
    detected_signals = wimd_profile.get("signals_detected", [])
    
    # Common values inference from coaching language
    inferred_values = []
    
    if "helping others" in coaching_text.lower() or "service" in coaching_text.lower():
        inferred_values.append("service_to_others")
    if "stability" in coaching_text.lower() or "security" in coaching_text.lower():
        inferred_values.append("financial_security")
    if "creative" in coaching_text.lower() or "innovation" in coaching_text.lower():
        inferred_values.append("creativity")
    if "growth" in coaching_text.lower() or "learning" in coaching_text.lower():
        inferred_values.append("continuous_learning")
    if "balance" in coaching_text.lower() or "flexibility" in coaching_text.lower():
        inferred_values.append("work_life_balance")
    
    # Default values if none inferred
    return inferred_values or ["stability", "growth", "meaningful_work"]

def extract_constraints_from_wimd(wimd_profile: Dict) -> Dict:
    """Extract hard constraints from WIMD profile"""
    return {
        "location_preference": "remote_preferred",
        "salary_minimum": 60000,  # Default based on signals
        "schedule_requirement": "flexible",
        "industry_blacklist": [],
        "company_size_preference": "any"
    }

def extract_validated_roles_from_wimd(wimd_profile: Dict) -> List[str]:
    """Extract validated target roles from WIMD experiments"""
    # In production, this would parse actual experiment results
    # For now, infer from coaching response
    coaching_text = wimd_profile.get("coaching_response", "").lower()
    
    validated_roles = []
    if "customer" in coaching_text and ("success" in coaching_text or "support" in coaching_text):
        validated_roles.append("Customer Success Manager")
    if "project" in coaching_text and "management" in coaching_text:
        validated_roles.append("Project Manager")
    if "software" in coaching_text or "engineering" in coaching_text:
        validated_roles.append("Software Engineer")
    if "data" in coaching_text and ("analyst" in coaching_text or "science" in coaching_text):
        validated_roles.append("Data Analyst")
    
    return validated_roles or ["Customer Success Manager", "Project Coordinator"]

def configure_search_parameters(values: List[str], constraints: Dict, validated_roles: List[str], user_preferences: Optional[Dict]) -> Dict:
    """Configure job search parameters based on WIMD insights"""
    config = {
        "target_roles": validated_roles,
        "values_keywords": values,
        "constraints": constraints,
        "search_radius": user_preferences.get("search_radius", "remote") if user_preferences else "remote",
        "experience_level": user_preferences.get("experience_level", "mid") if user_preferences else "mid",
        "company_values_required": True,
        "culture_transparency_required": True
    }
    
    if user_preferences:
        config.update(user_preferences)
    
    return config

def aggregate_jobs_from_sources(search_config: Dict) -> List[Dict]:
    """
    Mock job aggregation - in production would call Remotive, RemoteOK, etc. APIs
    """
    # Mock job data that would come from real APIs
    mock_jobs = [
        {
            "job_id": "cs_001",
            "title": "Customer Success Manager",
            "company": "GrowthTech Solutions",
            "location": "Remote",
            "salary_range": "70000-90000",
            "description": "Join our customer success team to help clients achieve their goals. We value empathy, growth mindset, and collaborative problem-solving.",
            "company_values": ["customer_first", "continuous_learning", "work_life_balance"],
            "culture_signals": {
                "transparency": "high",
                "employee_reviews": 4.2,
                "diversity_commitment": "strong"
            },
            "posted_date": "2025-09-08"
        },
        {
            "job_id": "pm_002", 
            "title": "Project Manager",
            "company": "Impact Ventures",
            "location": "Remote",
            "salary_range": "75000-95000",
            "description": "Lead meaningful projects that create positive social impact. We're looking for organized, empathetic leaders who care about making a difference.",
            "company_values": ["social_impact", "collaboration", "innovation"],
            "culture_signals": {
                "transparency": "high",
                "employee_reviews": 4.5,
                "diversity_commitment": "excellent"
            },
            "posted_date": "2025-09-09"
        },
        {
            "job_id": "swe_003",
            "title": "Software Engineer",
            "company": "TechFlow Inc",
            "location": "Remote",
            "salary_range": "80000-120000",
            "description": "Build software that helps small businesses thrive. Join our engineering team focused on creating intuitive, powerful tools.",
            "company_values": ["small_business_support", "technical_excellence", "team_collaboration"],
            "culture_signals": {
                "transparency": "medium",
                "employee_reviews": 3.9,
                "diversity_commitment": "good"
            },
            "posted_date": "2025-09-07"
        }
    ]
    
    # Filter based on search config
    filtered_jobs = []
    for job in mock_jobs:
        if any(role.lower() in job["title"].lower() for role in search_config["target_roles"]):
            filtered_jobs.append(job)
    
    return filtered_jobs

def analyze_character_resonance(job: Dict, wimd_profile: Dict) -> Dict:
    """
    Analyze character resonance between job opportunity and WIMD profile
    """
    try:
        # Values alignment analysis
        wimd_values = extract_values_from_wimd(wimd_profile)
        job_values = job.get("company_values", [])
        
        values_alignment = calculate_values_alignment(wimd_values, job_values)
        
        # Role fit assessment (based on validated roles)
        validated_roles = extract_validated_roles_from_wimd(wimd_profile)
        role_fit = calculate_role_fit(job["title"], validated_roles)
        
        # Constraint compliance
        constraints = extract_constraints_from_wimd(wimd_profile)
        constraint_compliance = check_constraint_compliance(job, constraints)
        
        # Overall character resonance score
        overall_score = int(
            (values_alignment * 0.4) + 
            (role_fit * 0.35) + 
            (constraint_compliance * 0.25)
        )
        
        return {
            "overall_score": overall_score,
            "values_alignment": values_alignment,
            "role_fit": role_fit,
            "constraint_compliance": constraint_compliance,
            "resonance_factors": {
                "values_match": values_alignment > 80,
                "role_validated": role_fit > 75,
                "constraints_met": constraint_compliance == 100
            }
        }
        
    except Exception as e:
        # Fallback scoring
        return {
            "overall_score": 70,
            "values_alignment": 70,
            "role_fit": 70,
            "constraint_compliance": 70,
            "error": str(e)
        }

def calculate_values_alignment(wimd_values: List[str], job_values: List[str]) -> int:
    """Calculate values alignment percentage"""
    if not wimd_values or not job_values:
        return 70  # Default moderate alignment
    
    # Simple overlap calculation (in production, would use semantic matching)
    overlap = len(set(wimd_values) & set(job_values))
    max_possible = max(len(wimd_values), len(job_values))
    
    if max_possible == 0:
        return 70
    
    alignment = (overlap / max_possible) * 100
    return max(50, min(100, int(alignment)))

def calculate_role_fit(job_title: str, validated_roles: List[str]) -> int:
    """Calculate role fit based on WIMD validated roles"""
    if not validated_roles:
        return 70
    
    job_title_lower = job_title.lower()
    
    for validated_role in validated_roles:
        if validated_role.lower() in job_title_lower or job_title_lower in validated_role.lower():
            return 95  # Strong match
    
    # Partial matches
    job_words = set(job_title_lower.split())
    for validated_role in validated_roles:
        validated_words = set(validated_role.lower().split())
        if job_words & validated_words:  # Any word overlap
            return 75
    
    return 60  # No clear match

def check_constraint_compliance(job: Dict, constraints: Dict) -> int:
    """Check if job meets hard constraints"""
    compliance_score = 100
    
    # Salary constraint
    salary_range = job.get("salary_range", "")
    if salary_range and constraints.get("salary_minimum"):
        try:
            salary_min = int(salary_range.split("-")[0])
            if salary_min < constraints["salary_minimum"]:
                compliance_score -= 30
        except:
            pass  # Could not parse salary
    
    # Location constraint  
    if constraints.get("location_preference") == "remote_only" and job.get("location") != "Remote":
        compliance_score -= 40
    
    return max(0, compliance_score)

def create_opportunity_report(job: Dict, character_score: Dict, wimd_profile: Dict) -> Dict:
    """Create detailed opportunity report with coaching guidance"""
    
    # Generate contextual coaching guidance
    coaching_guidance = generate_opportunity_coaching(job, character_score, wimd_profile)
    
    return {
        "opportunity_id": f"opp_{job['job_id']}_{int(datetime.now().timestamp())}",
        "job": {
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "salary_range": job.get("salary_range", "Not specified"),
            "posted_date": job.get("posted_date", "Unknown"),
            "description_preview": job["description"][:200] + "..."
        },
        "character_resonance": character_score,
        "wimd_connections": {
            "validated_through": ["wimd_coaching_session"],
            "confidence_basis": f"Resonance score: {character_score['overall_score']}/100",
            "pulse_alignment": wimd_profile.get("pulse_score", 70)
        },
        "coaching_guidance": coaching_guidance,
        "next_steps": generate_next_steps(job, wimd_profile),
        "foundation_compliant": True
    }

def generate_opportunity_coaching(job: Dict, character_score: Dict, wimd_profile: Dict) -> Dict:
    """Generate Foundation-compliant coaching guidance for opportunity"""
    
    coaching_response = wimd_profile.get("coaching_response", "")
    
    # Values-based why this fits
    why_fits = f"This opportunity aligns with your career exploration around {job['title']} roles and the values reflected in your recent coaching session."
    
    # Experiment suggestions
    next_experiments = [
        "Research the company's mission and recent projects",
        "Connect with someone in a similar role at the company",
        "Reflect on how this role connects to your core values"
    ]
    
    # Application approach (non-directive)
    application_approach = "What aspects of your experience feel most relevant to highlight for this role?"
    
    return {
        "why_this_fits": why_fits,
        "next_experiments": next_experiments,
        "application_approach": application_approach,
        "values_connection": f"Resonance score of {character_score['overall_score']}/100 suggests strong alignment with your career exploration"
    }

def generate_next_steps(job: Dict, wimd_profile: Dict) -> List[str]:
    """Generate actionable next steps for opportunity exploration"""
    return [
        f"Explore {job['company']}'s website and recent news",
        f"Research the day-to-day reality of {job['title']} roles",
        "Consider what questions you'd want answered before applying",
        "Reflect on how this opportunity connects to your values and goals"
    ]

def infer_values_from_coaching_response(coaching_response: str) -> List[str]:
    """Infer values from WIMD coaching response text"""
    values = []
    text_lower = coaching_response.lower()
    
    if "meaningful" in text_lower or "purpose" in text_lower:
        values.append("meaningful_work")
    if "stable" in text_lower or "security" in text_lower:
        values.append("stability") 
    if "creative" in text_lower or "innovative" in text_lower:
        values.append("creativity")
    if "help" in text_lower or "service" in text_lower:
        values.append("helping_others")
    if "growth" in text_lower or "learning" in text_lower:
        values.append("continuous_learning")
    
    return values or ["growth", "meaningful_work", "stability"]