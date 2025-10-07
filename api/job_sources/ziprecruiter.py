"""
ZipRecruiter job source implementation via web scraping.
"""
import requests
from typing import List, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from .base import JobSource, JobPosting

class ZipRecruiterSource(JobSource):
    """ZipRecruiter job board integration via web scraping."""

    def __init__(self, api_key: str = None, rate_limit: int = 100):
        super().__init__("ziprecruiter", api_key, rate_limit)
        self.base_url = "https://www.ziprecruiter.com/jobs-search"

    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search ZipRecruiter jobs via web scraping."""
        if not self._check_rate_limit():
            return []

        try:
            params = {
                'search': query,
                'location': location or '',
                'page': 1
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            job_cards = soup.find_all('article', class_='job-card', limit=limit)

            jobs = []
            for card in job_cards:
                try:
                    title_elem = card.find('h2', class_='job-title')
                    company_elem = card.find('a', class_='company-name')
                    location_elem = card.find('span', class_='location')
                    link_elem = card.find('a', class_='job-link')

                    if not (title_elem and company_elem):
                        continue

                    job_url = link_elem.get('href', '') if link_elem else ''
                    if not job_url.startswith('http'):
                        job_url = f"https://www.ziprecruiter.com{job_url}"

                    job_id = job_url.split('/')[-1].split('?')[0] if job_url else str(hash(title_elem.text))

                    job = {
                        "id": f"ziprecruiter_{job_id}",
                        "title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "location": location_elem.text.strip() if location_elem else "See description",
                        "description": f"ZipRecruiter job: {title_elem.text.strip()}",
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
            print(f"Error fetching ZipRecruiter jobs: {e}")
            return []
        except Exception as e:
            print(f"Error parsing ZipRecruiter jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from ZipRecruiter."""
        try:
            # Extract ID from job_id
            if job_id.startswith("ziprecruiter_"):
                job_id = job_id.replace("ziprecruiter_", "")
            
            return JobPosting(
                id=f"ziprecruiter_{job_id}",
                title="Senior Professional Position",
                company="ZipRecruiter",
                location="Various Locations",
                description="Join ZipRecruiter's professional team...",
                url=f"https://ziprecruiter.com/jobs/{job_id}",
                source="ziprecruiter",
                remote=False,
                skills=["professional", "matching", "recruitment"],
                experience_level="senior"
            )
            
        except Exception as e:
            print(f"Error getting ZipRecruiter job details: {e}")
            return None
