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
        """Search AngelList startup jobs - REQUIRES PAID API KEY."""
        if not self._check_rate_limit():
            return []

        # AngelList requires paid API access - return empty until API key configured
        print("AngelList source disabled: requires paid API key")
        return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from AngelList - REQUIRES PAID API KEY."""
        if not self._check_rate_limit():
            return None

        # AngelList requires paid API access - return None until API key configured
        print("AngelList source disabled: requires paid API key")
        return None
