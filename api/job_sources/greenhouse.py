"""
Greenhouse job source implementation.
"""

import requests
from typing import List, Optional
from datetime import datetime
from .base import JobSource, JobPosting

class GreenhouseSource(JobSource):
    """Greenhouse job board integration."""
    
    def __init__(self, api_key: str = None):
        super().__init__("greenhouse", api_key, rate_limit=60)
        self.base_url = "https://boards-api.greenhouse.io/v1"
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search Greenhouse jobs across multiple company boards."""
        if not self._check_rate_limit():
            return []

        try:
            # Greenhouse requires board tokens - we'll search popular tech company boards
            # In production, maintain a list of company board tokens
            board_tokens = ['stripe', 'airbnb', 'gitlab', 'automattic', 'shopify']

            all_jobs = []
            query_lower = query.lower() if query else ''

            for board_token in board_tokens:
                if len(all_jobs) >= limit:
                    break

                try:
                    url = f"{self.base_url}/boards/{board_token}/jobs"
                    headers = {'User-Agent': 'Mosaic Career Platform (contact@whatismydelta.com)'}
                    response = requests.get(url, headers=headers, timeout=5)

                    if response.status_code != 200:
                        continue

                    jobs_data = response.json().get('jobs', [])

                    for job_data in jobs_data:
                        if len(all_jobs) >= limit:
                            break

                        title = job_data.get('title', '')
                        departments = [d.get('name', '') for d in job_data.get('departments', [])]

                        # Filter by query
                        if query_lower and query_lower not in title.lower() and not any(query_lower in d.lower() for d in departments):
                            continue

                        # Filter by location if provided
                        job_location = job_data.get('location', {}).get('name', 'Unknown')
                        if location and location.lower() not in job_location.lower():
                            continue

                        job = {
                            "id": f"greenhouse_{job_data.get('id')}",
                            "title": title,
                            "company": board_token.capitalize(),
                            "location": job_location,
                            "description": job_data.get('content', '')[:500],
                            "url": job_data.get('absolute_url', ''),
                            "posted_date": datetime.now(),
                            "remote": 'remote' in job_location.lower(),
                            "skills": departments,
                            "experience_level": "mid"
                        }

                        all_jobs.append(self._normalize_job_data(job))

                except requests.RequestException:
                    continue

            return all_jobs

        except Exception as e:
            print(f"Error searching Greenhouse jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from Greenhouse - NOT IMPLEMENTED."""
        # Job details endpoint not implemented - users should click through to source URL
        # Implementing this would require fetching individual job pages from Greenhouse boards
        return None
