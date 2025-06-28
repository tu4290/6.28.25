"""
🎯 EXPERT ROUTER - ROUTING STRATEGIES
==================================================================

This module contains the routing strategies for the ExpertRouter.
"""

from .base import BaseRoutingStrategy
from .vector_based import VectorBasedRouting
from .performance_based import PerformanceBasedRouting
from .adaptive import AdaptiveRouting

__all__ = [
    'BaseRoutingStrategy',
    'VectorBasedRouting',
    'PerformanceBasedRouting',
    'AdaptiveRouting'
]
