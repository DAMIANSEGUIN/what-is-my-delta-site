"""
Reddit job source implementation for r/forhire and r/remotejs.
"""

import requests
from typing import List, Optional
from datetime import datetime
from .base import JobSource, JobPosting

class RedditSource(JobSource):
    """Reddit job posting integration via JSON API."""

    def __init__(self, api_key: str = None):
        super().__init__("reddit", api_key, rate_limit=60)
        self.subreddits = ["forhire", "remotejs", "jobs", "jobsearch"]

    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search Reddit job postings via JSON API."""
        if not self._check_rate_limit():
            return []

        try:
            all_jobs = []
            query_lower = query.lower() if query else ''

            for subreddit in self.subreddits:
                if len(all_jobs) >= limit:
                    break

                try:
                    url = f"https://www.reddit.com/r/{subreddit}/new.json"
                    headers = {'User-Agent': 'Mosaic Career Platform (contact@whatismydelta.com)'}
                    response = requests.get(url, headers=headers, params={'limit': 25}, timeout=10)
                    response.raise_for_status()

                    data = response.json()
                    posts = data.get('data', {}).get('children', [])

                    for post in posts:
                        if len(all_jobs) >= limit:
                            break

                        post_data = post.get('data', {})
                        title = post_data.get('title', '')
                        selftext = post_data.get('selftext', '')

                        # Filter: must be hiring post and match query
                        if '[hiring]' not in title.lower() and 'hiring' not in title.lower():
                            continue

                        if query_lower and query_lower not in title.lower() and query_lower not in selftext.lower():
                            continue

                        # Extract company (heuristic)
                        company = 'Company'
                        if ']' in title:
                            parts = title.split(']', 1)
                            if len(parts) > 1 and '-' in parts[1]:
                                company = parts[1].split('-')[0].strip()

                        job = {
                            "id": f"reddit_{post_data.get('id', '')}",
                            "title": title.replace('[HIRING]', '').replace('[Hiring]', '').strip(),
                            "company": company,
                            "location": "Remote" if 'remote' in title.lower() else "See description",
                            "description": selftext[:500] if selftext else title,
                            "url": f"https://reddit.com{post_data.get('permalink', '')}",
                            "posted_date": datetime.fromtimestamp(post_data.get('created_utc', 0)),
                            "remote": 'remote' in title.lower() or 'remote' in selftext.lower(),
                            "skills": [],
                            "experience_level": "mid"
                        }

                        all_jobs.append(self._normalize_job_data(job))

                except requests.RequestException:
                    continue

            return all_jobs

        except Exception as e:
            print(f"Error searching Reddit jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from Reddit - NOT IMPLEMENTED."""
        # Job details endpoint not implemented - users should click through to source URL
        # Implementing this would require fetching full Reddit post via API
        return None
