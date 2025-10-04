"""
SerpApi job source implementation for job board searches.
"""

# import requests  # Temporarily disabled for testing
from typing import List, Optional
from datetime import datetime
from .base import JobSource, JobPosting

class SerpApiSource(JobSource):
    """SerpApi job search integration."""
    
    def __init__(self, api_key: str = None):
        super().__init__("serpapi", api_key, rate_limit=100)
        self.base_url = "https://serpapi.com/search"
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search jobs using SerpApi."""
        if not self._check_rate_limit():
            return []
        
        try:
            # SerpApi job search (simplified)
            params = {
                "engine": "google_jobs",
                "q": query,
                "api_key": self.api_key,
                "num": limit
            }
            if location:
                params["location"] = location
            
            # For now, return mock data
            # In production, this would make actual API calls
            mock_jobs = [
                {
                    "id": f"serpapi_{i}",
                    "title": f"{query} Developer",
                    "company": f"Tech Corp {i}",
                    "location": location or "Remote",
                    "description": f"Join our team as a {query} developer...",
                    "url": f"https://example.com/jobs/{i}",
                    "posted_date": datetime.now(),
                    "remote": True,
                    "skills": ["Python", "Django", "React"],
                    "experience_level": "Mid-level"
                }
                for i in range(1, min(limit + 1))
            ]
            
            return [self._normalize_job_data(job) for job in mock_jobs]
            
        except Exception as e:
            print(f"Error searching SerpApi jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from SerpApi."""
        if not self._check_rate_limit():
            return None
        
        try:
            # Mock detailed job data
            job_data = {
                "id": job_id,
                "title": "Full Stack Developer",
                "company": "Innovation Labs",
                "location": "New York, NY",
                "description": "We're seeking a talented full stack developer...",
                "url": f"https://example.com/jobs/{job_id}",
                "posted_date": datetime.now(),
                "salary_range": "$100,000 - $150,000",
                "job_type": "Full-time",
                "remote": False,
                "skills": ["JavaScript", "Node.js", "React", "MongoDB"],
                "experience_level": "Mid-level"
            }
            
            return self._normalize_job_data(job_data)
            
        except Exception as e:
            print(f"Error getting SerpApi job details: {e}")
            return None
