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
from .remoteok import RemoteOKSource
from .weworkremotely import WeWorkRemotelySource
from .dice import DiceSource
from .monster import MonsterSource
from .ziprecruiter import ZipRecruiterSource
from .careerbuilder import CareerBuilderSource
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
    'RemoteOKSource',
    'WeWorkRemotelySource',
    'DiceSource',
    'MonsterSource',
    'ZipRecruiterSource',
    'CareerBuilderSource',
    'HackerNewsSource'
]
