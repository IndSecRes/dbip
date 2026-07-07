"""
Tests for Metadata Enrichment
"""

import pytest
from src.metadata import (
    MetadataEnricher,
    DomainClassifier,
    CategoryClassifier,
    TagGenerator,
    ContextExtractor,
    EntityExtractor
)


def test_domain_classifier():
    """Test domain classification"""
    classifier = DomainClassifier()
    
    content = {
        "message": "ACME Corp is opening a new office in NYC",
        "metadata": {"source": "twitter"}
    }
    
    domains = classifier.classify(content)
    
    assert len(domains) >= 1
    assert "osint" in domains or "socmint" in domains


def test_category_classifier():
    """Test category classification"""
    classifier = CategoryClassifier()
    
    content = {
        "message": "John Doe joined ACME Corp as CEO"
    }
    
    categories = classifier.classify(content)
    
    assert len(categories) >= 1


def test_tag_generator():
    """Test tag generation"""
    generator = TagGenerator(max_tags=5)
    
    content = {
        "message": "ACME Corp announces new office in New York City with 500 employees"
    }
    
    tags = generator.classify(content)
    
    assert len(tags) <= 5
    assert len(tags) > 0


def test_context_extractor():
    """Test context extraction"""
    extractor = ContextExtractor()
    
    content = {
        "message": "Meeting tomorrow in NYC for ACME Corp expansion",
        "timestamp": "2026-07-07T14:30:00Z"
    }
    
    temporal = extractor.extract_temporal(content)
    geographic = extractor.extract_geographic(content)
    sentiment = extractor.extract_sentiment(content)
    
    assert "temporal_span" in temporal or "time_references" in temporal
    assert "detected_locations" in geographic
    assert "sentiment" in sentiment


def test_entity_extractor():
    """Test entity extraction"""
    extractor = EntityExtractor()
    
    text = "John Doe works at ACME Corp in New York City using Python and Docker"
    
    names = extractor.extract_person_names(text)
    organizations = extractor.extract_organizations(text)
    technologies = extractor.extract_technologies(text)
    
    assert len(names) >= 1
    assert len(organizations) >= 1
    assert len(technologies) >= 1


def test_metadata_enricher():
    """Test full metadata enrichment"""
    enricher = MetadataEnricher()
    
    asset = {
        "asset_id": "TEST_001",
        "title": "Test Asset",
        "content": {
            "message": "John Doe from ACME Corp is moving to New York City"
        }
    }
    
    enriched = enricher.enrich_dictionary(asset)
    
    assert "metadata" in enriched
    assert "classification" in enriched["metadata"]
    assert "context" in enriched["metadata"]
    assert "entities" in enriched["metadata"]
    assert "quality" in enriched["metadata"]
    assert "tags" in enriched["metadata"]["classification"]