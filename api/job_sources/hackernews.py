"""
Hacker News job source implementation for "Who is hiring" threads.
"""

import requests
from typing import List, Optional
from datetime import datetime
from .base import JobSource, JobPosting

class HackerNewsSource(JobSource):
    """Hacker News 'Who is hiring' thread integration."""
    
    def __init__(self, api_key: str = None):
        super().__init__("hackernews", api_key, rate_limit=60)
        self.base_url = "https://hacker-news.firebaseio.com/v0"

    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search Hacker News job postings from Job Stories."""
        if not self._check_rate_limit():
            return []

        try:
            # Get job story IDs
            response = requests.get(f"{self.base_url}/jobstories.json", timeout=10)
            response.raise_for_status()
            job_ids = response.json()[:limit*2]  # Get extra for filtering

            jobs = []
            query_lower = query.lower() if query else ''

            for job_id in job_ids:
                if len(jobs) >= limit:
                    break

                # Fetch job details
                try:
                    job_response = requests.get(f"{self.base_url}/item/{job_id}.json", timeout=5)
                    job_response.raise_for_status()
                    job_data = job_response.json()

                    if not job_data or job_data.get('dead') or job_data.get('deleted'):
                        continue

                    title = job_data.get('title', '')
                    text = job_data.get('text', '')

                    # Filter by query if provided
                    if query_lower and query_lower not in title.lower() and query_lower not in text.lower():
                        continue

                    # Extract company from title (common format: "Company Name (Location) | Position")
                    company = 'Company'
                    if '(' in title:
                        company = title.split('(')[0].strip()

                    job = {
                        "id": f"hn_{job_id}",
                        "title": title,
                        "company": company,
                        "location": "See description",
                        "description": text[:500] if text else title,
                        "url": f"https://news.ycombinator.com/item?id={job_id}",
                        "posted_date": datetime.fromtimestamp(job_data.get('time', 0)),
                        "job_type": "Full-time",
                        "remote": 'remote' in title.lower() or 'remote' in text.lower(),
                        "skills": [],
                        "experience_level": "mid"
                    }

                    jobs.append(self._normalize_job_data(job))

                except requests.RequestException:
                    continue  # Skip failed individual job fetches

            return jobs

        except requests.RequestException as e:
            print(f"Error fetching Hacker News jobs: {e}")
            return []
        except Exception as e:
            print(f"Error processing Hacker News jobs: {e}")
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
