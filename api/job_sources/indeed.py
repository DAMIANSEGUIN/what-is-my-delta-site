"""
Indeed job source implementation via XML feed.
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Optional
from datetime import datetime
from .base import JobSource, JobPosting

class IndeedSource(JobSource):
    """Indeed job board integration via XML feed."""

    def __init__(self, api_key: str = None):
        super().__init__("indeed", api_key, rate_limit=100)
        self.xml_url = "https://www.indeed.com/rss"
    
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search Indeed jobs via RSS feed."""
        if not self._check_rate_limit():
            return []

        try:
            params = {'q': query}
            if location:
                params['l'] = location

            headers = {'User-Agent': 'Mosaic Career Platform (contact@whatismydelta.com)'}
            response = requests.get(self.xml_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            jobs = []

            for item in root.findall('.//item')[:limit]:
                title = item.find('title').text if item.find('title') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''

                # Extract company from title (format: "Job Title - Company Name")
                company = 'Company'
                if ' - ' in title:
                    parts = title.split(' - ', 1)
                    if len(parts) > 1:
                        company = parts[1].strip()
                        title = parts[0].strip()

                # Extract job ID from link
                job_id = link.split('jk=')[-1].split('&')[0] if 'jk=' in link else str(hash(title))

                job = {
                    "id": f"indeed_{job_id}",
                    "title": title,
                    "company": company,
                    "location": location or "See description",
                    "description": description[:500],
                    "url": link,
                    "posted_date": datetime.now(),
                    "remote": 'remote' in title.lower() or 'remote' in description.lower(),
                    "skills": [],
                    "experience_level": "mid"
                }

                jobs.append(self._normalize_job_data(job))

            return jobs

        except requests.RequestException as e:
            print(f"Error fetching Indeed jobs: {e}")
            return []
        except ET.ParseError as e:
            print(f"Error parsing Indeed RSS: {e}")
            return []
        except Exception as e:
            print(f"Error processing Indeed jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from Indeed."""
        if not self._check_rate_limit():
            return None
        
        try:
            # Mock detailed job data
            job_data = {
                "id": job_id,
                "title": "Senior Software Engineer",
                "company": "Indeed Tech",
                "location": "Austin, TX",
                "description": "We're looking for a senior software engineer to join our team...",
                "url": f"https://indeed.com/viewjob?jk={job_id}",
                "posted_date": datetime.now(),
                "salary_range": "$120,000 - $180,000",
                "job_type": "Full-time",
                "remote": False,
                "skills": ["Python", "Django", "PostgreSQL", "Docker"],
                "experience_level": "Senior"
            }
            
            return self._normalize_job_data(job_data)
            
        except Exception as e:
            print(f"Error getting Indeed job details: {e}")
            return None
