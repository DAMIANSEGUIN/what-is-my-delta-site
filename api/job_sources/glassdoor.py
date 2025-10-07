"""
Glassdoor job source implementation via web scraping.
"""

import requests
from typing import List, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from .base import JobSource, JobPosting

class GlassdoorSource(JobSource):
    """Glassdoor job board integration via web scraping."""

    def __init__(self, api_key: str = None):
        super().__init__("glassdoor", api_key, rate_limit=100)
        self.base_url = "https://www.glassdoor.com/Job/"

    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search Glassdoor jobs via web scraping."""
        if not self._check_rate_limit():
            return []

        try:
            # Build search URL (Glassdoor format: /Job/location-query-jobs-SRCH_IL.0,8_IC1147401_KO9,15.htm)
            location_slug = location.replace(' ', '-').replace(',', '') if location else 'remote'
            query_slug = query.replace(' ', '-')

            search_url = f"{self.base_url}{location_slug}-{query_slug}-jobs-SRCH_KO0,{len(query)}.htm"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            job_cards = soup.find_all('li', class_='react-job-listing', limit=limit)

            jobs = []
            for card in job_cards:
                try:
                    title_elem = card.find('a', class_='job-title')
                    company_elem = card.find('div', class_='employer-name')
                    location_elem = card.find('div', class_='location')

                    if not (title_elem and company_elem):
                        continue

                    job_url = f"https://www.glassdoor.com{title_elem.get('href', '')}"
                    job_id = title_elem.get('data-job-id', str(hash(title_elem.text)))

                    job = {
                        "id": f"glassdoor_{job_id}",
                        "title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "location": location_elem.text.strip() if location_elem else "See description",
                        "description": f"Glassdoor job: {title_elem.text.strip()}",
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
            print(f"Error fetching Glassdoor jobs: {e}")
            return []
        except Exception as e:
            print(f"Error parsing Glassdoor jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from Glassdoor."""
        if not self._check_rate_limit():
            return None
        
        try:
            # Mock detailed job data
            job_data = {
                "id": job_id,
                "title": "Data Analyst",
                "company": "Glassdoor",
                "location": "Chicago, IL",
                "description": "Join Glassdoor's data team...",
                "url": f"https://glassdoor.com/job-listing/{job_id}",
                "posted_date": datetime.now(),
                "salary_range": "$80,000 - $120,000",
                "job_type": "Full-time",
                "remote": True,
                "skills": ["Python", "R", "SQL", "PowerBI"],
                "experience_level": "Mid-level"
            }
            
            return self._normalize_job_data(job_data)
            
        except Exception as e:
            print(f"Error getting Glassdoor job details: {e}")
            return None
