"""
WeWorkRemotely job source implementation.
"""
import json
import requests
from typing import List, Optional, Dict, Any
from datetime import datetime
import xml.etree.ElementTree as ET

from .base import JobSource, JobPosting

class WeWorkRemotelySource(JobSource):
    """WeWorkRemotely job board integration."""
    
    def __init__(self, api_key: str = None, rate_limit: int = 60):
        super().__init__("weworkremotely", api_key, rate_limit)
        self.rss_url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"

    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search WeWorkRemotely jobs via RSS feed."""
        try:
            headers = {'User-Agent': 'Mosaic Career Platform (contact@whatismydelta.com)'}
            response = requests.get(self.rss_url, headers=headers, timeout=10)
            response.raise_for_status()

            # Parse RSS XML
            root = ET.fromstring(response.content)
            jobs = []
            query_lower = query.lower()

            for item in root.findall('.//item')[:limit+20]:  # Get extra for filtering
                if len(jobs) >= limit:
                    break

                title = item.find('title').text if item.find('title') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''

                # Filter by query match
                if query_lower not in title.lower() and query_lower not in description.lower():
                    continue

                # Extract company from title (format: "Company: Job Title")
                company = 'Company'
                if ':' in title:
                    parts = title.split(':', 1)
                    company = parts[0].strip()
                    title = parts[1].strip() if len(parts) > 1 else title

                # Generate job ID from link
                job_id = link.split('/')[-1] if link else str(hash(title))

                job = JobPosting(
                    id=f"weworkremotely_{job_id}",
                    title=title,
                    company=company,
                    location='Remote',
                    description=description[:500],  # Limit description
                    url=link,
                    source='weworkremotely',
                    remote=True,
                    skills=[query] if query else [],
                    experience_level='mid'
                )
                jobs.append(job)

            return jobs

        except requests.RequestException as e:
            print(f"Error fetching WeWorkRemotely jobs: {e}")
            return []
        except ET.ParseError as e:
            print(f"Error parsing WeWorkRemotely RSS: {e}")
            return []
        except Exception as e:
            print(f"Error processing WeWorkRemotely jobs: {e}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed job information from WeWorkRemotely."""
        # Job details endpoint not implemented - users should click through to source URL
        return None
