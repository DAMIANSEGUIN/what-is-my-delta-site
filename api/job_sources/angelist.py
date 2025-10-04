"""
AngelList job source implementation for startup jobs.
"""

# import requests  # Temporarily disabled for testing
from typing import List, Optional
from datetime import datetime
from .base import JobSource, JobPosting

class AngelListSource(JobSource):
    """AngelList startup job integration."""
    
    def __init__(self, api_key: str = None):
        super().__init__("angelist", api_key, rate_limit=60)
        self.base_url = "https://api.angel.co"
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search AngelList startup jobs."""
        if not self._check_rate_limit():
            return []
        
        try:
            # AngelList API search (simplified)
            # In production, this would make actual API calls
            mock_jobs = [
                {
                    "id": f"angelist_{i}",
                    "title": f"Startup {query} Developer",
                    "company": f"Startup {i}",
                    "location": location or "San Francisco, CA",
                    "description": f"Join our startup as a {query} Developer...",
                    "url": f"https://angel.co/company/startup{i}/jobs/{i}",
                    "posted_date": datetime.now(),
                    "salary_range": f"${60000 + i*5000} - ${100000 + i*5000}",
                    "job_type": "Full-time",
                    "remote": True,
                    "skills": ["Python", "Django", "React", "PostgreSQL"],
                    "experience_level": "Mid-level"
                }
                for i in range(1, min(limit + 1))
            ]
            
            return [self._normalize_job_data(job) for job in mock_jobs]
            
        except Exception as e:
            print(f"Error searching AngelList jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from AngelList."""
        if not self._check_rate_limit():
            return None
        
        try:
            # Mock detailed job data
            job_data = {
                "id": job_id,
                "title": "Full Stack Developer",
                "company": "Tech Startup",
                "location": "Remote",
                "description": "Join our fast-growing startup...",
                "url": f"https://angel.co/company/startup/jobs/{job_id}",
                "posted_date": datetime.now(),
                "salary_range": "$70,000 - $110,000",
                "job_type": "Full-time",
                "remote": True,
                "skills": ["JavaScript", "Node.js", "React", "MongoDB"],
                "experience_level": "Mid-level"
            }
            
            return self._normalize_job_data(job_data)
            
        except Exception as e:
            print(f"Error getting AngelList job details: {e}")
            return None
