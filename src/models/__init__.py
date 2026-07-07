"""
DBIP Models Package
Contains MDIPS-compliant intelligence models
"""

# Import legacy models from legacy_models.py
from ..legacy_models import (
    ProvenanceNode,
    IntelligenceSignal,
    CanonicalEntity,
    IntelligenceAsset,
    EvidenceRating as LegacyEvidenceRating,
    SignalType,
    EntityType as LegacyEntityType
)

# MDIPS v3.0 Models
from .mdips import (
    # Enums
    EntityType,
    RelationshipType,
    Domain,
    EvidenceRating,
    
    # Core Models
    ConfidenceModel,
    ProvenanceEntry,
    ProvenanceChain,
    
    # MDIPS Objects
    MDIPSEntity,
    MDIPSRelationship,
    MDPISSEvent,
    MDPISSEvidence,
    MDIPSObservation,
    MDIPSAssessment,
    MDIPSIntelligenceProduct,
    
    # Factory Functions
    create_entity,
    create_relationship,
)

__all__ = [
    # Legacy
    "ProvenanceNode",
    "IntelligenceSignal",
    "CanonicalEntity",
    "IntelligenceAsset",
    "LegacyEvidenceRating",
    "SignalType",
    "LegacyEntityType",
    
    # MDIPS v3.0
    "EntityType",
    "RelationshipType",
    "Domain",
    "EvidenceRating",
    "ConfidenceModel",
    "ProvenanceEntry",
    "ProvenanceChain",
    "MDIPSEntity",
    "MDIPSRelationship",
    "MDPISSEvent",
    "MDPISSEvidence",
    "MDIPSObservation",
    "MDIPSAssessment",
    "MDIPSIntelligenceProduct",
    "create_entity",
    "create_relationship",
]