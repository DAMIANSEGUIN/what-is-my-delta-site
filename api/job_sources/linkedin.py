"""
LinkedIn job source implementation via web scraping.
"""

import requests
from typing import List, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from .base import JobSource, JobPosting

class LinkedInSource(JobSource):
    """LinkedIn job board integration via web scraping."""

    def __init__(self, api_key: str = None):
        super().__init__("linkedin", api_key, rate_limit=100)
        self.base_url = "https://www.linkedin.com/jobs/search/"

    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search LinkedIn jobs via web scraping."""
        if not self._check_rate_limit():
            return []

        try:
            # Build search URL
            params = {
                'keywords': query,
                'location': location or '',
                'start': 0
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            job_cards = soup.find_all('div', class_='base-card', limit=limit)

            jobs = []
            for card in job_cards:
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    location_elem = card.find('span', class_='job-search-card__location')
                    link_elem = card.find('a', class_='base-card__full-link')

                    if not (title_elem and company_elem and link_elem):
                        continue

                    job_url = link_elem.get('href', '')
                    job_id = job_url.split('/')[-1].split('?')[0] if job_url else str(hash(title_elem.text))

                    job = {
                        "id": f"linkedin_{job_id}",
                        "title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "location": location_elem.text.strip() if location_elem else "See description",
                        "description": f"LinkedIn job: {title_elem.text.strip()}",
                        "url": job_url,
                        "posted_date": datetime.now(),
                        "remote": 'remote' in (location_elem.text.lower() if location_elem else ''),
                        "skills": [],
                        "experience_level": "mid"
                    }

                    jobs.append(self._normalize_job_data(job))

                except Exception:
                    continue

            return jobs

        except requests.RequestException as e:
            print(f"Error fetching LinkedIn jobs: {e}")
            return []
        except Exception as e:
            print(f"Error parsing LinkedIn jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from LinkedIn."""
        # Job details endpoint not implemented - users should click through to source URL
        return None
