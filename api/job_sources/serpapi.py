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
        """Search jobs using SerpApi - REQUIRES PAID API KEY."""
        if not self._check_rate_limit():
            return []

        # SerpAPI requires paid API access - return empty until API key configured
        print("SerpAPI source disabled: requires paid API key")
        return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from SerpApi - REQUIRES PAID API KEY."""
        if not self._check_rate_limit():
            return None

        # SerpAPI requires paid API access - return None until API key configured
        print("SerpAPI source disabled: requires paid API key")
        return None
