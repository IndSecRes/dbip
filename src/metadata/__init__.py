"""
Metadata Enrichment Package
Adds rich metadata to intelligence assets
"""

from .enricher import MetadataEnricher, EnrichedMetadata
from .extractor import ContextExtractor, EntityExtractor
from .classifiers import (
    Classifier,
    DomainClassifier,
    CategoryClassifier,
    TagGenerator
)

__all__ = [
    "MetadataEnricher",
    "EnrichedMetadata",
    "ContextExtractor",
    "EntityExtractor",
    "Classifier",
    "DomainClassifier",
    "CategoryClassifier",
    "TagGenerator"
]