"""
RemoteOK job source implementation.
"""
import json
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base import JobSource, JobPosting

class RemoteOKSource(JobSource):
    """RemoteOK job board integration."""
    
    def __init__(self, api_key: str = None, rate_limit: int = 60):
        super().__init__("remoteok", api_key, rate_limit)
        self.base_url = "https://remoteok.io/api"
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search RemoteOK jobs."""
        try:
            # RemoteOK API search (simplified)
            jobs = []
            for i in range(min(limit, 5)):  # Simulate API response
                job = JobPosting(
                    id=f"remoteok_{i}",
                    title=f"Remote {query} Developer {i}",
                    company=f"RemoteOK Company {i}",
                    location="Remote",
                    description=f"Join our remote team as a {query} developer...",
                    url=f"https://remoteok.io/remote-jobs/{i}",
                    source="remoteok",
                    remote=True,
                    skills=[query, "remote", "flexible"],
                    experience_level="mid"
                )
                jobs.append(job)
            
            return jobs
            
        except Exception as e:
            print(f"Error searching RemoteOK jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from RemoteOK."""
        try:
            # Extract ID from job_id
            if job_id.startswith("remoteok_"):
                job_id = job_id.replace("remoteok_", "")
            
            return JobPosting(
                id=f"remoteok_{job_id}",
                title="Senior Remote Developer",
                company="RemoteOK",
                location="Remote",
                description="Join RemoteOK's engineering team...",
                url=f"https://remoteok.io/remote-jobs/{job_id}",
                source="remoteok",
                remote=True,
                skills=["python", "remote", "flexible"],
                experience_level="senior"
            )
            
        except Exception as e:
            print(f"Error getting RemoteOK job details: {e}")
            return None
