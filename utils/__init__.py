"""
Utils package for fight detection system.
Provides drawing and geometry utilities.
"""

from .drawing import draw_text_with_background
from .geometry import check_overlap, point_in_box

__all__ = [
    'draw_text_with_background',
    'check_overlap',
    'point_in_box',
]
