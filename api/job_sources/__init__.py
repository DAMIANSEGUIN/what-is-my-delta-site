"""
Job Sources Interface for Mosaic 2.0
Provides standardized interface for different job data sources.
"""

from .base import JobSource, JobPosting
from .greenhouse import GreenhouseSource
from .serpapi import SerpApiSource
from .reddit import RedditSource

__all__ = [
    'JobSource',
    'JobPosting', 
    'GreenhouseSource',
    'SerpApiSource',
    'RedditSource'
]
