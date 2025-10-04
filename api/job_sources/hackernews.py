"""
Hacker News job source implementation for "Who is hiring" threads.
"""

# import requests  # Temporarily disabled for testing
from typing import List, Optional
from datetime import datetime
from .base import JobSource, JobPosting

class HackerNewsSource(JobSource):
    """Hacker News 'Who is hiring' thread integration."""
    
    def __init__(self, api_key: str = None):
        super().__init__("hackernews", api_key, rate_limit=60)
        self.base_url = "https://hacker-news.firebaseio.com"
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search Hacker News job postings."""
        if not self._check_rate_limit():
            return []
        
        try:
            # Hacker News API search (simplified)
            # In production, this would make actual API calls
            mock_jobs = [
                {
                    "id": f"hn_{i}",
                    "title": f"[HIRING] {query} Developer - Remote",
                    "company": f"Tech Company {i}",
                    "location": "Remote",
                    "description": f"We're hiring a {query} developer for our remote team...",
                    "url": f"https://news.ycombinator.com/item?id={i}",
                    "posted_date": datetime.now(),
                    "salary_range": f"${80000 + i*10000} - ${130000 + i*10000}",
                    "job_type": "Full-time",
                    "remote": True,
                    "skills": ["Python", "Django", "PostgreSQL", "Docker"],
                    "experience_level": "Senior"
                }
                for i in range(1, min(limit + 1))
            ]
            
            return [self._normalize_job_data(job) for job in mock_jobs]
            
        except Exception as e:
            print(f"Error searching Hacker News jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from Hacker News."""
        if not self._check_rate_limit():
            return None
        
        try:
            # Mock detailed job data
            job_data = {
                "id": job_id,
                "title": "[HIRING] Senior Software Engineer - Remote",
                "company": "Tech Company",
                "location": "Remote",
                "description": "We're a fast-growing tech company looking for a senior software engineer...",
                "url": f"https://news.ycombinator.com/item?id={job_id}",
                "posted_date": datetime.now(),
                "salary_range": "$120,000 - $180,000",
                "job_type": "Full-time",
                "remote": True,
                "skills": ["Python", "Django", "PostgreSQL", "AWS"],
                "experience_level": "Senior"
            }
            
            return self._normalize_job_data(job_data)
            
        except Exception as e:
            print(f"Error getting Hacker News job details: {e}")
            return None
