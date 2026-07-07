"""
Tests for MDIPS v3.0 compliant models
"""

import pytest
from datetime import datetime
from src.models.mdips import (
    EntityType,
    RelationshipType,
    Domain,
    EvidenceRating,
    ConfidenceModel,
    ProvenanceEntry,
    ProvenanceChain,
    MDIPSEntity,
    MDIPSRelationship,
    MDPISSEvent,
    MDPISSEvidence,
    MDIPSObservation,
    MDIPSAssessment,
    MDIPSIntelligenceProduct,
    create_entity,
    create_relationship,
)


def test_confidence_model():
    """Test multi-dimensional confidence model"""
    confidence = ConfidenceModel(
        source_reliability=0.9,
        extraction_confidence=0.95,
        identity_confidence=0.92,
        relationship_confidence=0.85,
        temporal_confidence=0.88,
        analytical_confidence=0.90
    )
    
    assert confidence.source_reliability == 0.9
    assert confidence.overall > 0.85
    assert confidence.evidence_rating == EvidenceRating.A


def test_provenance_chain():
    """Test provenance chain tracking"""
    chain = ProvenanceChain()
    chain.add_entry(
        source_id="test_source",
        source_type="API",
        operation="collection",
        handler="collector_agent"
    )
    chain.add_entry(
        source_id="test_source",
        source_type="API",
        operation="extraction",
        handler="extractor_agent"
    )
    
    assert len(chain.entries) == 2
    assert chain.first.source_id == "test_source"
    assert chain.first.operation == "collection"
    assert chain.last.operation == "extraction"


def test_mdips_entity_creation():
    """Test MDIPS entity creation"""
    entity = create_entity(
        entity_type=EntityType.PERSON,
        label="John Doe",
        description="Test person",
        attributes={"phone": "+1-555-123-4567"},
        domains=[Domain.OSINT]
    )
    
    assert entity.entity_id.startswith("ENT_")
    assert entity.entity_type == EntityType.PERSON
    assert entity.label == "John Doe"
    assert entity.attributes["phone"] == "+1-555-123-4567"
    assert len(entity.provenance.entries) == 1


def test_mdips_relationship_creation():
    """Test MDIPS relationship creation"""
    entity1 = create_entity(EntityType.PERSON, "John Doe")
    entity2 = create_entity(EntityType.ORGANIZATION, "ACME Corp")
    
    relationship = create_relationship(
        source_entity_id=entity1.entity_id,
        target_entity_id=entity2.entity_id,
        relationship_type=RelationshipType.WORKS_AT,
        attributes={"role": "Data Analyst"}
    )
    
    assert relationship.relationship_id.startswith("REL_")
    assert relationship.source_entity_id == entity1.entity_id
    assert relationship.target_entity_id == entity2.entity_id
    assert relationship.relationship_type == RelationshipType.WORKS_AT


def test_mdips_event():
    """Test MDIPS event model"""
    event = MDPISSEvent(
        event_type="account_creation",
        description="New account created",
        entities=["ENT_001"],
        source="telegram_api"
    )
    
    assert event.event_id.startswith("EVT_")
    assert event.event_type == "account_creation"
    assert event.timestamp is not None


def test_mdips_evidence():
    """Test MDIPS evidence model"""
    evidence = MDPISSEvidence(
        evidence_type="screenshot",
        source="telegram_api",
        location="s3://evidence/001.png",
        hash="sha256:abc123"
    )
    
    assert evidence.evidence_id.startswith("EVD_")
    assert evidence.evidence_type == "screenshot"
    assert evidence.hash == "sha256:abc123"


def test_mdips_observation():
    """Test MDIPS observation model"""
    observation = MDIPSObservation(
        statement="Domain X resolves to IP Y",
        related_entities=["ENT_001", "ENT_002"],
        source="dns_lookup"
    )
    
    assert observation.observation_id.startswith("OBS_")
    assert observation.statement == "Domain X resolves to IP Y"
    assert len(observation.related_entities) == 2


def test_mdips_assessment():
    """Test MDIPS assessment model"""
    assessment = MDIPSAssessment(
        finding="Entity is likely associated with malicious activity",
        evidence_chain=["EVD_001", "EVD_002"],
        analyst_notes="Cross-referenced with threat intelligence feeds"
    )
    
    assert assessment.assessment_id.startswith("ASS_")
    assert "malicious" in assessment.finding
    assert len(assessment.evidence_chain) == 2


def test_mdips_intelligence_product():
    """Test MDIPS intelligence product"""
    product = MDIPSIntelligenceProduct(
        title="Threat Assessment Report",
        description="Comprehensive threat assessment",
        type="report",
        content={"findings": ["Threat actor identified"]},
        entities=["ENT_001"],
        tags=["threat", "assessment"]
    )
    
    assert product.product_id.startswith("PROD_")
    assert product.title == "Threat Assessment Report"
    assert product.classification == "unclassified"