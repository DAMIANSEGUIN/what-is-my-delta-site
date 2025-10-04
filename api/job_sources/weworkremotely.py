"""
WeWorkRemotely job source implementation.
"""
import json
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base import JobSource, JobPosting

class WeWorkRemotelySource(JobSource):
    """WeWorkRemotely job board integration."""
    
    def __init__(self, api_key: str = None, rate_limit: int = 60):
        super().__init__("weworkremotely", api_key, rate_limit)
        self.base_url = "https://weworkremotely.com"
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search WeWorkRemotely jobs."""
        try:
            # WeWorkRemotely API search (simplified)
            jobs = []
            for i in range(min(limit, 5)):  # Simulate API response
                job = JobPosting(
                    id=f"weworkremotely_{i}",
                    title=f"Remote {query} Position {i}",
                    company=f"WeWorkRemotely Company {i}",
                    location="Remote",
                    description=f"Join our distributed team as a {query} professional...",
                    url=f"https://weworkremotely.com/remote-jobs/{i}",
                    source="weworkremotely",
                    remote=True,
                    skills=[query, "remote", "distributed"],
                    experience_level="mid"
                )
                jobs.append(job)
            
            return jobs
            
        except Exception as e:
            print(f"Error searching WeWorkRemotely jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from WeWorkRemotely."""
        try:
            # Extract ID from job_id
            if job_id.startswith("weworkremotely_"):
                job_id = job_id.replace("weworkremotely_", "")
            
            return JobPosting(
                id=f"weworkremotely_{job_id}",
                title="Senior Remote Professional",
                company="WeWorkRemotely",
                location="Remote",
                description="Join WeWorkRemotely's distributed team...",
                url=f"https://weworkremotely.com/remote-jobs/{job_id}",
                source="weworkremotely",
                remote=True,
                skills=["remote", "distributed", "flexible"],
                experience_level="senior"
            )
            
        except Exception as e:
            print(f"Error getting WeWorkRemotely job details: {e}")
            return None
