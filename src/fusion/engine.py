"""
Signal Fusion Engine
Correlates weak signals into strong intelligence
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict

from src.fusion.patterns import PatternDetector
from src.models.mdips import ConfidenceModel, EvidenceRating


@dataclass
class FusedSignal:
    """Represents a fused signal from multiple sources"""
    signal_type: str  # Moved BEFORE fields with defaults
    content: Dict[str, Any]  # Moved BEFORE fields with defaults
    fused_id: str = field(default_factory=lambda: f"FUS_{uuid.uuid4().hex[:8].upper()}")
    sources: List[str] = field(default_factory=list)
    source_count: int = 0
    confidence: ConfidenceModel = field(default_factory=ConfidenceModel)
    evidence_rating: EvidenceRating = field(default_factory=lambda: EvidenceRating.C)
    patterns: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    provenance: List[Dict[str, Any]] = field(default_factory=list)


class SignalFusionEngine:
    """
    Fuses multiple weak signals into strong intelligence
    """
    
    def __init__(self, confidence_threshold: float = 0.6):
        self.confidence_threshold = confidence_threshold
        self.pattern_detector = PatternDetector()
        self.fused_signals: List[FusedSignal] = []
    
    def fuse_signals(self, signals: List[Dict[str, Any]]) -> List[FusedSignal]:
        """
        Fuse multiple signals into a single intelligence signal
        
        Args:
            signals: List of raw signals with extracted entities
            
        Returns:
            List of fused signals
        """
        if not signals:
            return []
        
        # Phase 1: Detect patterns
        patterns = self.pattern_detector.detect_all_patterns(signals)
        
        # Phase 2: Correlate signals
        correlations = self._correlate_signals(signals, patterns)
        
        # Phase 3: Build fused signals
        fused_signals = self._build_fused_signals(correlations, patterns)
        
        self.fused_signals = fused_signals
        return fused_signals
    
    def _correlate_signals(
        self,
        signals: List[Dict[str, Any]],
        patterns: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Correlate signals based on patterns
        """
        correlations = []
        
        # Group by entity patterns
        entity_patterns = patterns.get("entity_patterns", [])
        for pattern in entity_patterns:
            if pattern.confidence >= self.confidence_threshold:
                # Find signals matching this pattern
                matching_signals = []
                for signal in signals:
                    entities = signal.get("extracted_entities", [])
                    for entity in entities:
                        if entity.get("name") == pattern.entity_name:
                            matching_signals.append(signal)
                            break
                
                if len(matching_signals) >= 2:
                    correlations.append({
                        "type": "entity",
                        "pattern": pattern,
                        "signals": matching_signals,
                        "confidence": pattern.confidence
                    })
        
        # Group by temporal patterns
        temporal_patterns = patterns.get("temporal_patterns", [])
        for pattern in temporal_patterns:
            if pattern.confidence >= self.confidence_threshold:
                # Find signals matching this pattern
                matching_signals = []
                for signal in signals:
                    timestamp = signal.get("timestamp")
                    if timestamp and pattern.start_time - timedelta(hours=12) <= timestamp <= pattern.end_time + timedelta(hours=12):
                        matching_signals.append(signal)
                
                if len(matching_signals) >= 2:
                    correlations.append({
                        "type": "temporal",
                        "pattern": pattern,
                        "signals": matching_signals,
                        "confidence": pattern.confidence
                    })
        
        # Group by geographic patterns
        geographic_patterns = patterns.get("geographic_patterns", [])
        for pattern in geographic_patterns:
            if pattern.confidence >= self.confidence_threshold:
                matching_signals = []
                for signal in signals:
                    content = signal.get("content", {})
                    message = content.get("message", "") or content.get("text", "")
                    if pattern.location in message.lower():
                        matching_signals.append(signal)
                
                if len(matching_signals) >= 2:
                    correlations.append({
                        "type": "geographic",
                        "pattern": pattern,
                        "signals": matching_signals,
                        "confidence": pattern.confidence
                    })
        
        return correlations
    
    def _build_fused_signals(
        self,
        correlations: List[Dict[str, Any]],
        patterns: Dict[str, Any]
    ) -> List[FusedSignal]:
        """
        Build fused signals from correlations
        """
        fused_signals = []
        
        for correlation in correlations:
            # Calculate overall confidence
            base_confidence = correlation["confidence"]
            signal_count = len(correlation["signals"])
            
            # Boost confidence with more sources
            source_boost = min(0.2, signal_count * 0.05)
            
            # Boost with pattern corroboration
            pattern_boost = 0.1
            
            overall_confidence = min(0.95, base_confidence + source_boost + pattern_boost)
            
            # Create confidence model
            confidence = ConfidenceModel(
                source_reliability=min(1.0, overall_confidence + 0.05),
                extraction_confidence=min(1.0, overall_confidence),
                identity_confidence=min(1.0, overall_confidence + 0.02),
                relationship_confidence=min(1.0, overall_confidence - 0.05),
                temporal_confidence=min(1.0, overall_confidence + 0.03),
                analytical_confidence=min(1.0, overall_confidence)
            )
            
            # Build content from correlated signals
            content = {
                "correlation_type": correlation["type"],
                "message_count": len(correlation["signals"]),
                "sources": list(set(s.get("source", "") for s in correlation["signals"])),
                "entities": []
            }
            
            # Extract entities from signals
            entities_set = set()
            for signal in correlation["signals"]:
                entities = signal.get("extracted_entities", [])
                for entity in entities:
                    entities_set.add(entity.get("name", ""))
                    if "content" not in content:
                        content["content"] = {}
                    content["content"][entity.get("type", "entity")] = entity.get("name", "")
            
            # Detect topic from keyword clusters
            topic = None
            for cluster in patterns.get("keyword_clusters", []):
                if cluster.confidence >= self.confidence_threshold:
                    for signal in correlation["signals"]:
                        if any(kw in str(signal.get("content", {})).lower() for kw in cluster.keywords):
                            topic = cluster.keywords[0]
                            break
                    if topic:
                        break
            
            # Create fused signal
            fused = FusedSignal(
                signal_type="correlated",
                content=content,
                sources=list(set(s.get("source", "") for s in correlation["signals"])),
                source_count=len(correlation["signals"]),
                confidence=confidence,
                evidence_rating=confidence.evidence_rating,
                patterns=[correlation["type"]],
                entities=list(entities_set),
                timestamp=datetime.now(),
                provenance=[
                    {
                        "source": s.get("source", "unknown"),
                        "timestamp": s.get("timestamp"),
                        "original_data": s.get("original_data", {})
                    }
                    for s in correlation["signals"][:3]  # Limit provenance
                ]
            )
            
            fused_signals.append(fused)
        
        # Sort by confidence descending
        fused_signals.sort(key=lambda x: x.confidence.overall, reverse=True)
        
        return fused_signals
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of fused signals"""
        return {
            "total_fused_signals": len(self.fused_signals),
            "average_confidence": round(sum(
                s.confidence.overall for s in self.fused_signals
            ) / len(self.fused_signals) if self.fused_signals else 0, 3),
            "ratings_distribution": {
                "A": len([s for s in self.fused_signals if s.confidence.evidence_rating == EvidenceRating.A]),
                "B": len([s for s in self.fused_signals if s.confidence.evidence_rating == EvidenceRating.B]),
                "C": len([s for s in self.fused_signals if s.confidence.evidence_rating == EvidenceRating.C]),
                "D": len([s for s in self.fused_signals if s.confidence.evidence_rating == EvidenceRating.D])
            },
            "top_sources": self._get_top_sources(),
            "top_entities": self._get_top_entities()
        }
    
    def _get_top_sources(self) -> List[Dict[str, Any]]:
        """Get top sources from fused signals"""
        source_counts = defaultdict(int)
        for fused in self.fused_signals:
            for source in fused.sources:
                source_counts[source] += 1
        
        return [
            {"source": source, "count": count}
            for source, count in sorted(
                source_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        ]
    
    def _get_top_entities(self) -> List[Dict[str, Any]]:
        """Get top entities from fused signals"""
        entity_counts = defaultdict(int)
        for fused in self.fused_signals:
            for entity in fused.entities:
                entity_counts[entity] += 1
        
        return [
            {"entity": entity, "count": count}
            for entity, count in sorted(
                entity_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        ]


def fuse_signals(signals: List[Dict[str, Any]]) -> List[FusedSignal]:
    """Factory function to fuse signals"""
    engine = SignalFusionEngine()
    return engine.fuse_signals(signals) 