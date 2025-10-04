"""
Job Sources Interface for Mosaic 2.0
Provides standardized interface for different job data sources.
"""

from .base import JobSource, JobPosting
from .greenhouse import GreenhouseSource
from .serpapi import SerpApiSource
from .reddit import RedditSource
from .indeed import IndeedSource
from .linkedin import LinkedInSource
from .glassdoor import GlassdoorSource
from .angelist import AngelListSource
from .hackernews import HackerNewsSource

__all__ = [
    'JobSource',
    'JobPosting', 
    'GreenhouseSource',
    'SerpApiSource',
    'RedditSource',
    'IndeedSource',
    'LinkedInSource',
    'GlassdoorSource',
    'AngelListSource',
    'HackerNewsSource'
]
