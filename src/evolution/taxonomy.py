"""
Taxonomy Manager
Manages taxonomy evolution and proposals
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import json


@dataclass
class CategoryProposal:
    """Proposal for a new category"""
    name: str
    description: str
    proposal_id: str = field(default_factory=lambda: f"PROP_{uuid.uuid4().hex[:8].upper()}")
    parent_category: Optional[str] = None
    subcategories: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    status: str = "proposed"  # proposed, approved, rejected, implemented
    created_at: datetime = field(default_factory=datetime.now)
    approved_at: Optional[datetime] = None
    implemented_at: Optional[datetime] = None
    feedback: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class EntityTypeProposal:
    """Proposal for a new entity type"""
    name: str
    description: str
    proposal_id: str = field(default_factory=lambda: f"ETP_{uuid.uuid4().hex[:8].upper()}")
    parent_type: Optional[str] = None
    attributes: List[str] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    status: str = "proposed"
    created_at: datetime = field(default_factory=datetime.now)


class TaxonomyManager:
    """
    Manages taxonomy evolution
    """
    
    def __init__(self):
        self.categories: Dict[str, Dict[str, Any]] = {}
        self.entity_types: Dict[str, Dict[str, Any]] = {}
        self.category_proposals: List[CategoryProposal] = []
        self.entity_type_proposals: List[EntityTypeProposal] = []
        
        # Initialize with default taxonomy
        self._initialize_taxonomy()
    
    def _initialize_taxonomy(self) -> None:
        """Initialize with default taxonomy"""
        # Default categories
        default_categories = [
            {"name": "individual", "description": "Individual persons"},
            {"name": "organization", "description": "Organizations and companies"},
            {"name": "event", "description": "Events and incidents"},
            {"name": "location", "description": "Geographic locations"},
            {"name": "financial", "description": "Financial matters"},
            {"name": "technical", "description": "Technical topics"},
            {"name": "threat", "description": "Threats and risks"},
            {"name": "intelligence", "description": "Intelligence matters"}
        ]
        for cat in default_categories:
            self.categories[cat["name"]] = cat
        
        # Default entity types
        default_entity_types = [
            {"name": "person", "description": "Individual person"},
            {"name": "organization", "description": "Organization or company"},
            {"name": "location", "description": "Physical location"},
            {"name": "domain", "description": "Domain name"},
            {"name": "ip_address", "description": "IP address"},
            {"name": "email", "description": "Email address"},
            {"name": "account", "description": "User account"},
            {"name": "document", "description": "Document file"}
        ]
        for et in default_entity_types:
            self.entity_types[et["name"]] = et
    
    def propose_category(self, name: str, description: str, evidence: List[Dict[str, Any]]) -> CategoryProposal:
        """Propose a new category"""
        proposal = CategoryProposal(
            name=name,
            description=description,
            evidence=evidence,
            confidence=self._calculate_confidence(evidence)
        )
        self.category_proposals.append(proposal)
        return proposal
    
    def propose_entity_type(self, name: str, description: str, evidence: List[Dict[str, Any]]) -> EntityTypeProposal:
        """Propose a new entity type"""
        proposal = EntityTypeProposal(
            name=name,
            description=description,
            evidence=evidence,
            confidence=self._calculate_confidence(evidence)
        )
        self.entity_type_proposals.append(proposal)
        return proposal
    
    def approve_category(self, proposal_id: str) -> bool:
        """Approve a category proposal"""
        proposal = self._find_category_proposal(proposal_id)
        if not proposal:
            return False
        
        proposal.status = "approved"
        proposal.approved_at = datetime.now()
        return True
    
    def implement_category(self, proposal_id: str) -> bool:
        """Implement an approved category proposal"""
        proposal = self._find_category_proposal(proposal_id)
        if not proposal or proposal.status != "approved":
            return False
        
        # Add to taxonomy
        self.categories[proposal.name] = {
            "name": proposal.name,
            "description": proposal.description,
            "parent": proposal.parent_category,
            "subcategories": proposal.subcategories,
            "keywords": proposal.keywords,
            "implemented_at": datetime.now().isoformat()
        }
        
        proposal.status = "implemented"
        proposal.implemented_at = datetime.now()
        return True
    
    def reject_proposal(self, proposal_id: str, reason: str) -> bool:
        """Reject a proposal"""
        proposal = self._find_category_proposal(proposal_id)
        if not proposal:
            proposal = self._find_entity_type_proposal(proposal_id)
        
        if not proposal:
            return False
        
        proposal.status = "rejected"
        proposal.feedback.append({"reason": reason, "timestamp": datetime.now().isoformat()})
        return True
    
    def get_pending_proposals(self) -> Dict[str, Any]:
        """Get all pending proposals"""
        pending_categories = [p for p in self.category_proposals if p.status == "proposed"]
        pending_entity_types = [p for p in self.entity_type_proposals if p.status == "proposed"]
        
        return {
            "pending_categories": len(pending_categories),
            "pending_entity_types": len(pending_entity_types),
            "categories": [
                {
                    "id": p.proposal_id,
                    "name": p.name,
                    "description": p.description,
                    "confidence": p.confidence,
                    "evidence_count": len(p.evidence)
                }
                for p in pending_categories[:10]
            ],
            "entity_types": [
                {
                    "id": p.proposal_id,
                    "name": p.name,
                    "description": p.description,
                    "confidence": p.confidence,
                    "evidence_count": len(p.evidence)
                }
                for p in pending_entity_types[:10]
            ]
        }
    
    def get_taxonomy(self) -> Dict[str, Any]:
        """Get current taxonomy"""
        return {
            "categories": list(self.categories.values()),
            "entity_types": list(self.entity_types.values()),
            "total_categories": len(self.categories),
            "total_entity_types": len(self.entity_types)
        }
    
    def _find_category_proposal(self, proposal_id: str) -> Optional[CategoryProposal]:
        """Find a category proposal by ID"""
        for p in self.category_proposals:
            if p.proposal_id == proposal_id:
                return p
        return None
    
    def _find_entity_type_proposal(self, proposal_id: str) -> Optional[EntityTypeProposal]:
        """Find an entity type proposal by ID"""
        for p in self.entity_type_proposals:
            if p.proposal_id == proposal_id:
                return p
        return None
    
    def _calculate_confidence(self, evidence: List[Dict[str, Any]]) -> float:
        """Calculate confidence from evidence"""
        if not evidence:
            return 0.3
        
        # Weighted confidence based on evidence quality
        confidence = 0.5
        for e in evidence:
            if e.get("source_reliability", 0) > 0.8:
                confidence += 0.1
            if e.get("corroboration_count", 0) > 1:
                confidence += 0.05
        
        return min(0.95, confidence)