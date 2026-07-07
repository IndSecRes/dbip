"""
Tests for data models
"""

import pytest
import uuid
from datetime import datetime

# Add src to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.models import (
    ProvenanceNode,
    IntelligenceSignal,
    CanonicalEntity,
    IntelligenceAsset,
    EvidenceRating,  # This is the MDIPS version
    SignalType,
    EntityType  # This is the MDIPS version
)


def test_provenance_node_creation():
    """Test creating a provenance node"""
    provenance = ProvenanceNode(
        source_id="test_source_001",
        source_type="API",
        confidence_score=0.8
    )
    
    assert provenance.node_id is not None
    assert provenance.source_id == "test_source_001"
    assert provenance.source_type == "API"
    assert provenance.confidence_score == 0.8
    assert provenance.collection_timestamp is not None


def test_intelligence_signal_creation():
    """Test creating an intelligence signal"""
    provenance = ProvenanceNode(
        source_id="test_source_001",
        source_type="API"
    )
    
    signal = IntelligenceSignal(
        provenance=provenance,
        raw_data={"content": "Test signal"},
        signal_type=SignalType.OBSERVED
    )
    
    assert signal.signal_id is not None
    assert signal.provenance.source_id == "test_source_001"
    assert signal.raw_data["content"] == "Test signal"
    assert signal.signal_type == SignalType.OBSERVED


def test_canonical_entity_creation():
    """Test creating a canonical entity"""
    entity = CanonicalEntity(
        entity_type=EntityType.PERSON,
        canonical_attributes={"name": "John Doe"},
        confidence=0.92
    )
    
    assert entity.entity_id is not None
    assert entity.entity_type == EntityType.PERSON
    assert entity.canonical_attributes["name"] == "John Doe"
    assert entity.confidence == 0.92
    assert entity.evidence_rating == EvidenceRating.D


def test_intelligence_asset_creation():
    """Test creating an intelligence asset"""
    asset = IntelligenceAsset(
        asset_type="identity_profile",
        title="John Doe Profile",
        description="Complete intelligence profile",
        content={"name": "John Doe"},
        confidence_score=0.92,
        evidence_rating=EvidenceRating.A
    )
    
    assert asset.asset_id is not None
    assert asset.asset_type == "identity_profile"
    assert asset.title == "John Doe Profile"
    assert asset.confidence_score == 0.92
    assert asset.evidence_rating == EvidenceRating.A
    assert asset.created_at is not None


def test_provenance_with_evidence_rating():
    """Test provenance node with evidence rating"""
    provenance = ProvenanceNode(
        source_id="test_source_001",
        source_type="API",
        confidence_score=0.9,
        evidence_rating=EvidenceRating.A
    )
    
    assert provenance.evidence_rating == EvidenceRating.A


def test_entity_evidence_rating_override():
    """Test entity evidence rating override"""
    entity = CanonicalEntity(
        entity_type=EntityType.ORGANIZATION,
        evidence_rating=EvidenceRating.B
    )
    
    assert entity.evidence_rating == EvidenceRating.B


def test_intelligence_signal_temporal_context():
    """Test intelligence signal with temporal context"""
    provenance = ProvenanceNode(
        source_id="test_source_001",
        source_type="API"
    )
    
    signal = IntelligenceSignal(
        provenance=provenance,
        raw_data={},
        temporal_context={"valid_from": datetime.now()}
    )
    
    assert "valid_from" in signal.temporal_context