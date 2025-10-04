"""
Glassdoor job source implementation.
"""

# import requests  # Temporarily disabled for testing
from typing import List, Optional
from datetime import datetime
from .base import JobSource, JobPosting

class GlassdoorSource(JobSource):
    """Glassdoor job board integration."""
    
    def __init__(self, api_key: str = None):
        super().__init__("glassdoor", api_key, rate_limit=100)
        self.base_url = "https://api.glassdoor.com"
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search Glassdoor jobs."""
        if not self._check_rate_limit():
            return []
        
        try:
            # Glassdoor API search (simplified)
            # In production, this would make actual API calls
            mock_jobs = [
                {
                    "id": f"glassdoor_{i}",
                    "title": f"{query} Specialist",
                    "company": f"Glassdoor Company {i}",
                    "location": location or "New York, NY",
                    "description": f"Looking for a {query} Specialist to join our team...",
                    "url": f"https://glassdoor.com/job-listing/{i}",
                    "posted_date": datetime.now(),
                    "salary_range": f"${70000 + i*8000} - ${110000 + i*8000}",
                    "job_type": "Full-time",
                    "remote": True,
                    "skills": ["Python", "SQL", "Tableau", "Excel"],
                    "experience_level": "Mid-level"
                }
                for i in range(1, min(limit + 1))
            ]
            
            return [self._normalize_job_data(job) for job in mock_jobs]
            
        except Exception as e:
            print(f"Error searching Glassdoor jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from Glassdoor."""
        if not self._check_rate_limit():
            return None
        
        try:
            # Mock detailed job data
            job_data = {
                "id": job_id,
                "title": "Data Analyst",
                "company": "Glassdoor",
                "location": "Chicago, IL",
                "description": "Join Glassdoor's data team...",
                "url": f"https://glassdoor.com/job-listing/{job_id}",
                "posted_date": datetime.now(),
                "salary_range": "$80,000 - $120,000",
                "job_type": "Full-time",
                "remote": True,
                "skills": ["Python", "R", "SQL", "PowerBI"],
                "experience_level": "Mid-level"
            }
            
            return self._normalize_job_data(job_data)
            
        except Exception as e:
            print(f"Error getting Glassdoor job details: {e}")
            return None
