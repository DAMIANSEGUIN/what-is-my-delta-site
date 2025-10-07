"""
CareerBuilder job source implementation via web scraping.
"""
import requests
from typing import List, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from .base import JobSource, JobPosting

class CareerBuilderSource(JobSource):
    """CareerBuilder job board integration via web scraping."""

    def __init__(self, api_key: str = None, rate_limit: int = 100):
        super().__init__("careerbuilder", api_key, rate_limit)
        self.base_url = "https://www.careerbuilder.com/jobs"

    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search CareerBuilder jobs via web scraping."""
        if not self._check_rate_limit():
            return []

        try:
            params = {
                'keywords': query,
                'location': location or '',
                'page_number': 1
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            job_cards = soup.find_all('div', class_='data-results-content', limit=limit)

            jobs = []
            for card in job_cards:
                try:
                    title_elem = card.find('h2', class_='job-title')
                    company_elem = card.find('span', class_='company-name')
                    location_elem = card.find('span', class_='job-location')
                    link_elem = card.find('a', class_='data-results-content-link')

                    if not (title_elem and company_elem):
                        continue

                    job_url = link_elem.get('href', '') if link_elem else ''
                    if not job_url.startswith('http'):
                        job_url = f"https://www.careerbuilder.com{job_url}"

                    job_id = job_url.split('/')[-1].split('?')[0] if job_url else str(hash(title_elem.text))

                    job = {
                        "id": f"careerbuilder_{job_id}",
                        "title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "location": location_elem.text.strip() if location_elem else "See description",
                        "description": f"CareerBuilder job: {title_elem.text.strip()}",
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
            print(f"Error fetching CareerBuilder jobs: {e}")
            return []
        except Exception as e:
            print(f"Error parsing CareerBuilder jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from CareerBuilder."""
        # Job details endpoint not implemented - users should click through to source URL
        return None
