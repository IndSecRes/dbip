"""
Signal Fusion Package
Correlates weak signals into strong intelligence
"""

from .engine import SignalFusionEngine, FusedSignal
from .patterns import (
    PatternDetector,
    EntityPattern,
    TemporalPattern,
    GeographicPattern,
    KeywordCluster
)

__all__ = [
    "SignalFusionEngine",
    "FusedSignal",
    "PatternDetector",
    "EntityPattern",
    "TemporalPattern",
    "GeographicPattern",
    "KeywordCluster"
]   