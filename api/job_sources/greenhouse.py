"""
Greenhouse job source implementation.
"""

# import requests  # Temporarily disabled for testing
from typing import List, Optional
from datetime import datetime
from .base import JobSource, JobPosting

class GreenhouseSource(JobSource):
    """Greenhouse job board integration."""
    
    def __init__(self, api_key: str = None):
        super().__init__("greenhouse", api_key, rate_limit=60)
        self.base_url = "https://boards-api.greenhouse.io/v1"
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search Greenhouse jobs."""
        if not self._check_rate_limit():
            return []
        
        try:
            # Greenhouse API search (simplified)
            params = {
                "q": query,
                "limit": limit
            }
            if location:
                params["location"] = location
            
            # For now, return mock data
            # In production, this would make actual API calls
            mock_jobs = [
                {
                    "id": f"greenhouse_{i}",
                    "title": f"Software Engineer - {query}",
                    "company": f"Company {i}",
                    "location": location or "Remote",
                    "description": f"Great opportunity for {query} developers...",
                    "url": f"https://boards.greenhouse.io/company{i}/jobs/{i}",
                    "posted_date": datetime.now(),
                    "remote": True,
                    "skills": ["Python", "JavaScript", "React"],
                    "experience_level": "Mid-level"
                }
                for i in range(1, min(limit + 1))
            ]
            
            return [self._normalize_job_data(job) for job in mock_jobs]
            
        except Exception as e:
            print(f"Error searching Greenhouse jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from Greenhouse."""
        if not self._check_rate_limit():
            return None
        
        try:
            # Mock detailed job data
            job_data = {
                "id": job_id,
                "title": "Senior Software Engineer",
                "company": "Tech Company",
                "location": "San Francisco, CA",
                "description": "We're looking for a senior software engineer to join our team...",
                "url": f"https://boards.greenhouse.io/company/jobs/{job_id}",
                "posted_date": datetime.now(),
                "salary_range": "$120,000 - $180,000",
                "job_type": "Full-time",
                "remote": True,
                "skills": ["Python", "Django", "PostgreSQL", "AWS"],
                "experience_level": "Senior"
            }
            
            return self._normalize_job_data(job_data)
            
        except Exception as e:
            print(f"Error getting Greenhouse job details: {e}")
            return None
