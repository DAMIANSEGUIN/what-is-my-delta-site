"""
OSINT Forensics Engine for Values-Driven Job Search Intelligence
Analyzes companies through job postings to understand values alignment, 
passion opportunities, and cultural fit for Mosaic users.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
from dataclasses import dataclass

@dataclass
class JobPostingAnalysis:
    """Analysis of individual job postings for values alignment."""
    title: str
    location: str
    posting_date: str
    source: str
    compensation: Optional[str]
    snippets: List[str]
    values_indicators: List[str]
    passion_opportunities: List[str]
    culture_signals: List[str]
    growth_indicators: List[str]
    red_flags: List[str]
    confidence_score: int
    is_archive: bool

@dataclass
class CompanyOSINTReport:
    """Comprehensive OSINT analysis for values-driven job search."""
    company_name: str
    analysis_date: str
    values_alignment: Dict[str, Any]
    passion_opportunities: Dict[str, Any]
    cultural_insights: Dict[str, Any]
    growth_signals: Dict[str, Any]
    watch_outs: Dict[str, Any]
    receipts_table: List[Dict[str, Any]]
    user_values_match: Dict[str, Any]
    passion_skills_alignment: Dict[str, Any]

class OSINTForensicsEngine:
    """Engine for OSINT forensics analysis focused on values and passion alignment."""
    
    def __init__(self):
        self.analysis_cache = {}
        self.values_keywords = {
            "environmental": ["sustainability", "green", "climate", "renewable", "carbon", "environmental"],
            "social_impact": ["social impact", "community", "nonprofit", "mission-driven", "purpose"],
            "learning": ["learning", "education", "training", "development", "growth", "mentorship"],
            "innovation": ["innovation", "cutting-edge", "breakthrough", "pioneer", "disruptive"],
            "collaboration": ["collaborative", "team", "partnership", "cross-functional", "inclusive"],
            "transparency": ["transparent", "open", "honest", "authentic", "genuine"]
        }
        
        self.passion_indicators = {
            "creative": ["creative", "design", "artistic", "design", "aesthetic", "artistic"],
            "technical": ["technical", "engineering", "development", "coding", "programming"],
            "leadership": ["leadership", "management", "mentor", "guide", "inspire"],
            "analytical": ["analytical", "data", "research", "analysis", "insights"],
            "communication": ["communication", "presentation", "writing", "storytelling"],
            "problem_solving": ["problem-solving", "solutions", "challenges", "fix", "resolve"]
        }
    
    def analyze_job_posting(self, posting: Dict[str, Any]) -> JobPostingAnalysis:
        """Analyze individual job posting for values and passion alignment."""
        title = posting.get("title", "")
        location = posting.get("location", "")
        posting_date = posting.get("date", "")
        source = posting.get("source", "")
        compensation = posting.get("compensation")
        description = posting.get("description", "")
        
        # Check if posting is archive (>90 days)
        is_archive = self._is_archive_posting(posting_date)
        
        # Extract snippets (first 2 meaningful sentences)
        snippets = self._extract_snippets(description)
        
        # Analyze values indicators
        values_indicators = self._extract_values_indicators(description)
        
        # Analyze passion opportunities
        passion_opportunities = self._extract_passion_opportunities(description)
        
        # Analyze culture signals
        culture_signals = self._extract_culture_signals(description)
        
        # Analyze growth indicators
        growth_indicators = self._extract_growth_indicators(description)
        
        # Identify red flags
        red_flags = self._identify_red_flags(posting)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(posting, description)
        
        return JobPostingAnalysis(
            title=title,
            location=location,
            posting_date=posting_date,
            source=source,
            compensation=compensation,
            snippets=snippets,
            values_indicators=values_indicators,
            passion_opportunities=passion_opportunities,
            culture_signals=culture_signals,
            growth_indicators=growth_indicators,
            red_flags=red_flags,
            confidence_score=confidence_score,
            is_archive=is_archive
        )
    
    def generate_osint_report(self, company_name: str, job_postings: List[Dict[str, Any]], 
                            user_values: List[str] = None, user_passions: List[str] = None) -> CompanyOSINTReport:
        """Generate comprehensive OSINT report for values-driven job search."""
        
        # Analyze all job postings
        analyses = [self.analyze_job_posting(posting) for posting in job_postings]
        
        # Generate values alignment analysis
        values_alignment = self._analyze_values_alignment(analyses, user_values)
        
        # Generate passion opportunities analysis
        passion_opportunities = self._analyze_passion_opportunities(analyses, user_passions)
        
        # Generate cultural insights
        cultural_insights = self._analyze_cultural_insights(analyses)
        
        # Generate growth signals
        growth_signals = self._analyze_growth_signals(analyses)
        
        # Generate watch outs
        watch_outs = self._analyze_watch_outs(analyses)
        
        # Generate receipts table
        receipts_table = self._generate_receipts_table(analyses)
        
        # Generate user-specific alignment
        user_values_match = self._analyze_user_values_match(analyses, user_values)
        passion_skills_alignment = self._analyze_passion_skills_alignment(analyses, user_passions)
        
        return CompanyOSINTReport(
            company_name=company_name,
            analysis_date=datetime.utcnow().isoformat(),
            values_alignment=values_alignment,
            passion_opportunities=passion_opportunities,
            cultural_insights=cultural_insights,
            growth_signals=growth_signals,
            watch_outs=watch_outs,
            receipts_table=receipts_table,
            user_values_match=user_values_match,
            passion_skills_alignment=passion_skills_alignment
        )
    
    def _is_archive_posting(self, posting_date: str) -> bool:
        """Check if posting is older than 90 days."""
        try:
            if not posting_date:
                return True
            # Parse date and check if older than 90 days
            # This is a simplified check - in production, you'd parse the actual date
            return "ARCHIVE" in posting_date.upper() or "90+" in posting_date
        except:
            return True
    
    def _extract_snippets(self, description: str) -> List[str]:
        """Extract 1-2 meaningful snippets from job description."""
        if not description:
            return []
        
        # Split into sentences and take first 2 meaningful ones
        sentences = description.split('.')[:2]
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_values_indicators(self, description: str) -> List[str]:
        """Extract values indicators from job description."""
        indicators = []
        description_lower = description.lower()
        
        for value_type, keywords in self.values_keywords.items():
            for keyword in keywords:
                if keyword in description_lower:
                    indicators.append(f"{value_type}: {keyword}")
        
        return indicators
    
    def _extract_passion_opportunities(self, description: str) -> List[str]:
        """Extract passion opportunities from job description."""
        opportunities = []
        description_lower = description.lower()
        
        for passion_type, keywords in self.passion_indicators.items():
            for keyword in keywords:
                if keyword in description_lower:
                    opportunities.append(f"{passion_type}: {keyword}")
        
        return opportunities
    
    def _extract_culture_signals(self, description: str) -> List[str]:
        """Extract culture signals from job description."""
        signals = []
        description_lower = description.lower()
        
        culture_keywords = {
            "remote_friendly": ["remote", "flexible", "work from home"],
            "collaborative": ["collaborative", "team", "cross-functional"],
            "innovative": ["innovative", "cutting-edge", "breakthrough"],
            "inclusive": ["inclusive", "diverse", "equity"],
            "fast_paced": ["fast-paced", "dynamic", "agile"],
            "stable": ["stable", "established", "long-term"]
        }
        
        for signal_type, keywords in culture_keywords.items():
            for keyword in keywords:
                if keyword in description_lower:
                    signals.append(f"{signal_type}: {keyword}")
        
        return signals
    
    def _extract_growth_indicators(self, description: str) -> List[str]:
        """Extract growth indicators from job description."""
        indicators = []
        description_lower = description.lower()
        
        growth_keywords = {
            "new_team": ["new team", "first hire", "90-day pilot"],
            "expansion": ["expanding", "growing", "scaling"],
            "investment": ["investment", "funding", "backed"],
            "innovation": ["innovation", "R&D", "research"]
        }
        
        for indicator_type, keywords in growth_keywords.items():
            for keyword in keywords:
                if keyword in description_lower:
                    indicators.append(f"{indicator_type}: {keyword}")
        
        return indicators
    
    def _identify_red_flags(self, posting: Dict[str, Any]) -> List[str]:
        """Identify red flags in job posting."""
        red_flags = []
        
        # Check for stale postings
        if self._is_archive_posting(posting.get("date", "")):
            red_flags.append("Stale posting (>90 days)")
        
        # Check for reposted without changes
        if "reposted" in posting.get("title", "").lower():
            red_flags.append("Reposted without changes")
        
        # Check for vague descriptions
        description = posting.get("description", "")
        if len(description) < 100:
            red_flags.append("Vague job description")
        
        return red_flags
    
    def _calculate_confidence_score(self, posting: Dict[str, Any], description: str) -> int:
        """Calculate confidence score for job posting analysis."""
        score = 50  # Base score
        
        # Increase for recent postings
        if not self._is_archive_posting(posting.get("date", "")):
            score += 20
        
        # Increase for detailed descriptions
        if len(description) > 200:
            score += 15
        
        # Increase for compensation listed
        if posting.get("compensation"):
            score += 10
        
        # Increase for specific location
        if posting.get("location") and "remote" not in posting.get("location", "").lower():
            score += 5
        
        return min(score, 100)
    
    def _analyze_values_alignment(self, analyses: List[JobPostingAnalysis], user_values: List[str] = None) -> Dict[str, Any]:
        """Analyze values alignment from job postings."""
        all_values = []
        for analysis in analyses:
            all_values.extend(analysis.values_indicators)
        
        values_summary = {}
        for value in all_values:
            value_type = value.split(":")[0] if ":" in value else value
            values_summary[value_type] = values_summary.get(value_type, 0) + 1
        
        # Calculate alignment with user values
        user_alignment = {}
        if user_values:
            for user_value in user_values:
                alignment_score = 0
                for value_type, count in values_summary.items():
                    if user_value.lower() in value_type.lower():
                        alignment_score += count
                user_alignment[user_value] = alignment_score
        
        return {
            "values_detected": values_summary,
            "user_values_alignment": user_alignment,
            "top_values": sorted(values_summary.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    
    def _analyze_passion_opportunities(self, analyses: List[JobPostingAnalysis], user_passions: List[str] = None) -> Dict[str, Any]:
        """Analyze passion opportunities from job postings."""
        all_passions = []
        for analysis in analyses:
            all_passions.extend(analysis.passion_opportunities)
        
        passions_summary = {}
        for passion in all_passions:
            passion_type = passion.split(":")[0] if ":" in passion else passion
            passions_summary[passion_type] = passions_summary.get(passion_type, 0) + 1
        
        # Calculate alignment with user passions
        user_alignment = {}
        if user_passions:
            for user_passion in user_passions:
                alignment_score = 0
                for passion_type, count in passions_summary.items():
                    if user_passion.lower() in passion_type.lower():
                        alignment_score += count
                user_alignment[user_passion] = alignment_score
        
        return {
            "passions_detected": passions_summary,
            "user_passions_alignment": user_alignment,
            "top_passions": sorted(passions_summary.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    
    def _analyze_cultural_insights(self, analyses: List[JobPostingAnalysis]) -> Dict[str, Any]:
        """Analyze cultural insights from job postings."""
        all_culture = []
        for analysis in analyses:
            all_culture.extend(analysis.culture_signals)
        
        culture_summary = {}
        for signal in all_culture:
            signal_type = signal.split(":")[0] if ":" in signal else signal
            culture_summary[signal_type] = culture_summary.get(signal_type, 0) + 1
        
        return {
            "culture_signals": culture_summary,
            "dominant_culture": max(culture_summary.items(), key=lambda x: x[1]) if culture_summary else None,
            "culture_diversity": len(culture_summary)
        }
    
    def _analyze_growth_signals(self, analyses: List[JobPostingAnalysis]) -> Dict[str, Any]:
        """Analyze growth signals from job postings."""
        all_growth = []
        for analysis in analyses:
            all_growth.extend(analysis.growth_indicators)
        
        growth_summary = {}
        for signal in all_growth:
            signal_type = signal.split(":")[0] if ":" in signal else signal
            growth_summary[signal_type] = growth_summary.get(signal_type, 0) + 1
        
        return {
            "growth_signals": growth_summary,
            "growth_strength": sum(growth_summary.values()),
            "top_growth_areas": sorted(growth_summary.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    
    def _analyze_watch_outs(self, analyses: List[JobPostingAnalysis]) -> Dict[str, Any]:
        """Analyze watch outs and red flags from job postings."""
        all_red_flags = []
        for analysis in analyses:
            all_red_flags.extend(analysis.red_flags)
        
        red_flags_summary = {}
        for flag in all_red_flags:
            red_flags_summary[flag] = red_flags_summary.get(flag, 0) + 1
        
        return {
            "red_flags": red_flags_summary,
            "total_red_flags": len(all_red_flags),
            "risk_level": "high" if len(all_red_flags) > 3 else "medium" if len(all_red_flags) > 1 else "low"
        }
    
    def _generate_receipts_table(self, analyses: List[JobPostingAnalysis]) -> List[Dict[str, Any]]:
        """Generate receipts table for OSINT analysis."""
        receipts = []
        
        for analysis in analyses:
            for snippet in analysis.snippets:
                receipts.append({
                    "claim": snippet[:50] + "..." if len(snippet) > 50 else snippet,
                    "snippet": snippet,
                    "job": f"{analysis.title} - {analysis.location}",
                    "date": analysis.posting_date,
                    "source": analysis.source,
                    "confidence": analysis.confidence_score,
                    "archive": "ARCHIVE" if analysis.is_archive else "",
                    "values_indicators": ", ".join(analysis.values_indicators[:2]),
                    "passion_opportunities": ", ".join(analysis.passion_opportunities[:2])
                })
        
        return receipts
    
    def _analyze_user_values_match(self, analyses: List[JobPostingAnalysis], user_values: List[str] = None) -> Dict[str, Any]:
        """Analyze how well company matches user values."""
        if not user_values:
            return {"match_score": 0, "matched_values": [], "missing_values": []}
        
        matched_values = []
        missing_values = []
        
        for user_value in user_values:
            found = False
            for analysis in analyses:
                for indicator in analysis.values_indicators:
                    if user_value.lower() in indicator.lower():
                        matched_values.append(user_value)
                        found = True
                        break
                if found:
                    break
            
            if not found:
                missing_values.append(user_value)
        
        match_score = (len(matched_values) / len(user_values)) * 100 if user_values else 0
        
        return {
            "match_score": match_score,
            "matched_values": matched_values,
            "missing_values": missing_values,
            "alignment_strength": "strong" if match_score > 70 else "moderate" if match_score > 40 else "weak"
        }
    
    def _analyze_passion_skills_alignment(self, analyses: List[JobPostingAnalysis], user_passions: List[str] = None) -> Dict[str, Any]:
        """Analyze how well company matches user passions and skills."""
        if not user_passions:
            return {"match_score": 0, "matched_passions": [], "missing_passions": []}
        
        matched_passions = []
        missing_passions = []
        
        for user_passion in user_passions:
            found = False
            for analysis in analyses:
                for opportunity in analysis.passion_opportunities:
                    if user_passion.lower() in opportunity.lower():
                        matched_passions.append(user_passion)
                        found = True
                        break
                if found:
                    break
            
            if not found:
                missing_passions.append(user_passion)
        
        match_score = (len(matched_passions) / len(user_passions)) * 100 if user_passions else 0
        
        return {
            "match_score": match_score,
            "matched_passions": matched_passions,
            "missing_passions": missing_passions,
            "alignment_strength": "strong" if match_score > 70 else "moderate" if match_score > 40 else "weak"
        }
    
    def get_osint_health(self) -> Dict[str, Any]:
        """Get health status of OSINT forensics engine."""
        return {
            "status": "operational",
            "cache_size": len(self.analysis_cache),
            "values_keywords": len(self.values_keywords),
            "passion_indicators": len(self.passion_indicators),
            "last_updated": datetime.utcnow().isoformat()
        }

# Global instance
osint_forensics = OSINTForensicsEngine()

def analyze_company_osint(company_name: str, job_postings: List[Dict[str, Any]], 
                         user_values: List[str] = None, user_passions: List[str] = None) -> CompanyOSINTReport:
    """Analyze company using OSINT forensics for values-driven job search."""
    return osint_forensics.generate_osint_report(company_name, job_postings, user_values, user_passions)

def get_osint_health() -> Dict[str, Any]:
    """Get OSINT forensics health status."""
    return osint_forensics.get_osint_health()
