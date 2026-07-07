"""
DBIP Core Data Models
MDIPS-compliant intelligence objects
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class EntityType(str, Enum):
    """Types of entities recognized by DBIP"""
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    EVENT = "event"
    ASSET = "asset"
    RELATIONSHIP = "relationship"


class EvidenceRating(str, Enum):
    """Evidence quality ratings"""
    A = "HIGH_CONFIDENCE"      # Multiple independent sources
    B = "MODERATE_CONFIDENCE"  # Multiple sources, some corroboration
    C = "LOW_CONFIDENCE"       # Single source or conflicting
    D = "UNVERIFIED"           # Unconfirmed intelligence


class SignalType(str, Enum):
    """Types of intelligence signals"""
    OBSERVED = "observed"
    INFERRED = "inferred"
    CORRELATED = "correlated"
    RESOLVED = "resolved"


class ProvenanceNode(BaseModel):
    """
    Tracks the complete lineage of data transformations
    """
    node_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str
    source_type: str  # 'API', 'Database', 'File', 'Stream'
    collection_timestamp: datetime = Field(default_factory=datetime.now)
    transformation_history: List[Dict[str, Any]] = []
    confidence_score: float = 0.0
    evidence_rating: Optional[EvidenceRating] = None


class IntelligenceSignal(BaseModel):
    """
    Raw intelligence signal before full processing
    """
    signal_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provenance: ProvenanceNode
    raw_data: Dict[str, Any]
    extracted_entities: List[Dict[str, Any]] = []
    signal_type: SignalType = SignalType.OBSERVED
    temporal_context: Dict[str, datetime] = {}
    confidence: float = 0.0


class CanonicalEntity(BaseModel):
    """
    Resolved entity after identity resolution
    """
    entity_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    entity_type: EntityType
    canonical_attributes: Dict[str, Any] = {}
    aliases: List[str] = []
    resolved_identities: List[str] = []  # UUIDs of resolved source identities
    confidence: float = 0.0
    evidence_rating: EvidenceRating = EvidenceRating.D
    last_updated: datetime = Field(default_factory=datetime.now)
    provenance_graph: List[ProvenanceNode] = []


class RelationshipObject(BaseModel):
    """
    Relationship between two entities
    """
    relationship_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_entity_id: str
    target_entity_id: str
    relationship_type: str  # 'belongs_to', 'located_at', 'associated_with', etc.
    relationship_attributes: Dict[str, Any] = {}
    confidence: float = 0.0
    provenance: List[ProvenanceNode] = []


class IntelligenceAsset(BaseModel):
    """
    Final intelligence product ready for distribution
    """
    asset_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_type: str  # 'signal', 'entity', 'dataset', 'relationship'
    title: str
    description: str
    content: Dict[str, Any]
    confidence_score: float
    evidence_rating: EvidenceRating
    temporal_validity: Dict[str, datetime] = {}
    provenance: List[ProvenanceNode] = []
    tags: List[str] = []
    classification: str = "unclassified"  # unclassified, confidential, secret
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = {}


# Test the models when run directly
if __name__ == "__main__":
    # Create a sample provenance node
    provenance = ProvenanceNode(
        source_id="test_source_001",
        source_type="API",
        confidence_score=0.8
    )
    
    print("✅ ProvenanceNode created successfully!")
    print(f"   Node ID: {provenance.node_id}")
    print(f"   Source: {provenance.source_id}")
    print(f"   Confidence: {provenance.confidence_score}")