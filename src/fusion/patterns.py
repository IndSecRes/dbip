"""
Signal Fusion - Pattern Detection
Detects patterns across multiple signals
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set, Tuple
from collections import defaultdict, Counter
import uuid
from dataclasses import dataclass, field


@dataclass
class EntityPattern:
    """Pattern detected across entities"""
    entity_type: str
    entity_name: str
    pattern_id: str = field(default_factory=lambda: f"PAT_{uuid.uuid4().hex[:8].upper()}")
    aliases: List[str] = field(default_factory=list)
    source_count: int = 0
    confidence: float = 0.0
    sources: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TemporalPattern:
    """Temporal pattern detected across signals"""
    event_type: str
    description: str
    start_time: datetime
    pattern_id: str = field(default_factory=lambda: f"TMP_{uuid.uuid4().hex[:8].upper()}")
    end_time: Optional[datetime] = None
    entity_ids: List[str] = field(default_factory=list)
    signal_count: int = 0
    confidence: float = 0.0
    sources: List[str] = field(default_factory=list)


@dataclass
class GeographicPattern:
    """Geographic pattern detected across signals"""
    location: str
    pattern_id: str = field(default_factory=lambda: f"GEO_{uuid.uuid4().hex[:8].upper()}")
    coordinates: Optional[Tuple[float, float]] = None
    entity_ids: List[str] = field(default_factory=list)
    signal_count: int = 0
    confidence: float = 0.0
    sources: List[str] = field(default_factory=list)


@dataclass
class KeywordCluster:
    """Cluster of keywords detected across signals"""
    keywords: List[str]
    cluster_id: str = field(default_factory=lambda: f"CLS_{uuid.uuid4().hex[:8].upper()}")
    signals: List[Dict[str, Any]] = field(default_factory=list)
    count: int = 0
    confidence: float = 0.0
    topic: Optional[str] = None


class PatternDetector:
    """
    Detects patterns across multiple signals
    """
    
    def __init__(self):
        self.entity_patterns: List[EntityPattern] = []
        self.temporal_patterns: List[TemporalPattern] = []
        self.geographic_patterns: List[GeographicPattern] = []
        self.keyword_clusters: List[KeywordCluster] = []
    
    def detect_entity_patterns(self, signals: List[Dict[str, Any]]) -> List[EntityPattern]:
        """
        Detect entity patterns across signals
        """
        # Extract entities from signals
        entity_occurrences = defaultdict(list)
        
        for signal in signals:
            entities = signal.get("extracted_entities", [])
            for entity in entities:
                entity_name = entity.get("name", "")
                entity_type = entity.get("type", "unknown")
                if entity_name:
                    entity_occurrences[(entity_type, entity_name)].append({
                        "signal": signal,
                        "entity": entity
                    })
        
        # Create patterns from occurrences
        patterns = []
        for (entity_type, entity_name), occurrences in entity_occurrences.items():
            if len(occurrences) >= 2:
                # Calculate confidence based on occurrence count and source diversity
                source_count = len(set(o["signal"].get("source", "") for o in occurrences))
                confidence = min(0.9, 0.5 + (len(occurrences) * 0.05) + (source_count * 0.05))
                
                patterns.append(EntityPattern(
                    entity_type=entity_type,
                    entity_name=entity_name,
                    aliases=[entity_name],
                    source_count=len(occurrences),
                    confidence=confidence,
                    sources=list(set(o["signal"].get("source", "") for o in occurrences)),
                    attributes=occurrences[0]["entity"].get("attributes", {})
                ))
        
        self.entity_patterns = patterns
        return patterns
    
    def detect_temporal_patterns(self, signals: List[Dict[str, Any]]) -> List[TemporalPattern]:
        """
        Detect temporal patterns across signals
        """
        # Extract temporal information
        events = []
        for signal in signals:
            timestamp = signal.get("timestamp")
            content = signal.get("content", {})
            message = content.get("message", "") or content.get("text", "")
            
            if timestamp and message:
                # Look for time-related keywords
                time_keywords = ["today", "tomorrow", "next week", "soon", "now", "later"]
                if any(kw in message.lower() for kw in time_keywords):
                    events.append({
                        "signal": signal,
                        "timestamp": timestamp,
                        "content": message
                    })
        
        # Group events by time proximity
        patterns = []
        if len(events) >= 2:
            # Sort by timestamp
            events.sort(key=lambda x: x["timestamp"])
            
            # Group events within 24 hours
            current_group = [events[0]]
            for i in range(1, len(events)):
                if events[i]["timestamp"] - events[i-1]["timestamp"] <= timedelta(hours=24):
                    current_group.append(events[i])
                else:
                    if len(current_group) >= 2:
                        patterns.append(self._create_temporal_pattern(current_group))
                    current_group = [events[i]]
            
            if len(current_group) >= 2:
                patterns.append(self._create_temporal_pattern(current_group))
        
        self.temporal_patterns = patterns
        return patterns
    
    def _create_temporal_pattern(self, events: List[Dict]) -> TemporalPattern:
        """Create a temporal pattern from a group of events"""
        confidence = min(0.9, 0.4 + (len(events) * 0.1))
        
        # Determine event type from content
        content = " ".join([e["content"] for e in events])
        event_types = ["meeting", "event", "announcement", "update", "release"]
        detected_type = "event"
        for et in event_types:
            if et in content.lower():
                detected_type = et
                break
        
        return TemporalPattern(
            event_type=detected_type,
            description=content[:100],
            start_time=events[0]["timestamp"],
            end_time=events[-1]["timestamp"],
            signal_count=len(events),
            confidence=confidence,
            sources=list(set(e["signal"].get("source", "") for e in events))
        )
    
    def detect_geographic_patterns(self, signals: List[Dict[str, Any]]) -> List[GeographicPattern]:
        """
        Detect geographic patterns across signals
        """
        # Extract locations from signals
        locations = defaultdict(list)
        
        for signal in signals:
            content = signal.get("content", {})
            message = content.get("message", "") or content.get("text", "")
            
            # Look for location keywords
            location_keywords = ["nyc", "new york", "la", "los angeles", "sf", "san francisco", "london", "paris"]
            for location in location_keywords:
                if location in message.lower():
                    locations[location].append(signal)
        
        patterns = []
        for location, loc_signals in locations.items():
            if len(loc_signals) >= 2:
                patterns.append(GeographicPattern(
                    location=location,
                    signal_count=len(loc_signals),
                    confidence=min(0.9, 0.4 + (len(loc_signals) * 0.1)),
                    sources=list(set(s.get("source", "") for s in loc_signals))
                ))
        
        self.geographic_patterns = patterns
        return patterns
    
    def detect_keyword_clusters(self, signals: List[Dict[str, Any]]) -> List[KeywordCluster]:
        """
        Detect keyword clusters across signals
        """
        # Extract text content
        texts = []
        for signal in signals:
            content = signal.get("content", {})
            message = content.get("message", "") or content.get("text", "")
            if message:
                texts.append({
                    "signal": signal,
                    "text": message
                })
        
        # Count keyword frequencies
        word_counts = Counter()
        for item in texts:
            words = re.findall(r'\b\w+\b', item["text"].lower())
            # Filter common words
            stopwords = {"the", "a", "an", "of", "to", "for", "with", "on", "at", "from", "by", "in", "is", "it", "and", "or", "but"}
            words = [w for w in words if w not in stopwords and len(w) > 2]
            word_counts.update(words)
        
        # Find clusters
        clusters = []
        threshold = 2
        for word, count in word_counts.most_common(20):
            if count >= threshold:
                # Find signals containing this word
                cluster_signals = []
                for item in texts:
                    if word in item["text"].lower():
                        cluster_signals.append(item["signal"])
                
                if cluster_signals:
                    clusters.append(KeywordCluster(
                        keywords=[word],
                        signals=cluster_signals,
                        count=len(cluster_signals),
                        confidence=min(0.9, 0.3 + (count * 0.1))
                    ))
        
        self.keyword_clusters = clusters
        return clusters
    
    def detect_all_patterns(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect all patterns across signals"""
        return {
            "entity_patterns": self.detect_entity_patterns(signals),
            "temporal_patterns": self.detect_temporal_patterns(signals),
            "geographic_patterns": self.detect_geographic_patterns(signals),
            "keyword_clusters": self.detect_keyword_clusters(signals),
            "summary": {
                "total_entity_patterns": len(self.entity_patterns),
                "total_temporal_patterns": len(self.temporal_patterns),
                "total_geographic_patterns": len(self.geographic_patterns),
                "total_keyword_clusters": len(self.keyword_clusters),
                "signals_analyzed": len(signals)
            }
        }   