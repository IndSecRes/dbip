"""
Identity Resolution Engine
Resolves entities across multiple sources into canonical identities
"""

import uuid
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field

from src.identity.matcher import (
    PhoneMatcher,
    EmailMatcher,
    PhoneticMatcher,
    AddressMatcher,
    RelationshipMatcher
)
from src.models.mdips import ConfidenceModel, EvidenceRating, MDIPSEntity


@dataclass
class ResolvedEntity:
    """Represents a resolved canonical entity"""
    entity_id: str
    canonical_id: str
    source_entity_ids: List[str]
    attributes: Dict[str, Any]
    aliases: List[str]
    confidence: ConfidenceModel
    evidence_rating: EvidenceRating
    resolved_at: datetime
    match_score: float
    
    @property
    def is_resolved(self) -> bool:
        """Check if entity was resolved from multiple sources"""
        return len(self.source_entity_ids) > 1


class IdentityResolver:
    """
    Identity Resolution Engine
    Performs blocking, scoring, and decision for entity resolution
    """
    
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        self.review_threshold = 0.70
        
        # Initialize matchers
        self.phone_matcher = PhoneMatcher()
        self.email_matcher = EmailMatcher()
        self.phonetic_matcher = PhoneticMatcher()
        self.address_matcher = AddressMatcher()
        self.relationship_matcher = RelationshipMatcher()
    
    def resolve_entities(self, entities: List[Dict[str, Any]]) -> List[ResolvedEntity]:
        """
        Resolve a list of entities into canonical identities
        
        Args:
            entities: List of entity dictionaries with attributes
            
        Returns:
            List of resolved entities
        """
        if not entities:
            return []
        
        # Phase 1: Blocking
        blocks = self._blocking(entities)
        
        # Phase 2: Scoring
        scores = self._scoring(blocks)
        
        # Phase 3: Decision
        resolved = self._decision(scores)
        
        return resolved
    
    def _blocking(self, entities: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Phase 1: Blocking - Reduce candidates using key attributes
        
        Creates blocks based on:
        - Phone numbers
        - Email addresses
        - Names (phonetic)
        - Addresses
        """
        blocks = {
            "phone": {},
            "email": {},
            "phonetic": {},
            "address": {}
        }
        
        for entity in entities:
            entity_id = entity.get("entity_id", str(uuid.uuid4()))
            
            # Phone blocking
            phones = entity.get("phone_numbers", [])
            for phone in phones:
                cleaned = self.phone_matcher.clean_phone(phone)
                if cleaned:
                    blocks["phone"].setdefault(cleaned, []).append(entity)
            
            # Email blocking
            emails = entity.get("emails", [])
            for email in emails:
                cleaned = self.email_matcher.clean_email(email)
                if cleaned:
                    blocks["email"].setdefault(cleaned, []).append(entity)
            
            # Phonetic blocking (name)
            name = entity.get("name", "") or entity.get("label", "")
            if name:
                soundex = self.phonetic_matcher.get_soundex(name)
                if soundex:
                    blocks["phonetic"].setdefault(soundex, []).append(entity)
            
            # Address blocking
            address = entity.get("address", "")
            if address:
                normalized = self.address_matcher.normalize_address(address)
                if normalized:
                    blocks["address"].setdefault(normalized, []).append(entity)
        
        return blocks
    
    def _scoring(self, blocks: Dict) -> List[Dict]:
        """
        Phase 2: Scoring - Calculate similarity scores between candidates
        
        Returns:
            List of candidate pairs with scores
        """
        candidates = []
        
        # Process each block
        for block_type, block_data in blocks.items():
            for key, entities in block_data.items():
                if len(entities) < 2:
                    continue
                
                # Compare each pair in the block
                for i in range(len(entities)):
                    for j in range(i + 1, len(entities)):
                        entity1 = entities[i]
                        entity2 = entities[j]
                        
                        # Calculate composite score
                        score = self._calculate_score(entity1, entity2)
                        
                        candidates.append({
                            "entity1": entity1,
                            "entity2": entity2,
                            "score": score,
                            "block_type": block_type,
                            "block_key": key
                        })
        
        return candidates
    
    def _calculate_score(self, entity1: Dict, entity2: Dict) -> float:
        """
        Calculate composite similarity score between two entities
        
        Weights:
        - Phone: 0.25
        - Email: 0.20
        - Name (phonetic): 0.20
        - Address: 0.15
        - Relationships: 0.20
        """
        scores = {
            "phone": self.phone_matcher.match(entity1, entity2),
            "email": self.email_matcher.match(entity1, entity2),
            "phonetic": self.phonetic_matcher.match(entity1, entity2),
            "address": self.address_matcher.match(entity1, entity2),
            "relationship": self.relationship_matcher.match(entity1, entity2)
        }
        
        # Weighted average
        weights = {
            "phone": 0.25,
            "email": 0.20,
            "phonetic": 0.20,
            "address": 0.15,
            "relationship": 0.20
        }
        
        total = sum(scores[key] * weights[key] for key in weights)
        return round(min(total, 1.0), 3)
    
    def _decision(self, candidates: List[Dict]) -> List[ResolvedEntity]:
        """
        Phase 3: Decision - Merge, Reject, or Review
        """
        resolved = []
        processed = set()
        
        # Collect all entities from candidates
        all_entities = {}
        for candidate in candidates:
            entity1 = candidate.get("entity1", {})
            entity2 = candidate.get("entity2", {})
            entity1_id = entity1.get("entity_id", str(uuid.uuid4()))
            entity2_id = entity2.get("entity_id", str(uuid.uuid4()))
            all_entities[entity1_id] = entity1
            all_entities[entity2_id] = entity2
        
        # Sort candidates by score descending
        candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        for candidate in candidates:
            entity1 = candidate.get("entity1", {})
            entity2 = candidate.get("entity2", {})
            entity1_id = entity1.get("entity_id", "")
            entity2_id = entity2.get("entity_id", "")
            score = candidate.get("score", 0)
            
            # Skip if either entity already processed
            if entity1_id in processed or entity2_id in processed:
                continue
            
            if score >= self.threshold:
                # MERGE - High confidence, merge entities
                merged = self._merge_entities(entity1, entity2)
                resolved.append(merged)
                processed.add(entity1_id)
                processed.add(entity2_id)
            elif score >= self.review_threshold:
                # REVIEW - Medium confidence
                processed.add(entity1_id)
                processed.add(entity2_id)
                # Keep them separate for now
                resolved.append(self._create_resolved_entity([entity1]))
                resolved.append(self._create_resolved_entity([entity2]))
            else:
                # REJECT - Low confidence
                processed.add(entity1_id)
                processed.add(entity2_id)
                resolved.append(self._create_resolved_entity([entity1]))
                resolved.append(self._create_resolved_entity([entity2]))
        
        # Add any entities that weren't processed
        for entity_id, entity in all_entities.items():
            if entity_id not in processed:
                resolved.append(self._create_resolved_entity([entity]))
                processed.add(entity_id)
        
        return resolved
    
    def _merge_entities(self, entity1: Dict, entity2: Dict) -> ResolvedEntity:
        """Merge two entities into a canonical entity"""
        # Combine attributes
        attributes = {}
        for key in set(entity1.keys()) | set(entity2.keys()):
            if key in entity1 and key in entity2:
                if isinstance(entity1[key], list) and isinstance(entity2[key], list):
                    # Merge lists
                    attributes[key] = list(set(entity1[key] + entity2[key]))
                elif isinstance(entity1[key], dict) and isinstance(entity2[key], dict):
                    # Merge dicts (prefer entity1 values)
                    attributes[key] = {**entity2[key], **entity1[key]}
                else:
                    # Prefer entity1
                    attributes[key] = entity1[key]
            elif key in entity1:
                attributes[key] = entity1[key]
            else:
                attributes[key] = entity2[key]
        
        # Combine aliases
        aliases = list(set(
            entity1.get("aliases", []) + 
            entity2.get("aliases", []) +
            [entity1.get("name", ""), entity2.get("name", "")]
        ))
        aliases = [a for a in aliases if a]
        
        # Calculate confidence
        confidence = ConfidenceModel(
            source_reliability=max(
                entity1.get("confidence", {}).get("source_reliability", 0.5),
                entity2.get("confidence", {}).get("source_reliability", 0.5)
            ),
            extraction_confidence=0.9,
            identity_confidence=0.95,
            relationship_confidence=0.85,
            temporal_confidence=0.9,
            analytical_confidence=0.9
        )
        
        return ResolvedEntity(
            entity_id=str(uuid.uuid4()),
            canonical_id=f"CAN_{uuid.uuid4().hex[:8].upper()}",
            source_entity_ids=[entity1.get("entity_id", ""), entity2.get("entity_id", "")],
            attributes=attributes,
            aliases=aliases,
            confidence=confidence,
            evidence_rating=confidence.evidence_rating,
            resolved_at=datetime.now(),
            match_score=0.95
        )
    
    def _create_resolved_entity(self, entities: List[Dict]) -> ResolvedEntity:
        """Create a resolved entity from a single source"""
        if not entities:
            return None
        
        entity = entities[0]
        confidence = entity.get("confidence", ConfidenceModel())
        if isinstance(confidence, dict):
            confidence = ConfidenceModel(**confidence)
        
        return ResolvedEntity(
            entity_id=entity.get("entity_id", str(uuid.uuid4())),
            canonical_id=f"CAN_{uuid.uuid4().hex[:8].upper()}",
            source_entity_ids=[entity.get("entity_id", "")],
            attributes=entity.get("attributes", {}),
            aliases=entity.get("aliases", []),
            confidence=confidence,
            evidence_rating=confidence.evidence_rating,
            resolved_at=datetime.now(),
            match_score=1.0
        )


def create_resolved_entity_from_sources(
    entities: List[Dict[str, Any]],
    threshold: float = 0.85
) -> List[ResolvedEntity]:
    """Factory function to resolve entities from multiple sources"""
    resolver = IdentityResolver(threshold)
    return resolver.resolve_entities(entities)