"""
Evidence Assessment Engine
Transforms raw signals into structured, confidence-scored evidence
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import uuid

from src.models.mdips import (
    MDPISSEvidence,
    ConfidenceModel,
    EvidenceRating,
    ProvenanceEntry,
    ProvenanceChain
)


class EvidenceAssessor:
    """
    Assesses and structures evidence from raw signals.
    Converts signals to MDIPS-compliant evidence objects.
    """
    
    def __init__(self):
        self.chain_of_custody: List[Dict[str, Any]] = []
    
    def assess_evidence(
        self,
        signal: Dict[str, Any],
        source_reliability: float = 0.7,
        extraction_confidence: float = 0.8
    ) -> MDPISSEvidence:
        """Assess a single signal and convert to evidence"""
        
        # Generate evidence hash
        evidence_hash = self._generate_hash(signal)
        
        # Determine evidence type
        evidence_type = self._determine_evidence_type(signal)
        
        # Create confidence model
        confidence = ConfidenceModel(
            source_reliability=source_reliability,
            extraction_confidence=extraction_confidence,
            identity_confidence=0.7,
            relationship_confidence=0.6,
            temporal_confidence=0.8,
            analytical_confidence=0.7
        )
        
        # Build evidence
        evidence = MDPISSEvidence(
            evidence_type=evidence_type,
            source=signal.get("source", "unknown"),
            content=signal.get("content", {}),
            location=signal.get("location", None),
            hash=evidence_hash,
            confidence=confidence,
            timestamp=datetime.now(timezone.utc),
            supporting_sources=[],
            corroborating_evidence=[],
            contradictory_evidence=[]
        )
        
        # Add chain of custody
        evidence.chain_of_custody.append(
            ProvenanceEntry(
                source_id=signal.get("source_id", "unknown"),
                source_type=signal.get("source_type", "unknown"),
                operation="collection",
                timestamp=datetime.now(timezone.utc)
            )
        )
        
        return evidence
    
    def assess_multiple_signals(
        self,
        signals: List[Dict[str, Any]],
        source_reliability: float = 0.7,
        extraction_confidence: float = 0.8
    ) -> List[MDPISSEvidence]:
        """Assess multiple signals and return evidence objects"""
        evidence_list = []
        for signal in signals:
            evidence = self.assess_evidence(signal, source_reliability, extraction_confidence)
            evidence_list.append(evidence)
        return evidence_list
    
    def corroborate_evidence(
        self,
        evidence_list: List[MDPISSEvidence]
    ) -> List[Dict[str, Any]]:
        """Corroborate multiple pieces of evidence"""
        results = []
        
        for evidence in evidence_list:
            # Find corroborating evidence
            corroborating = self._find_corroborating_evidence(evidence, evidence_list)
            contradictory = self._find_contradictory_evidence(evidence, evidence_list)
            
            # Update evidence with corroboration info
            evidence.corroborating_evidence = [e.evidence_id for e in corroborating]
            evidence.contradictory_evidence = [e.evidence_id for e in contradictory]
            
            # Calculate corroboration score
            corroboration_score = self._calculate_corroboration_score(
                evidence, corroborating, contradictory
            )
            
            # Update confidence based on corroboration
            if corroboration_score > 0.5:
                evidence.confidence.source_reliability = min(
                    1.0, evidence.confidence.source_reliability + 0.1
                )
                evidence.confidence.analytical_confidence = min(
                    1.0, evidence.confidence.analytical_confidence + 0.05
                )
            
            results.append({
                "evidence": evidence,
                "corroborating_count": len(corroborating),
                "contradictory_count": len(contradictory),
                "corroboration_score": corroboration_score,
                "overall_confidence": evidence.confidence.overall,
                "evidence_rating": evidence.confidence.evidence_rating
            })
        
        return results
    
    def _generate_hash(self, data: Dict[str, Any]) -> str:
        """Generate a SHA-256 hash of the evidence"""
        content = json.dumps(data, sort_keys=True, default=str)
        return f"sha256:{hashlib.sha256(content.encode()).hexdigest()}"
    
    def _determine_evidence_type(self, signal: Dict[str, Any]) -> str:
        """Determine the type of evidence based on the signal"""
        source = signal.get("source", "").lower()
        content = signal.get("content", {})
        
        if "message" in content:
            return "message"
        elif "image" in content or "screenshot" in content:
            return "screenshot"
        elif "document" in content:
            return "document"
        elif "location" in content:
            return "geolocation"
        elif "transaction" in content:
            return "transaction"
        else:
            return "observation"
    
    def _find_corroborating_evidence(
        self,
        evidence: MDPISSEvidence,
        evidence_list: List[MDPISSEvidence]
    ) -> List[MDPISSEvidence]:
        """Find evidence that corroborates this evidence"""
        corroborating = []
        
        # Extract key identifiers from the evidence
        keywords = set()
        if evidence.content:
            for value in evidence.content.values():
                if isinstance(value, str):
                    keywords.update(value.lower().split())
        
        for other in evidence_list:
            if other.evidence_id == evidence.evidence_id:
                continue
            
            if other.content:
                for value in other.content.values():
                    if isinstance(value, str):
                        other_keywords = set(value.lower().split())
                        if len(keywords.intersection(other_keywords)) >= 2:
                            corroborating.append(other)
                            break
        
        return corroborating
    
    def _find_contradictory_evidence(
        self,
        evidence: MDPISSEvidence,
        evidence_list: List[MDPISSEvidence]
    ) -> List[MDPISSEvidence]:
        """Find evidence that contradicts this evidence"""
        contradictory = []
        negations = ["not", "no", "never", "unable", "cannot", "deny", "false"]
        
        if evidence.content and "statement" in evidence.content:
            statement = evidence.content["statement"].lower()
            
            for other in evidence_list:
                if other.evidence_id == evidence.evidence_id:
                    continue
                
                if other.content and "statement" in other.content:
                    other_statement = other.content["statement"].lower()
                    if any(neg in other_statement for neg in negations):
                        # Check if it's the same topic but negated
                        topic_words = [w for w in statement.split() if len(w) > 3]
                        for word in topic_words:
                            if word in other_statement:
                                contradictory.append(other)
                                break
        
        return contradictory
    
    def _calculate_corroboration_score(
        self,
        evidence: MDPISSEvidence,
        corroborating: List[MDPISSEvidence],
        contradictory: List[MDPISSEvidence]
    ) -> float:
        """Calculate a corroboration score between 0 and 1"""
        total = len(corroborating) + len(contradictory) + 1
        
        if total == 0:
            return 0.5
        
        # Weighted scoring
        corroboration_weight = 0.8
        contradiction_weight = 0.2
        
        score = (len(corroborating) * corroboration_weight) - (len(contradictory) * contradiction_weight)
        score = (score + 1) / 2  # Normalize to 0-1
        
        # Apply source reliability factor
        score = score * evidence.confidence.source_reliability
        
        return round(min(1.0, max(0.0, score)), 3)


def create_evidence_from_signal(
    signal: Dict[str, Any],
    source_reliability: float = 0.7,
    extraction_confidence: float = 0.8
) -> MDPISSEvidence:
    """Factory function to create evidence from a signal"""
    assessor = EvidenceAssessor()
    return assessor.assess_evidence(signal, source_reliability, extraction_confidence)