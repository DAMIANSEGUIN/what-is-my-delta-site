#!/usr/bin/env python3
"""
Scale Persona Generation Engine
Creates 100+ realistic personas using Census data + psychological modeling
For WIMD Foundation system validation at scale
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
import requests
from faker import Faker

# Initialize Faker for realistic data generation
fake = Faker(['en_US'])

@dataclass
class ScalePersona:
    """Enhanced persona for scale testing"""
    persona_id: str
    name: str
    age: int
    location: str
    
    # Demographics (Census-based)
    income_bracket: str  # "<25k", "25-50k", "50-75k", "75-100k", "100k+"
    education_level: str  # "high_school", "some_college", "bachelor", "graduate"
    employment_status: str  # "employed", "unemployed", "underemployed", "student"
    household_type: str  # "single", "single_parent", "couple", "family"
    
    # Geographic context
    urban_rural: str  # "urban", "suburban", "rural"
    region: str  # "northeast", "south", "midwest", "west"
    cost_of_living_index: float  # 0.8-1.5 (national average = 1.0)
    
    # Career context
    current_job_title: str
    industry: str
    years_experience: int
    career_stage: str  # "entry", "mid", "senior", "transition", "returning"
    job_satisfaction: int  # 0-100
    career_change_reason: str
    
    # Maslow hierarchy placement
    maslow_level: str  # "survival", "safety", "belonging", "esteem", "self_actualization"
    primary_motivator: str
    stress_level: int  # 0-100
    
    # Psychological profile (RIASEC + SCCT)
    realistic_score: int
    investigative_score: int
    artistic_score: int
    social_score: int
    enterprising_score: int
    conventional_score: int
    self_efficacy: int
    outcome_expectations: int
    
    # Constraints and resources
    time_availability: str  # "minimal", "limited", "moderate", "flexible"
    financial_resources: str  # "constrained", "tight", "moderate", "comfortable"
    learning_style: str  # "visual", "auditory", "kinesthetic", "reading"
    technology_comfort: int  # 0-100
    
    # Support systems
    family_support: int  # 0-100
    professional_network: int  # 0-100
    mentor_availability: bool
    
    # Barriers and challenges
    primary_barriers: List[str]
    accessibility_needs: List[str]
    cultural_considerations: List[str]
    
    # Expected WIMD outcomes (for validation)
    expected_journey_length: int  # weeks
    expected_pulse_improvement: int  # points
    expected_stage_challenges: List[str]
    success_probability: float  # 0.0-1.0

class PersonaScaleGenerator:
    """Generate large cohorts of realistic personas for AI testing"""
    
    def __init__(self):
        self.census_distributions = self._load_census_data()
        self.career_patterns = self._load_career_patterns()
        self.geographic_data = self._load_geographic_data()
        
    def generate_persona_cohort(self, n: int = 100, distribution_strategy: str = "representative") -> List[ScalePersona]:
        """Generate n personas using specified distribution strategy"""
        
        personas = []
        
        if distribution_strategy == "representative":
            # Match US Census distributions
            age_distribution = self._get_census_age_distribution()
            income_distribution = self._get_census_income_distribution()
            education_distribution = self._get_census_education_distribution()
        elif distribution_strategy == "career_explorer_focused":
            # Weight toward career transition demographics
            age_distribution = self._get_career_transition_age_distribution()
            income_distribution = self._get_transition_income_distribution()
            education_distribution = self._get_education_seeking_distribution()
        else:
            # Uniform distribution for edge case testing
            age_distribution = education_distribution = income_distribution = None
            
        for i in range(n):
            persona = self._generate_single_persona(
                age_dist=age_distribution,
                income_dist=income_distribution,
                education_dist=education_distribution
            )
            personas.append(persona)
            
        return personas
    
    def _generate_single_persona(self, age_dist=None, income_dist=None, education_dist=None) -> ScalePersona:
        """Generate one realistic persona"""
        
        # Demographics
        age = self._sample_age(age_dist)
        education = self._sample_education(education_dist, age)
        income_bracket = self._sample_income(income_dist, age, education)
        location_data = self._sample_location()
        
        # Career context
        career_data = self._generate_career_context(age, education, income_bracket)
        
        # Maslow level assessment
        maslow_data = self._assess_maslow_level(age, income_bracket, career_data)
        
        # Psychological profile
        psych_profile = self._generate_psychological_profile(career_data, maslow_data)
        
        # Constraints and resources
        constraints = self._generate_constraints(age, income_bracket, career_data, location_data)
        
        # Expected outcomes (for validation)
        expected_outcomes = self._model_expected_outcomes(psych_profile, constraints, maslow_data)
        
        return ScalePersona(
            persona_id=f"scale_{uuid.uuid4().hex[:8]}",
            name=fake.name(),
            age=age,
            location=f"{location_data['city']}, {location_data['state']}",
            
            # Demographics
            income_bracket=income_bracket,
            education_level=education,
            employment_status=career_data['employment_status'],
            household_type=self._sample_household_type(age),
            
            # Geographic
            urban_rural=location_data['urban_rural'],
            region=location_data['region'],
            cost_of_living_index=location_data['col_index'],
            
            # Career
            current_job_title=career_data['job_title'],
            industry=career_data['industry'],
            years_experience=career_data['years_exp'],
            career_stage=career_data['stage'],
            job_satisfaction=career_data['satisfaction'],
            career_change_reason=career_data['change_reason'],
            
            # Maslow
            maslow_level=maslow_data['level'],
            primary_motivator=maslow_data['motivator'],
            stress_level=maslow_data['stress'],
            
            # Psychology
            realistic_score=psych_profile['R'],
            investigative_score=psych_profile['I'],
            artistic_score=psych_profile['A'],
            social_score=psych_profile['S'],
            enterprising_score=psych_profile['E'],
            conventional_score=psych_profile['C'],
            self_efficacy=psych_profile['self_efficacy'],
            outcome_expectations=psych_profile['outcome_expectations'],
            
            # Constraints
            time_availability=constraints['time'],
            financial_resources=constraints['financial'],
            learning_style=constraints['learning_style'],
            technology_comfort=constraints['tech_comfort'],
            
            # Support
            family_support=constraints['family_support'],
            professional_network=constraints['network'],
            mentor_availability=constraints['mentor'],
            
            # Barriers
            primary_barriers=constraints['barriers'],
            accessibility_needs=constraints['accessibility'],
            cultural_considerations=constraints['cultural'],
            
            # Expected outcomes
            expected_journey_length=expected_outcomes['journey_weeks'],
            expected_pulse_improvement=expected_outcomes['pulse_gain'],
            expected_stage_challenges=expected_outcomes['challenges'],
            success_probability=expected_outcomes['success_prob']
        )
    
    def _sample_age(self, distribution=None) -> int:
        """Sample age from realistic distribution"""
        if distribution:
            return random.choices(
                list(distribution.keys()),
                weights=list(distribution.values())
            )[0]
        else:
            # Career transition focused: 25-55 with peak at 28-35
            if random.random() < 0.4:
                return random.randint(25, 35)
            elif random.random() < 0.7:
                return random.randint(36, 45)
            else:
                return random.randint(46, 60)
    
    def _sample_education(self, distribution, age) -> str:
        """Sample education level based on age cohort patterns"""
        education_levels = ["high_school", "some_college", "bachelor", "graduate"]
        
        # Younger cohorts have higher education rates
        if age < 35:
            weights = [0.15, 0.25, 0.45, 0.15]  # More college educated
        elif age < 50:
            weights = [0.25, 0.30, 0.35, 0.10]  # Mixed
        else:
            weights = [0.35, 0.35, 0.25, 0.05]  # More high school only
            
        return random.choices(education_levels, weights=weights)[0]
    
    def _sample_income(self, distribution, age, education) -> str:
        """Sample income based on age and education correlations"""
        income_brackets = ["<25k", "25-50k", "50-75k", "75-100k", "100k+"]
        
        # Model realistic income progression
        base_weights = [0.20, 0.30, 0.25, 0.15, 0.10]
        
        # Adjust for education
        if education == "graduate":
            base_weights = [0.05, 0.15, 0.25, 0.30, 0.25]
        elif education == "bachelor":
            base_weights = [0.10, 0.25, 0.30, 0.25, 0.10]
        elif education == "high_school":
            base_weights = [0.30, 0.40, 0.20, 0.08, 0.02]
            
        # Adjust for age (career progression)
        if age > 45:
            # Shift toward higher income (peak earning years)
            base_weights = [max(0, w-0.05) if i < 2 else w+0.025 for i, w in enumerate(base_weights)]
        
        return random.choices(income_brackets, weights=base_weights)[0]
    
    def _sample_location(self) -> Dict:
        """Sample realistic US location with economic context"""
        regions = {
            "northeast": {"weight": 0.17, "col_index": 1.15},
            "south": {"weight": 0.38, "col_index": 0.92},
            "midwest": {"weight": 0.21, "col_index": 0.88},
            "west": {"weight": 0.24, "col_index": 1.25}
        }
        
        region = random.choices(
            list(regions.keys()),
            weights=[v["weight"] for v in regions.values()]
        )[0]
        
        # Urban/rural distribution
        urban_rural = random.choices(
            ["urban", "suburban", "rural"],
            weights=[0.35, 0.50, 0.15]
        )[0]
        
        return {
            "city": fake.city(),
            "state": fake.state_abbr(),
            "region": region,
            "urban_rural": urban_rural,
            "col_index": regions[region]["col_index"] * random.uniform(0.85, 1.15)
        }
    
    def _generate_career_context(self, age, education, income) -> Dict:
        """Generate realistic career context"""
        
        # Map education/income to likely job categories
        job_categories = {
            ("high_school", "<25k"): ["retail_worker", "food_service", "security_guard"],
            ("high_school", "25-50k"): ["administrative_assistant", "truck_driver", "factory_worker"],
            ("bachelor", "25-50k"): ["junior_analyst", "customer_service_supervisor", "sales_associate"],
            ("bachelor", "50-75k"): ["project_coordinator", "marketing_specialist", "software_developer"],
            ("graduate", "75-100k"): ["senior_analyst", "project_manager", "consultant"],
            ("graduate", "100k+"): ["director", "senior_consultant", "principal_engineer"]
        }
        
        # Select job title
        key = (education, income)
        if key in job_categories:
            job_title = random.choice(job_categories[key])
        else:
            job_title = "specialist"  # fallback
            
        # Years of experience based on age
        min_years = max(0, age - 22)  # assuming work starts at 22
        years_exp = random.randint(0, min_years)
        
        # Career stage
        if years_exp < 3:
            stage = "entry"
        elif years_exp < 8:
            stage = "mid"
        elif years_exp < 15:
            stage = "senior"
        else:
            stage = "transition" if random.random() < 0.3 else "senior"
        
        # Employment status
        if random.random() < 0.85:
            employment_status = "employed"
        elif random.random() < 0.50:
            employment_status = "unemployed"
        else:
            employment_status = "underemployed"
        
        # Job satisfaction (influences career change motivation)
        satisfaction = random.randint(20, 95)
        
        # Career change reasons
        change_reasons = [
            "seeking_growth", "better_compensation", "work_life_balance",
            "company_layoffs", "industry_decline", "location_change",
            "passion_pursuit", "family_obligations", "health_reasons"
        ]
        
        change_reason = random.choice(change_reasons)
        if satisfaction > 70:
            change_reason = random.choice(["seeking_growth", "better_compensation", "passion_pursuit"])
        
        return {
            "job_title": job_title,
            "industry": self._map_job_to_industry(job_title),
            "years_exp": years_exp,
            "stage": stage,
            "employment_status": employment_status,
            "satisfaction": satisfaction,
            "change_reason": change_reason
        }
    
    def _assess_maslow_level(self, age, income, career_data) -> Dict:
        """Assess Maslow hierarchy level based on life circumstances"""
        
        # Income-based basic needs assessment
        if income == "<25k" and career_data["employment_status"] != "employed":
            level = "survival"
            motivator = "financial_security"
            stress = random.randint(70, 95)
        elif income in ["<25k", "25-50k"] and career_data["satisfaction"] < 50:
            level = "safety"
            motivator = "job_security"
            stress = random.randint(50, 80)
        elif career_data["satisfaction"] < 60 or age < 30:
            level = "belonging"
            motivator = "social_connection"
            stress = random.randint(40, 70)
        elif career_data["stage"] in ["mid", "senior"] and income in ["50-75k", "75-100k"]:
            level = "esteem"
            motivator = "recognition"
            stress = random.randint(30, 60)
        else:
            level = "self_actualization"
            motivator = "personal_fulfillment"
            stress = random.randint(20, 50)
        
        return {
            "level": level,
            "motivator": motivator,
            "stress": stress
        }
    
    def _generate_psychological_profile(self, career_data, maslow_data) -> Dict:
        """Generate RIASEC and SCCT profiles"""
        
        # Base RIASEC scores
        riasec_base = {code: random.randint(30, 70) for code in "RIASEC"}
        
        # Adjust based on job type (simplified mapping)
        job_adjustments = {
            "software_developer": {"R": +10, "I": +20, "C": +10},
            "project_manager": {"E": +15, "S": +10, "C": +10},
            "retail_worker": {"S": +10, "E": +5, "C": +5},
            "factory_worker": {"R": +15, "C": +10},
            "marketing_specialist": {"A": +10, "E": +15, "S": +5}
        }
        
        job_title = career_data["job_title"]
        if job_title in job_adjustments:
            for code, adjustment in job_adjustments[job_title].items():
                riasec_base[code] = min(100, riasec_base[code] + adjustment)
        
        # Self-efficacy based on career satisfaction and Maslow level
        base_efficacy = 50
        if career_data["satisfaction"] > 70:
            base_efficacy += 15
        if maslow_data["level"] in ["esteem", "self_actualization"]:
            base_efficacy += 10
        if career_data["employment_status"] == "unemployed":
            base_efficacy -= 15
            
        self_efficacy = max(20, min(95, base_efficacy + random.randint(-10, 10)))
        
        # Outcome expectations correlated with self-efficacy but distinct
        outcome_expectations = max(25, min(90, self_efficacy + random.randint(-15, 15)))
        
        return {
            "R": riasec_base["R"],
            "I": riasec_base["I"],
            "A": riasec_base["A"],
            "S": riasec_base["S"],
            "E": riasec_base["E"],
            "C": riasec_base["C"],
            "self_efficacy": self_efficacy,
            "outcome_expectations": outcome_expectations
        }
    
    def _generate_constraints(self, age, income, career_data, location_data) -> Dict:
        """Generate realistic constraints and resources"""
        
        # Time availability
        if age < 35 and random.random() < 0.3:  # Young parent likelihood
            time_availability = "minimal"
        elif income == "<25k":
            time_availability = "limited"  # Working multiple jobs
        elif career_data["stage"] == "senior":
            time_availability = "moderate"
        else:
            time_availability = "flexible"
        
        # Financial resources
        financial_map = {
            "<25k": "constrained",
            "25-50k": "tight", 
            "50-75k": "moderate",
            "75-100k": "comfortable",
            "100k+": "comfortable"
        }
        financial_resources = financial_map[income]
        
        # Learning style
        learning_styles = ["visual", "auditory", "kinesthetic", "reading"]
        learning_style = random.choice(learning_styles)
        
        # Technology comfort (age-correlated)
        if age < 35:
            tech_comfort = random.randint(70, 95)
        elif age < 50:
            tech_comfort = random.randint(50, 80)
        else:
            tech_comfort = random.randint(30, 70)
        
        # Support systems
        family_support = random.randint(30, 90)
        if location_data["urban_rural"] == "rural":
            professional_network = random.randint(20, 60)
        else:
            professional_network = random.randint(40, 80)
            
        mentor_availability = random.random() < 0.25  # 25% have mentors
        
        # Barriers
        barrier_pool = [
            "time_constraints", "financial_limitations", "lack_of_experience",
            "geographic_limitations", "family_obligations", "health_issues",
            "age_discrimination", "educational_requirements", "visa_status",
            "transportation", "childcare", "technology_access"
        ]
        
        num_barriers = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2])[0]
        barriers = random.sample(barrier_pool, num_barriers)
        
        # Accessibility needs (10% of population)
        accessibility = []
        if random.random() < 0.10:
            accessibility = random.choice([
                ["mobility_assistance"], ["vision_support"], ["hearing_support"],
                ["learning_disability_accommodation"], ["mental_health_support"]
            ])
        
        # Cultural considerations
        cultural = []
        if random.random() < 0.25:  # 25% have cultural considerations
            cultural = random.choice([
                ["first_generation_american"], ["non_native_english_speaker"],
                ["cultural_dress_requirements"], ["religious_accommodations"],
                ["veteran_status"], ["single_parent_household"]
            ])
        
        return {
            "time": time_availability,
            "financial": financial_resources,
            "learning_style": learning_style,
            "tech_comfort": tech_comfort,
            "family_support": family_support,
            "network": professional_network,
            "mentor": mentor_availability,
            "barriers": barriers,
            "accessibility": accessibility,
            "cultural": cultural
        }
    
    def _model_expected_outcomes(self, psych_profile, constraints, maslow_data) -> Dict:
        """Model expected WIMD journey outcomes for validation"""
        
        # Base journey length: 12 weeks
        base_weeks = 12
        
        # Adjust based on constraints
        if constraints["time"] == "minimal":
            base_weeks += 8
        elif constraints["time"] == "limited":
            base_weeks += 4
        
        if constraints["financial"] == "constrained":
            base_weeks += 6
        
        if len(constraints["barriers"]) > 2:
            base_weeks += 4
        
        # Self-efficacy affects journey speed
        if psych_profile["self_efficacy"] > 80:
            base_weeks -= 3
        elif psych_profile["self_efficacy"] < 50:
            base_weeks += 5
        
        journey_weeks = max(4, min(52, base_weeks))
        
        # Expected pulse improvement
        base_improvement = 20
        
        if maslow_data["level"] in ["survival", "safety"]:
            base_improvement += 15  # More room for improvement
        elif maslow_data["level"] == "self_actualization":
            base_improvement += 5   # Already high functioning
        
        if psych_profile["self_efficacy"] < 50:
            base_improvement += 10  # More potential gain
        
        pulse_improvement = max(5, min(50, base_improvement + random.randint(-5, 10)))
        
        # Challenge stages (based on Maslow level and constraints)
        challenge_map = {
            "survival": ["self_clarify", "fit_feasibility"],
            "safety": ["opportunity_scan", "fit_feasibility"],
            "belonging": ["self_clarify", "option_generation"],
            "esteem": ["option_generation", "plan_experiments"],
            "self_actualization": ["opportunity_scan", "stabilize_grow"]
        }
        
        expected_challenges = challenge_map.get(maslow_data["level"], ["self_clarify"])
        
        # Success probability
        base_success = 0.65
        
        # Adjust for self-efficacy
        if psych_profile["self_efficacy"] > 70:
            base_success += 0.15
        elif psych_profile["self_efficacy"] < 50:
            base_success -= 0.20
        
        # Adjust for constraints
        if len(constraints["barriers"]) > 2:
            base_success -= 0.15
        if constraints["family_support"] > 70:
            base_success += 0.10
        if constraints["mentor"]:
            base_success += 0.10
        
        success_prob = max(0.2, min(0.95, base_success))
        
        return {
            "journey_weeks": journey_weeks,
            "pulse_gain": pulse_improvement,
            "challenges": expected_challenges,
            "success_prob": success_prob
        }
    
    def _map_job_to_industry(self, job_title: str) -> str:
        """Map job titles to industries"""
        industry_mapping = {
            "retail_worker": "retail",
            "food_service": "hospitality",
            "software_developer": "technology",
            "project_manager": "consulting",
            "factory_worker": "manufacturing",
            "truck_driver": "logistics",
            "administrative_assistant": "business_services"
        }
        return industry_mapping.get(job_title, "other")
    
    def _sample_household_type(self, age: int) -> str:
        """Sample household type based on age patterns"""
        if age < 30:
            return random.choices(
                ["single", "couple", "single_parent", "family"],
                weights=[0.50, 0.30, 0.10, 0.10]
            )[0]
        elif age < 45:
            return random.choices(
                ["single", "couple", "single_parent", "family"],
                weights=[0.25, 0.35, 0.15, 0.25]
            )[0]
        else:
            return random.choices(
                ["single", "couple", "single_parent", "family"],
                weights=[0.30, 0.45, 0.10, 0.15]
            )[0]
    
    # Placeholder methods for data loading (would integrate real APIs)
    def _load_census_data(self) -> Dict:
        return {"age_distribution": {}, "income_brackets": {}}
    
    def _load_career_patterns(self) -> Dict:
        return {"transition_matrices": {}}
    
    def _load_geographic_data(self) -> Dict:
        return {"cost_of_living": {}}
    
    def _get_census_age_distribution(self) -> Dict:
        # Simplified - real implementation would use Census API
        return {age: 1 for age in range(25, 65)}
    
    def _get_census_income_distribution(self) -> Dict:
        return {"<25k": 0.2, "25-50k": 0.3, "50-75k": 0.25, "75-100k": 0.15, "100k+": 0.1}
    
    def _get_census_education_distribution(self) -> Dict:
        return {"high_school": 0.3, "some_college": 0.3, "bachelor": 0.3, "graduate": 0.1}
    
    def _get_career_transition_age_distribution(self) -> Dict:
        # Weight toward career change ages
        return {age: 2 if 28 <= age <= 35 else 1 for age in range(25, 65)}
    
    def _get_transition_income_distribution(self) -> Dict:
        # Weight toward middle income (most likely to seek change)
        return {"<25k": 0.15, "25-50k": 0.35, "50-75k": 0.35, "75-100k": 0.10, "100k+": 0.05}
    
    def _get_education_seeking_distribution(self) -> Dict:
        # Weight toward some college/bachelor (most likely to upskill)
        return {"high_school": 0.2, "some_college": 0.4, "bachelor": 0.35, "graduate": 0.05}

def export_persona_cohort(personas: List[ScalePersona], filename: str = "persona_cohort_100.json"):
    """Export generated personas to JSON for testing"""
    
    export_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_personas": len(personas),
            "generator_version": "1.0",
            "distribution_strategy": "career_explorer_focused"
        },
        "cohort_summary": analyze_cohort_distribution(personas),
        "personas": [asdict(persona) for persona in personas]
    }
    
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    return filename

def analyze_cohort_distribution(personas: List[ScalePersona]) -> Dict:
    """Analyze demographic distribution of generated cohort"""
    
    distributions = {
        "age": {},
        "education": {},
        "income": {},
        "maslow_level": {},
        "region": {},
        "career_stage": {}
    }
    
    for persona in personas:
        # Age buckets
        age_bucket = f"{persona.age//10*10}-{persona.age//10*10+9}"
        distributions["age"][age_bucket] = distributions["age"].get(age_bucket, 0) + 1
        
        # Education
        distributions["education"][persona.education_level] = distributions["education"].get(persona.education_level, 0) + 1
        
        # Income
        distributions["income"][persona.income_bracket] = distributions["income"].get(persona.income_bracket, 0) + 1
        
        # Maslow
        distributions["maslow_level"][persona.maslow_level] = distributions["maslow_level"].get(persona.maslow_level, 0) + 1
        
        # Region
        distributions["region"][persona.region] = distributions["region"].get(persona.region, 0) + 1
        
        # Career stage
        distributions["career_stage"][persona.career_stage] = distributions["career_stage"].get(persona.career_stage, 0) + 1
    
    # Convert counts to percentages
    total = len(personas)
    for category in distributions:
        for key in distributions[category]:
            distributions[category][key] = round(distributions[category][key] / total * 100, 1)
    
    return distributions

# Main execution
if __name__ == "__main__":
    print("🔬 GENERATING 100-PERSONA COHORT FOR WIMD TESTING")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    generator = PersonaScaleGenerator()
    
    print("📊 Generating personas with career-explorer-focused distribution...")
    personas = generator.generate_persona_cohort(n=100, distribution_strategy="career_explorer_focused")
    
    print(f"✅ Generated {len(personas)} personas")
    
    # Export for testing
    filename = export_persona_cohort(personas)
    print(f"💾 Exported to: {filename}")
    
    # Show sample personas
    print("\n🎭 SAMPLE PERSONAS:")
    print("━━━━━━━━━━━━━━━━━━━━━")
    for i, persona in enumerate(personas[:3]):
        print(f"\n{i+1}. {persona.name} ({persona.age}, {persona.location})")
        print(f"   📚 {persona.education_level}, 💰 {persona.income_bracket}")
        print(f"   💼 {persona.current_job_title} ({persona.career_stage})")
        print(f"   🏔️  Maslow: {persona.maslow_level}, 💓 Self-efficacy: {persona.self_efficacy}")
        print(f"   🚧 Barriers: {persona.primary_barriers}")
        print(f"   🎯 Expected journey: {persona.expected_journey_length} weeks, {persona.expected_pulse_improvement}pt gain")
    
    print(f"\n📈 COHORT DISTRIBUTION ANALYSIS:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    distribution = analyze_cohort_distribution(personas)
    for category, data in distribution.items():
        print(f"{category.upper()}: {data}")
    
    print("\n🎯 Ready for WIMD testing pipeline!")