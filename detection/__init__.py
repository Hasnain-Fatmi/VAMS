"""
Detection package for fight detection system.
Provides fight detection and person tracking components.
"""

from .fight_detector import FightDetector
from .person_tracker import PersonTracker

__all__ = [
    'FightDetector',
    'PersonTracker',
]
