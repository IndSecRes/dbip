"""
MDIPS v3.0 - Multi-Domain Intelligence Protocol Standard
Semantic Ontology, Intelligence Object Model & Interoperability Framework

This module implements the MDIPS standard for intelligence objects.
All objects are MDIPS-compliant and include:
- Complete provenance
- Multi-dimensional confidence
- Evidence tracking
- Relationship modeling
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Literal, Union
from pydantic import BaseModel, Field, validator
import uuid
from enum import Enum

# ============================================================================
# CORE ENUMS
# ============================================================================

class EntityType(str, Enum):
    """Core entity types defined by MDIPS"""
    # Human Domain
    PERSON = "person"
    ORGANIZATION = "organization"
    GROUP = "group"
    ROLE = "role"
    
    # Cyber Domain
    DOMAIN = "domain"
    IP_ADDRESS = "ip_address"
    URL = "url"
    EMAIL = "email"
    ACCOUNT = "account"
    DEVICE = "device"
    MALWARE = "malware"
    INFRASTRUCTURE = "infrastructure"
    
    # Financial Domain
    WALLET = "wallet"
    TRANSACTION = "transaction"
    BANK_ACCOUNT = "bank_account"
    ASSET = "asset"
    
    # Physical Domain
    LOCATION = "location"
    FACILITY = "facility"
    EVENT = "event"
    
    # Knowledge Domain
    DOCUMENT = "document"
    DATASET = "dataset"
    REPORT = "report"
    SOURCE = "source"


class RelationshipType(str, Enum):
    """Core relationship types defined by MDIPS"""
    # Ownership
    OWNS = "owns"
    CONTROLS = "controls"
    MANAGES = "manages"
    
    # Association
    LINKED_TO = "linked_to"
    ASSOCIATED_WITH = "associated_with"
    AFFILIATED_WITH = "affiliated_with"
    
    # Communication
    COMMUNICATES_WITH = "communicates_with"
    
    # Infrastructure
    HOSTS = "hosts"
    REGISTERED_WITH = "registered_with"
    USES = "uses"
    
    # Financial
    TRANSFERS_TO = "transfers_to"
    TRANSACTS_WITH = "transacts_with"
    
    # Evidence
    DERIVED_FROM = "derived_from"
    SUPPORTED_BY = "supported_by"
    CONTRADICTS = "contradicts"
    
    # Spatial
    LOCATED_AT = "located_at"
    CONTAINS = "contains"
    IMPLEMENTS = "implements"
    BELONGS_TO = "belongs_to"
    
    # Employment (ADD THESE)
    WORKS_AT = "works_at"
    EMPLOYS = "employs"
    CONTRACTS = "contracts"
    
    # Social
    FRIEND_OF = "friend_of"
    FOLLOWS = "follows"
    MENTIONS = "mentions"


class Domain(str, Enum):
    """Intelligence domains"""
    OSINT = "osint"     # Open Source Intelligence
    SOCMINT = "socmint" # Social Media Intelligence
    CYBINT = "cybint"   # Cyber Intelligence
    FININT = "finint"   # Financial Intelligence
    GEOINT = "geoint"   # Geospatial Intelligence
    IMINT = "imint"     # Image Intelligence
    DFIR = "dfir"       # Digital Forensics
    SIGINT = "sigint"   # Signals Intelligence


class EvidenceRating(str, Enum):
    """Evidence quality ratings"""
    A = "HIGH_CONFIDENCE"      # Multiple independent sources, strong corroboration
    B = "MODERATE_CONFIDENCE"  # Multiple sources, some corroboration
    C = "LOW_CONFIDENCE"       # Single source or conflicting evidence
    D = "UNVERIFIED"           # Unconfirmed intelligence


# ============================================================================
# CORE MODELS
# ============================================================================

class ConfidenceModel(BaseModel):
    """
    Multi-dimensional confidence framework (MDIPS v3)
    Confidence is tracked across multiple dimensions, not as a single score.
    """
    source_reliability: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Reliability of the source (0-1)"
    )
    extraction_confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence in extraction quality (0-1)"
    )
    identity_confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence in entity identity (0-1)"
    )
    relationship_confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence in relationship validity (0-1)"
    )
    temporal_confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence in temporal accuracy (0-1)"
    )
    analytical_confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence in analytical reasoning (0-1)"
    )
    
    @property
    def overall(self) -> float:
        """Calculate overall confidence as weighted average"""
        weights = {
            "source_reliability": 0.25,
            "extraction_confidence": 0.15,
            "identity_confidence": 0.20,
            "relationship_confidence": 0.15,
            "temporal_confidence": 0.10,
            "analytical_confidence": 0.15
        }
        total = 0
        for dim, weight in weights.items():
            total += getattr(self, dim) * weight
        return round(total, 3)
    
    @property
    def evidence_rating(self) -> EvidenceRating:
        """Convert confidence to evidence rating"""
        score = self.overall
        if score >= 0.85:
            return EvidenceRating.A
        elif score >= 0.70:
            return EvidenceRating.B
        elif score >= 0.50:
            return EvidenceRating.C
        else:
            return EvidenceRating.D


class ProvenanceEntry(BaseModel):
    """
    Provenance tracking for intelligence objects (MDIPS v3)
    Every object must maintain complete traceability.
    """
    source_id: str
    source_type: str = Field(description="API, Database, File, Stream, Manual")
    operation: str = Field(description="Collection, Extraction, Transformation, Fusion")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    handler: Optional[str] = Field(default=None, description="System or person responsible")
    version: str = Field(default="1.0")
    notes: Optional[str] = None


class ProvenanceChain(BaseModel):
    """
    Complete provenance chain for an intelligence object
    """
    entries: List[ProvenanceEntry] = Field(default_factory=list)
    
    def add_entry(
        self,
        source_id: str,
        source_type: str,
        operation: str,
        handler: Optional[str] = None,
        version: str = "1.0",
        notes: Optional[str] = None
    ) -> None:
        """Add a provenance entry to the chain"""
        self.entries.append(
            ProvenanceEntry(
                source_id=source_id,
                source_type=source_type,
                operation=operation,
                handler=handler,
                version=version,
                notes=notes
            )
        )
    
    @property
    def first(self) -> Optional[ProvenanceEntry]:
        """Get the first provenance entry (original source)"""
        return self.entries[0] if self.entries else None
    
    @property
    def last(self) -> Optional[ProvenanceEntry]:
        """Get the last provenance entry (most recent)"""
        return self.entries[-1] if self.entries else None


# ============================================================================
# MDIPS OBJECT MODELS
# ============================================================================

class MDIPSEntity(BaseModel):
    """
    MDIPS v3 Entity Model
    Represents any entity in the intelligence ecosystem.
    """
    entity_id: str = Field(default_factory=lambda: f"ENT_{uuid.uuid4().hex[:16].upper()}")
    entity_type: EntityType
    label: str
    description: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    domains: List[Domain] = Field(default_factory=list)
    confidence: ConfidenceModel = Field(default_factory=ConfidenceModel)
    provenance: ProvenanceChain = Field(default_factory=ProvenanceChain)
    created_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def add_attribute(self, key: str, value: Any) -> None:
        """Add or update an attribute"""
        self.attributes[key] = value
        self.updated_time = datetime.now(timezone.utc)


class MDIPSRelationship(BaseModel):
    """
    MDIPS v3 Relationship Model
    Represents a relationship between two entities.
    """
    relationship_id: str = Field(default_factory=lambda: f"REL_{uuid.uuid4().hex[:16].upper()}")
    source_entity_id: str
    target_entity_id: str
    relationship_type: RelationshipType
    attributes: Dict[str, Any] = Field(default_factory=dict)
    confidence: ConfidenceModel = Field(default_factory=ConfidenceModel)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_chain: List[str] = Field(default_factory=list)
    provenance: ProvenanceChain = Field(default_factory=ProvenanceChain)


class MDPISSEvent(BaseModel):
    """
    MDIPS v3 Event Model
    Events represent change over time.
    """
    event_id: str = Field(default_factory=lambda: f"EVT_{uuid.uuid4().hex[:16].upper()}")
    event_type: str
    description: str
    entities: List[str] = Field(default_factory=list)  # Entity IDs
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: str
    confidence: ConfidenceModel = Field(default_factory=ConfidenceModel)
    provenance: ProvenanceChain = Field(default_factory=ProvenanceChain)
    attributes: Dict[str, Any] = Field(default_factory=dict)


class MDPISSEvidence(BaseModel):
    """
    MDIPS v3 Evidence Model
    Evidence separates fact from interpretation.
    """
    evidence_id: str = Field(default_factory=lambda: f"EVD_{uuid.uuid4().hex[:16].upper()}")
    evidence_type: str = Field(description="screenshot, document, message, log, etc.")
    source: str
    content: Optional[Dict[str, Any]] = None
    location: Optional[str] = Field(default=None, description="URL, file path, or reference")
    hash: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    chain_of_custody: List[ProvenanceEntry] = Field(default_factory=list)
    confidence: ConfidenceModel = Field(default_factory=ConfidenceModel)
    provenance: ProvenanceChain = Field(default_factory=ProvenanceChain)


class MDIPSObservation(BaseModel):
    """
    MDIPS v3 Observation Model
    Represents detected information (raw signal).
    """
    observation_id: str = Field(default_factory=lambda: f"OBS_{uuid.uuid4().hex[:16].upper()}")
    statement: str
    related_entities: List[str] = Field(default_factory=list)
    source: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    confidence: ConfidenceModel = Field(default_factory=ConfidenceModel)
    provenance: ProvenanceChain = Field(default_factory=ProvenanceChain)


class MDIPSAssessment(BaseModel):
    """
    MDIPS v3 Assessment Model
    Represents intelligence findings and assessments.
    """
    assessment_id: str = Field(default_factory=lambda: f"ASS_{uuid.uuid4().hex[:16].upper()}")
    finding: str
    evidence_chain: List[str] = Field(default_factory=list)  # Evidence IDs
    confidence: ConfidenceModel = Field(default_factory=ConfidenceModel)
    analyst_notes: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provenance: ProvenanceChain = Field(default_factory=ProvenanceChain)


class MDIPSIntelligenceProduct(BaseModel):
    """
    MDIPS v3 Intelligence Product
    Final intelligence product ready for distribution.
    """
    product_id: str = Field(default_factory=lambda: f"PROD_{uuid.uuid4().hex[:16].upper()}")
    title: str
    description: str
    type: str = Field(description="report, brief, dossier, alert, etc.")
    content: Dict[str, Any]
    entities: List[str] = Field(default_factory=list)  # Entity IDs
    relationships: List[str] = Field(default_factory=list)  # Relationship IDs
    evidence: List[str] = Field(default_factory=list)  # Evidence IDs
    confidence: ConfidenceModel = Field(default_factory=ConfidenceModel)
    classification: str = Field(default="unclassified")
    tags: List[str] = Field(default_factory=list)
    created_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provenance: ProvenanceChain = Field(default_factory=ProvenanceChain)


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_entity(
    entity_type: EntityType,
    label: str,
    description: Optional[str] = None,
    attributes: Optional[Dict[str, Any]] = None,
    domains: Optional[List[Domain]] = None,
    source_id: str = "manual",
    source_type: str = "Manual"
) -> MDIPSEntity:
    """Factory function to create a new MDIPS entity"""
    entity = MDIPSEntity(
        entity_type=entity_type,
        label=label,
        description=description,
        attributes=attributes or {},
        domains=domains or []
    )
    entity.provenance.add_entry(
        source_id=source_id,
        source_type=source_type,
        operation="creation"
    )
    return entity


def create_relationship(
    source_entity_id: str,
    target_entity_id: str,
    relationship_type: RelationshipType,
    attributes: Optional[Dict[str, Any]] = None,
    source_id: str = "manual",
    source_type: str = "Manual"
) -> MDIPSRelationship:
    """Factory function to create a new MDIPS relationship"""
    relationship = MDIPSRelationship(
        source_entity_id=source_entity_id,
        target_entity_id=target_entity_id,
        relationship_type=relationship_type,
        attributes=attributes or {}
    )
    relationship.provenance.add_entry(
        source_id=source_id,
        source_type=source_type,
        operation="creation"
    )
    return relationship


# ============================================================================
# TEST / DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MDIPS v3.0 Model Test")
    print("=" * 60)
    
    # Create a person entity
    print("\n📌 Creating Person Entity:")
    person = create_entity(
        entity_type=EntityType.PERSON,
        label="John Doe",
        description="Individual identified through chatter analysis",
        attributes={
            "phone_numbers": ["+1-555-123-4567"],
            "emails": ["john.doe@email.com"],
            "social_media": {
                "telegram": "@johndoe",
                "twitter": "@johndoe_nyc"
            }
        },
        domains=[Domain.OSINT, Domain.SOCMINT]
    )
    print(f"   Entity ID: {person.entity_id}")
    print(f"   Label: {person.label}")
    print(f"   Attributes: {len(person.attributes)} fields")
    
    # Create an organization entity
    print("\n📌 Creating Organization Entity:")
    org = create_entity(
        entity_type=EntityType.ORGANIZATION,
        label="ACME Corp",
        description="Technology company expanding to NYC",
        attributes={
            "industry": "Technology",
            "employees": 5000,
            "founded": 1990
        },
        domains=[Domain.OSINT, Domain.FININT]
    )
    print(f"   Entity ID: {org.entity_id}")
    print(f"   Label: {org.label}")
    
    # Create relationship between person and organization
    print("\n📌 Creating Relationship:")
    relationship = create_relationship(
        source_entity_id=person.entity_id,
        target_entity_id=org.entity_id,
        relationship_type=RelationshipType.ASSOCIATED_WITH,
        attributes={"role": "Data Analyst", "start_date": "2024-01-01"}
    )
    print(f"   Relationship ID: {relationship.relationship_id}")
    print(f"   Type: {relationship.relationship_type}")
    print(f"   {person.label} → WORKS_AT → {org.label}")
    
    # Test confidence
    print("\n📌 Confidence Test:")
    confidence = ConfidenceModel(
        source_reliability=0.90,
        extraction_confidence=0.95,
        identity_confidence=0.92,
        relationship_confidence=0.85,
        temporal_confidence=0.88,
        analytical_confidence=0.90
    )
    print(f"   Overall Confidence: {confidence.overall}")
    print(f"   Evidence Rating: {confidence.evidence_rating}")
    
    print("\n✅ MDIPS models test completed!")