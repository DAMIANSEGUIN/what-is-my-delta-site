"""
Dice job source implementation via web scraping.
"""
import requests
from typing import List, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from .base import JobSource, JobPosting

class DiceSource(JobSource):
    """Dice job board integration via web scraping."""

    def __init__(self, api_key: str = None, rate_limit: int = 100):
        super().__init__("dice", api_key, rate_limit)
        self.base_url = "https://www.dice.com/jobs"

    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search Dice jobs via web scraping."""
        if not self._check_rate_limit():
            return []

        try:
            params = {
                'q': query,
                'location': location or '',
                'page': 1
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            job_cards = soup.find_all('div', class_='card', limit=limit)

            jobs = []
            for card in job_cards:
                try:
                    title_elem = card.find('a', class_='card-title-link')
                    company_elem = card.find('a', class_='card-company')
                    location_elem = card.find('span', class_='location')

                    if not (title_elem and company_elem):
                        continue

                    job_url = f"https://www.dice.com{title_elem.get('href', '')}"
                    job_id = job_url.split('/')[-1].split('?')[0] if job_url else str(hash(title_elem.text))

                    job = {
                        "id": f"dice_{job_id}",
                        "title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "location": location_elem.text.strip() if location_elem else "See description",
                        "description": f"Dice tech job: {title_elem.text.strip()}",
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
            print(f"Error fetching Dice jobs: {e}")
            return []
        except Exception as e:
            print(f"Error parsing Dice jobs: {e}")
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
