"""
Dice job source implementation.
"""
import json
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base import JobSource, JobPosting

class DiceSource(JobSource):
    """Dice job board integration."""
    
    def __init__(self, api_key: str = None, rate_limit: int = 100):
        super().__init__("dice", api_key, rate_limit)
        self.base_url = "https://api.dice.com"
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search Dice jobs."""
        try:
            # Dice API search (simplified)
            jobs = []
            for i in range(min(limit, 5)):  # Simulate API response
                job = JobPosting(
                    id=f"dice_{i}",
                    title=f"Tech {query} Engineer {i}",
                    company=f"Dice Company {i}",
                    location=location or "San Francisco, CA",
                    description=f"Join our tech team as a {query} engineer...",
                    url=f"https://dice.com/jobs/{i}",
                    source="dice",
                    remote=False,
                    skills=[query, "tech", "engineering"],
                    experience_level="mid"
                )
                jobs.append(job)
            
            return jobs
            
        except Exception as e:
            print(f"Error searching Dice jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from Dice."""
        try:
            # Extract ID from job_id
            if job_id.startswith("dice_"):
                job_id = job_id.replace("dice_", "")
            
            return JobPosting(
                id=f"dice_{job_id}",
                title="Senior Tech Engineer",
                company="Dice",
                location="San Francisco, CA",
                description="Join Dice's engineering team...",
                url=f"https://dice.com/jobs/{job_id}",
                source="dice",
                remote=False,
                skills=["python", "tech", "engineering"],
                experience_level="senior"
            )
            
        except Exception as e:
            print(f"Error getting Dice job details: {e}")
            return None
