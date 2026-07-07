"""
Evolution Engine
Self-improving taxonomy and categories
"""

from .engine import EvolutionEngine
from .patterns import PatternDiscovery, EntityPattern, TemporalPattern, CategoryPattern
from .taxonomy import TaxonomyManager, CategoryProposal, EntityTypeProposal
from .feedback import FeedbackSystem, FeedbackEntry

__all__ = [
    "EvolutionEngine",
    "PatternDiscovery",
    "EntityPattern",
    "TemporalPattern",
    "CategoryPattern",
    "TaxonomyManager",
    "CategoryProposal",
    "EntityTypeProposal",
    "FeedbackSystem",
    "FeedbackEntry"
]   