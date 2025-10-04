"""
Domain Adjacent Search Engine with RAG Semantic Clustering
Discovers related domains, skills, and opportunities through semantic analysis.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json
from dataclasses import dataclass
import random

@dataclass
class SemanticCluster:
    """Semantic cluster of related domains and skills."""
    cluster_id: str
    cluster_name: str
    core_skills: List[str]
    adjacent_skills: List[str]
    related_domains: List[str]
    opportunity_areas: List[str]
    skill_gaps: List[str]
    learning_paths: List[str]
    confidence_score: float
    cluster_strength: float

@dataclass
class DomainAdjacentSearch:
    """Domain adjacent search results with semantic clustering."""
    user_skills: List[str]
    user_domains: List[str]
    semantic_clusters: List[SemanticCluster]
    skill_alignment: Dict[str, float]
    domain_expansion: Dict[str, List[str]]
    opportunity_mapping: Dict[str, List[str]]
    learning_recommendations: List[str]
    career_paths: List[str]

class DomainAdjacentSearchEngine:
    """Engine for domain adjacent searches with RAG semantic clustering."""
    
    def __init__(self):
        self.cluster_cache = {}
        self.skill_knowledge_base = {
            "technical": {
                "core_skills": ["programming", "software development", "data analysis", "machine learning"],
                "adjacent_skills": ["cloud computing", "devops", "cybersecurity", "blockchain", "AI/ML"],
                "related_domains": ["fintech", "healthtech", "edtech", "cleantech", "biotech"],
                "opportunity_areas": ["startups", "scale-ups", "enterprise", "consulting", "research"]
            },
            "creative": {
                "core_skills": ["design", "writing", "marketing", "branding", "content creation"],
                "adjacent_skills": ["UX/UI", "video production", "photography", "social media", "copywriting"],
                "related_domains": ["media", "advertising", "publishing", "entertainment", "fashion"],
                "opportunity_areas": ["agencies", "freelance", "startups", "nonprofits", "education"]
            },
            "analytical": {
                "core_skills": ["data analysis", "research", "statistics", "modeling", "forecasting"],
                "adjacent_skills": ["business intelligence", "data science", "economics", "finance", "operations"],
                "related_domains": ["consulting", "finance", "healthcare", "government", "nonprofit"],
                "opportunity_areas": ["strategy", "research", "policy", "investment", "academia"]
            },
            "leadership": {
                "core_skills": ["management", "strategy", "team building", "communication", "decision making"],
                "adjacent_skills": ["project management", "product management", "operations", "HR", "sales"],
                "related_domains": ["business", "nonprofit", "government", "education", "healthcare"],
                "opportunity_areas": ["executive", "entrepreneurship", "consulting", "board positions", "mentoring"]
            },
            "communication": {
                "core_skills": ["writing", "presentation", "storytelling", "public speaking", "content creation"],
                "adjacent_skills": ["journalism", "marketing", "PR", "social media", "translation"],
                "related_domains": ["media", "publishing", "education", "nonprofit", "entertainment"],
                "opportunity_areas": ["content", "education", "advocacy", "freelance", "consulting"]
            },
            "problem_solving": {
                "core_skills": ["critical thinking", "analysis", "research", "innovation", "troubleshooting"],
                "adjacent_skills": ["engineering", "consulting", "research", "product development", "operations"],
                "related_domains": ["technology", "consulting", "research", "manufacturing", "services"],
                "opportunity_areas": ["innovation", "R&D", "consulting", "startups", "research"]
            }
        }
        
        self.domain_knowledge_base = {
            "technology": {
                "adjacent_domains": ["fintech", "healthtech", "edtech", "cleantech", "biotech", "agtech"],
                "skill_clusters": ["technical", "analytical", "problem_solving"],
                "growth_areas": ["AI/ML", "blockchain", "cybersecurity", "cloud", "IoT"]
            },
            "healthcare": {
                "adjacent_domains": ["biotech", "medtech", "pharma", "wellness", "fitness", "mental health"],
                "skill_clusters": ["analytical", "communication", "leadership"],
                "growth_areas": ["telemedicine", "AI diagnostics", "personalized medicine", "digital health"]
            },
            "finance": {
                "adjacent_domains": ["fintech", "cryptocurrency", "insurance", "real estate", "investment", "banking"],
                "skill_clusters": ["analytical", "technical", "leadership"],
                "growth_areas": ["blockchain", "AI trading", "regtech", "insurtech", "wealthtech"]
            },
            "education": {
                "adjacent_domains": ["edtech", "training", "consulting", "nonprofit", "government", "corporate"],
                "skill_clusters": ["communication", "leadership", "creative"],
                "growth_areas": ["online learning", "AI tutoring", "skills training", "corporate education"]
            },
            "environmental": {
                "adjacent_domains": ["cleantech", "renewable energy", "sustainability", "climate tech", "green finance"],
                "skill_clusters": ["analytical", "technical", "communication"],
                "growth_areas": ["carbon tech", "renewable energy", "sustainable finance", "climate adaptation"]
            }
        }
    
    def discover_semantic_clusters(self, user_skills: List[str], user_domains: List[str]) -> List[SemanticCluster]:
        """Discover semantic clusters based on user skills and domains."""
        clusters = []
        
        # Analyze user skills to identify skill clusters
        skill_clusters = self._identify_skill_clusters(user_skills)
        
        # Generate semantic clusters for each identified skill cluster
        for skill_cluster in skill_clusters:
            cluster = self._generate_semantic_cluster(skill_cluster, user_skills, user_domains)
            clusters.append(cluster)
        
        # Generate domain-based clusters
        domain_clusters = self._generate_domain_clusters(user_domains, user_skills)
        clusters.extend(domain_clusters)
        
        # Remove duplicates and sort by confidence
        unique_clusters = self._deduplicate_clusters(clusters)
        return sorted(unique_clusters, key=lambda x: x.confidence_score, reverse=True)
    
    def _identify_skill_clusters(self, user_skills: List[str]) -> List[str]:
        """Identify which skill clusters the user's skills belong to."""
        identified_clusters = []
        
        for skill in user_skills:
            skill_lower = skill.lower()
            for cluster_name, cluster_data in self.skill_knowledge_base.items():
                core_skills = cluster_data["core_skills"]
                adjacent_skills = cluster_data["adjacent_skills"]
                
                # Check if skill matches core or adjacent skills
                for core_skill in core_skills:
                    if core_skill.lower() in skill_lower or skill_lower in core_skill.lower():
                        if cluster_name not in identified_clusters:
                            identified_clusters.append(cluster_name)
                        break
                
                for adjacent_skill in adjacent_skills:
                    if adjacent_skill.lower() in skill_lower or skill_lower in adjacent_skill.lower():
                        if cluster_name not in identified_clusters:
                            identified_clusters.append(cluster_name)
                        break
        
        return identified_clusters
    
    def _generate_semantic_cluster(self, cluster_name: str, user_skills: List[str], user_domains: List[str]) -> SemanticCluster:
        """Generate a semantic cluster based on skill cluster."""
        cluster_data = self.skill_knowledge_base.get(cluster_name, {})
        
        # Get core skills from knowledge base
        core_skills = cluster_data.get("core_skills", [])
        adjacent_skills = cluster_data.get("adjacent_skills", [])
        related_domains = cluster_data.get("related_domains", [])
        opportunity_areas = cluster_data.get("opportunity_areas", [])
        
        # Find skills user already has
        user_core_skills = [skill for skill in user_skills if any(core in skill.lower() for core in core_skills)]
        user_adjacent_skills = [skill for skill in user_skills if any(adj in skill.lower() for adj in adjacent_skills)]
        
        # Identify skill gaps
        skill_gaps = [skill for skill in core_skills if not any(skill.lower() in user_skill.lower() for user_skill in user_skills)]
        
        # Generate learning paths
        learning_paths = self._generate_learning_paths(skill_gaps, cluster_name)
        
        # Calculate confidence score
        confidence_score = self._calculate_cluster_confidence(user_skills, core_skills, adjacent_skills)
        
        # Calculate cluster strength
        cluster_strength = len(user_core_skills) + len(user_adjacent_skills) * 0.5
        
        return SemanticCluster(
            cluster_id=f"{cluster_name}_{len(self.cluster_cache)}",
            cluster_name=cluster_name,
            core_skills=user_core_skills,
            adjacent_skills=user_adjacent_skills,
            related_domains=related_domains,
            opportunity_areas=opportunity_areas,
            skill_gaps=skill_gaps,
            learning_paths=learning_paths,
            confidence_score=confidence_score,
            cluster_strength=cluster_strength
        )
    
    def _generate_domain_clusters(self, user_domains: List[str], user_skills: List[str]) -> List[SemanticCluster]:
        """Generate clusters based on user domains."""
        clusters = []
        
        for domain in user_domains:
            domain_lower = domain.lower()
            for domain_name, domain_data in self.domain_knowledge_base.items():
                if domain_lower in domain_name.lower() or domain_name.lower() in domain_lower:
                    # Generate cluster for this domain
                    cluster = self._generate_domain_cluster(domain_name, domain_data, user_skills)
                    clusters.append(cluster)
                    break
        
        return clusters
    
    def _generate_domain_cluster(self, domain_name: str, domain_data: Dict[str, Any], user_skills: List[str]) -> SemanticCluster:
        """Generate a semantic cluster based on domain."""
        adjacent_domains = domain_data.get("adjacent_domains", [])
        skill_clusters = domain_data.get("skill_clusters", [])
        growth_areas = domain_data.get("growth_areas", [])
        
        # Find relevant skills
        relevant_skills = []
        for skill_cluster in skill_clusters:
            cluster_data = self.skill_knowledge_base.get(skill_cluster, {})
            core_skills = cluster_data.get("core_skills", [])
            adjacent_skills = cluster_data.get("adjacent_skills", [])
            relevant_skills.extend(core_skills + adjacent_skills)
        
        # Find skills user has
        user_relevant_skills = [skill for skill in user_skills if any(rel_skill.lower() in skill.lower() for rel_skill in relevant_skills)]
        
        # Identify skill gaps
        skill_gaps = [skill for skill in relevant_skills if not any(skill.lower() in user_skill.lower() for user_skill in user_skills)]
        
        # Generate learning paths
        learning_paths = self._generate_learning_paths(skill_gaps, domain_name)
        
        # Calculate confidence score
        confidence_score = self._calculate_domain_confidence(user_skills, relevant_skills)
        
        # Calculate cluster strength
        cluster_strength = len(user_relevant_skills) * 0.8
        
        return SemanticCluster(
            cluster_id=f"domain_{domain_name}_{len(self.cluster_cache)}",
            cluster_name=f"{domain_name}_domain",
            core_skills=user_relevant_skills,
            adjacent_skills=[],
            related_domains=adjacent_domains,
            opportunity_areas=growth_areas,
            skill_gaps=skill_gaps,
            learning_paths=learning_paths,
            confidence_score=confidence_score,
            cluster_strength=cluster_strength
        )
    
    def _generate_learning_paths(self, skill_gaps: List[str], cluster_name: str) -> List[str]:
        """Generate learning paths for skill gaps."""
        learning_paths = []
        
        for skill in skill_gaps[:3]:  # Top 3 skill gaps
            if "programming" in skill.lower() or "coding" in skill.lower():
                learning_paths.append(f"Learn {skill} through online courses and practice projects")
            elif "design" in skill.lower():
                learning_paths.append(f"Develop {skill} through design tools and portfolio building")
            elif "analysis" in skill.lower() or "data" in skill.lower():
                learning_paths.append(f"Master {skill} through data analysis projects and certifications")
            elif "management" in skill.lower() or "leadership" in skill.lower():
                learning_paths.append(f"Build {skill} through leadership roles and management training")
            else:
                learning_paths.append(f"Develop {skill} through targeted learning and practice")
        
        return learning_paths
    
    def _calculate_cluster_confidence(self, user_skills: List[str], core_skills: List[str], adjacent_skills: List[str]) -> float:
        """Calculate confidence score for skill cluster."""
        total_skills = len(core_skills) + len(adjacent_skills)
        matched_skills = 0
        
        for user_skill in user_skills:
            for core_skill in core_skills:
                if core_skill.lower() in user_skill.lower() or user_skill.lower() in core_skill.lower():
                    matched_skills += 1
                    break
        
        for user_skill in user_skills:
            for adjacent_skill in adjacent_skills:
                if adjacent_skill.lower() in user_skill.lower() or user_skill.lower() in adjacent_skill.lower():
                    matched_skills += 0.5
                    break
        
        return min((matched_skills / total_skills) * 100, 100) if total_skills > 0 else 0
    
    def _calculate_domain_confidence(self, user_skills: List[str], relevant_skills: List[str]) -> float:
        """Calculate confidence score for domain cluster."""
        if not relevant_skills:
            return 0
        
        matched_skills = 0
        for user_skill in user_skills:
            for rel_skill in relevant_skills:
                if rel_skill.lower() in user_skill.lower() or user_skill.lower() in rel_skill.lower():
                    matched_skills += 1
                    break
        
        return min((matched_skills / len(relevant_skills)) * 100, 100)
    
    def _deduplicate_clusters(self, clusters: List[SemanticCluster]) -> List[SemanticCluster]:
        """Remove duplicate clusters and merge similar ones."""
        unique_clusters = []
        seen_names = set()
        
        for cluster in clusters:
            if cluster.cluster_name not in seen_names:
                unique_clusters.append(cluster)
                seen_names.add(cluster.cluster_name)
        
        return unique_clusters
    
    def generate_domain_adjacent_search(self, user_skills: List[str], user_domains: List[str]) -> DomainAdjacentSearch:
        """Generate comprehensive domain adjacent search results."""
        # Discover semantic clusters
        semantic_clusters = self.discover_semantic_clusters(user_skills, user_domains)
        
        # Calculate skill alignment
        skill_alignment = self._calculate_skill_alignment(user_skills, semantic_clusters)
        
        # Generate domain expansion
        domain_expansion = self._generate_domain_expansion(user_domains, semantic_clusters)
        
        # Generate opportunity mapping
        opportunity_mapping = self._generate_opportunity_mapping(semantic_clusters)
        
        # Generate learning recommendations
        learning_recommendations = self._generate_learning_recommendations(semantic_clusters)
        
        # Generate career paths
        career_paths = self._generate_career_paths(semantic_clusters)
        
        return DomainAdjacentSearch(
            user_skills=user_skills,
            user_domains=user_domains,
            semantic_clusters=semantic_clusters,
            skill_alignment=skill_alignment,
            domain_expansion=domain_expansion,
            opportunity_mapping=opportunity_mapping,
            learning_recommendations=learning_recommendations,
            career_paths=career_paths
        )
    
    def _calculate_skill_alignment(self, user_skills: List[str], clusters: List[SemanticCluster]) -> Dict[str, float]:
        """Calculate skill alignment scores for each cluster."""
        alignment = {}
        
        for cluster in clusters:
            total_skills = len(cluster.core_skills) + len(cluster.adjacent_skills)
            user_skills_in_cluster = len([skill for skill in user_skills if skill in cluster.core_skills or skill in cluster.adjacent_skills])
            alignment[cluster.cluster_name] = (user_skills_in_cluster / total_skills) * 100 if total_skills > 0 else 0
        
        return alignment
    
    def _generate_domain_expansion(self, user_domains: List[str], clusters: List[SemanticCluster]) -> Dict[str, List[str]]:
        """Generate domain expansion opportunities."""
        expansion = {}
        
        for domain in user_domains:
            domain_lower = domain.lower()
            related_domains = []
            
            for cluster in clusters:
                if domain_lower in cluster.cluster_name.lower() or any(domain_lower in rel_domain.lower() for rel_domain in cluster.related_domains):
                    related_domains.extend(cluster.related_domains)
            
            expansion[domain] = list(set(related_domains))
        
        return expansion
    
    def _generate_opportunity_mapping(self, clusters: List[SemanticCluster]) -> Dict[str, List[str]]:
        """Generate opportunity mapping for each cluster."""
        opportunities = {}
        
        for cluster in clusters:
            opportunities[cluster.cluster_name] = cluster.opportunity_areas
        
        return opportunities
    
    def _generate_learning_recommendations(self, clusters: List[SemanticCluster]) -> List[str]:
        """Generate learning recommendations based on clusters."""
        recommendations = []
        
        for cluster in clusters:
            recommendations.extend(cluster.learning_paths)
        
        # Remove duplicates and limit to top 5
        unique_recommendations = list(set(recommendations))
        return unique_recommendations[:5]
    
    def _generate_career_paths(self, clusters: List[SemanticCluster]) -> List[str]:
        """Generate career paths based on clusters."""
        career_paths = []
        
        for cluster in clusters:
            if cluster.cluster_strength > 0.5:  # Only strong clusters
                for opportunity in cluster.opportunity_areas:
                    career_paths.append(f"{cluster.cluster_name} → {opportunity}")
        
        return career_paths[:5]
    
    def get_domain_adjacent_health(self) -> Dict[str, Any]:
        """Get health status of domain adjacent search engine."""
        return {
            "status": "operational",
            "cache_size": len(self.cluster_cache),
            "skill_knowledge_base_size": len(self.skill_knowledge_base),
            "domain_knowledge_base_size": len(self.domain_knowledge_base),
            "last_updated": datetime.utcnow().isoformat()
        }

# Global instance
domain_adjacent_search = DomainAdjacentSearchEngine()

def discover_domain_adjacent_opportunities(user_skills: List[str], user_domains: List[str]) -> DomainAdjacentSearch:
    """Discover domain adjacent opportunities through semantic clustering."""
    return domain_adjacent_search.generate_domain_adjacent_search(user_skills, user_domains)

def get_domain_adjacent_health() -> Dict[str, Any]:
    """Get domain adjacent search health status."""
    return domain_adjacent_search.get_domain_adjacent_health()
