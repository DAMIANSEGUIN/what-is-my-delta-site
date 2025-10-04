"""
Reddit job source implementation for r/forhire and r/remotejs.
"""

# import requests  # Temporarily disabled for testing
from typing import List, Optional
from datetime import datetime
from .base import JobSource, JobPosting

class RedditSource(JobSource):
    """Reddit job posting integration."""
    
    def __init__(self, api_key: str = None):
        super().__init__("reddit", api_key, rate_limit=60)
        self.base_url = "https://www.reddit.com/r"
        self.subreddits = ["forhire", "remotejs", "jobs"]
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search Reddit job postings."""
        if not self._check_rate_limit():
            return []
        
        try:
            # Reddit API search (simplified)
            # In production, this would use Reddit API or web scraping
            mock_jobs = [
                {
                    "id": f"reddit_{i}",
                    "title": f"[HIRING] {query} Developer - Remote",
                    "company": f"Startup {i}",
                    "location": "Remote",
                    "description": f"Looking for a {query} developer to join our remote team...",
                    "url": f"https://reddit.com/r/forhire/comments/{i}",
                    "posted_date": datetime.now(),
                    "remote": True,
                    "skills": ["Python", "Django", "PostgreSQL"],
                    "experience_level": "Mid-level"
                }
                for i in range(limit)
            ]
            
            return [self._normalize_job_data(job) for job in mock_jobs]
            
        except Exception as e:
            print(f"Error searching Reddit jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from Reddit."""
        if not self._check_rate_limit():
            return None
        
        try:
            # Mock detailed job data
            job_data = {
                "id": job_id,
                "title": "[HIRING] Senior Python Developer - Remote",
                "company": "Tech Startup",
                "location": "Remote",
                "description": "We're a fast-growing startup looking for a senior Python developer...",
                "url": f"https://reddit.com/r/forhire/comments/{job_id}",
                "posted_date": datetime.now(),
                "salary_range": "$80,000 - $120,000",
                "job_type": "Contract",
                "remote": True,
                "skills": ["Python", "Django", "PostgreSQL", "Docker"],
                "experience_level": "Senior"
            }
            
            return self._normalize_job_data(job_data)
            
        except Exception as e:
            print(f"Error getting Reddit job details: {e}")
            return None
