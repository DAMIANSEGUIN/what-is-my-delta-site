"""
Base classes for job sources interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class JobPosting:
    """Standardized job posting data structure."""
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str
    posted_date: Optional[datetime] = None
    salary_range: Optional[str] = None
    job_type: Optional[str] = None
    remote: bool = False
    skills: List[str] = None
    experience_level: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = []
        if self.metadata is None:
            self.metadata = {}

class JobSource(ABC):
    """Abstract base class for job data sources."""
    
    def __init__(self, name: str, api_key: str = None, rate_limit: int = 60):
        self.name = name
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.last_request = datetime.min
        self.requests_this_minute = 0
    
    @abstractmethod
    def search_jobs(self, query: str, location: str = None, limit: int = 10) -> List[JobPosting]:
        """Search for jobs matching the query."""
        pass
    
    @abstractmethod
    def get_job_details(self, job_id: str) -> Optional[JobPosting]:
        """Get detailed information for a specific job."""
        pass
    
    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits."""
        now = datetime.now()
        
        if (now - self.last_request).total_seconds() >= 60:
            self.requests_this_minute = 0
            self.last_request = now
        
        if self.requests_this_minute < self.rate_limit:
            self.requests_this_minute += 1
            return True
        return False
    
    def _normalize_job_data(self, raw_data: Dict[str, Any]) -> JobPosting:
        """Normalize raw job data to standard format."""
        return JobPosting(
            id=raw_data.get('id', ''),
            title=raw_data.get('title', ''),
            company=raw_data.get('company', ''),
            location=raw_data.get('location', ''),
            description=raw_data.get('description', ''),
            url=raw_data.get('url', ''),
            source=self.name,
            posted_date=raw_data.get('posted_date'),
            salary_range=raw_data.get('salary_range'),
            job_type=raw_data.get('job_type'),
            remote=raw_data.get('remote', False),
            skills=raw_data.get('skills', []),
            experience_level=raw_data.get('experience_level'),
            metadata=raw_data.get('metadata', {})
        )
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of the job source."""
        return {
            "name": self.name,
            "rate_limited": not self._check_rate_limit(),
            "requests_this_minute": self.requests_this_minute,
            "api_key_configured": bool(self.api_key)
        }
