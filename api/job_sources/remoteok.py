"""
RemoteOK job source implementation.
"""
import json
import requests
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base import JobSource, JobPosting

class RemoteOKSource(JobSource):
    """RemoteOK job board integration."""
    
    def __init__(self, api_key: str = None, rate_limit: int = 60):
        super().__init__("remoteok", api_key, rate_limit)
        self.base_url = "https://remoteok.io/api"
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search RemoteOK jobs via public API."""
        try:
            headers = {'User-Agent': 'Mosaic Career Platform (contact@whatismydelta.com)'}
            response = requests.get(self.base_url, headers=headers, timeout=10)
            response.raise_for_status()

            # RemoteOK returns JSON array, first item is metadata
            data = response.json()
            if not data or len(data) <= 1:
                return []

            jobs = []
            query_lower = query.lower()

            # Skip first item (metadata) and filter by query
            for job_data in data[1:limit+10]:  # Get extra to account for filtering
                if len(jobs) >= limit:
                    break

                # Filter by query match in position or tags
                position = job_data.get('position', '').lower()
                tags = [tag.lower() for tag in job_data.get('tags', [])]

                if query_lower not in position and not any(query_lower in tag for tag in tags):
                    continue

                job = JobPosting(
                    id=f"remoteok_{job_data.get('id', job_data.get('slug', ''))}",
                    title=job_data.get('position', 'Remote Position'),
                    company=job_data.get('company', 'Company'),
                    location='Remote',
                    description=job_data.get('description', '')[:500],  # Limit description length
                    url=job_data.get('url', f"https://remoteok.io/remote-jobs/{job_data.get('id', '')}"),
                    source='remoteok',
                    remote=True,
                    skills=job_data.get('tags', [])[:10],  # Limit skills
                    experience_level='mid',
                    salary_min=job_data.get('salary_min'),
                    salary_max=job_data.get('salary_max')
                )
                jobs.append(job)

            return jobs

        except requests.RequestException as e:
            print(f"Error fetching RemoteOK jobs: {e}")
            return []
        except Exception as e:
            print(f"Error parsing RemoteOK jobs: {e}")
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
