"""
Pattern Discovery
Discovers patterns in data for evolution
"""

from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import uuid
import re


@dataclass
class EntityPattern:
    """Pattern discovered in entities"""
    entity_type: str
    name: str
    pattern_id: str = field(default_factory=lambda: f"EPT_{uuid.uuid4().hex[:8].upper()}")
    attributes: Dict[str, Any] = field(default_factory=dict)
    occurrences: int = 0
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    confidence: float = 0.0
    sources: List[str] = field(default_factory=list)


@dataclass
class TemporalPattern:
    """Temporal pattern discovered"""
    pattern_type: str
    description: str
    pattern_id: str = field(default_factory=lambda: f"TMP_{uuid.uuid4().hex[:8].upper()}")
    frequency: int = 0
    first_occurrence: datetime = field(default_factory=datetime.now)
    last_occurrence: datetime = field(default_factory=datetime.now)
    confidence: float = 0.0
    entity_ids: List[str] = field(default_factory=list)


@dataclass
class CategoryPattern:
    """Category pattern discovered"""
    category: str
    pattern_id: str = field(default_factory=lambda: f"CAP_{uuid.uuid4().hex[:8].upper()}")
    subcategories: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    occurrence_count: int = 0
    confidence: float = 0.0
    parent_categories: List[str] = field(default_factory=list)


class PatternDiscovery:
    """
    Discovers patterns in data
    """
    
    def __init__(self):
        self.entity_patterns: List[EntityPattern] = []
        self.temporal_patterns: List[TemporalPattern] = []
        self.category_patterns: List[CategoryPattern] = []
    
    def discover_entity_patterns(self, entities: List[Dict[str, Any]]) -> List[EntityPattern]:
        """Discover patterns in entities"""
        # Group by type and name
        entity_groups = defaultdict(list)
        for entity in entities:
            key = (entity.get("type", "unknown"), entity.get("name", "unknown"))
            entity_groups[key].append(entity)
        
        patterns = []
        for (entity_type, name), occurrences in entity_groups.items():
            if len(occurrences) >= 2:
                # Calculate confidence based on occurrence count
                confidence = min(0.9, 0.4 + (len(occurrences) * 0.05))
                
                # Extract common attributes
                common_attrs = {}
                for occ in occurrences:
                    for key, value in occ.items():
                        if key not in ["type", "name"]:
                            if key not in common_attrs:
                                common_attrs[key] = value
                
                patterns.append(EntityPattern(
                    entity_type=entity_type,
                    name=name,
                    attributes=common_attrs,
                    occurrences=len(occurrences),
                    confidence=confidence,
                    sources=list(set(e.get("source", "unknown") for e in occurrences))
                ))
        
        self.entity_patterns = patterns
        return patterns
    
    def discover_temporal_patterns(self, timestamps: List[datetime]) -> List[TemporalPattern]:
        """Discover temporal patterns"""
        if not timestamps:
            return []
        
        patterns = []
        
        # Analyze frequency
        timestamps.sort()
        
        # Daily pattern
        daily_counts = defaultdict(int)
        for ts in timestamps:
            daily_counts[ts.date()] += 1
        
        avg_daily = sum(daily_counts.values()) / len(daily_counts) if daily_counts else 0
        
        if avg_daily > 2:
            patterns.append(TemporalPattern(
                pattern_type="daily",
                description=f"Daily pattern detected with average of {avg_daily:.1f} events/day",
                frequency=int(avg_daily),
                first_occurrence=timestamps[0],
                last_occurrence=timestamps[-1],
                confidence=min(0.9, 0.5 + (len(timestamps) * 0.01))
            ))
        
        # Weekly pattern
        weekly_counts = defaultdict(int)
        for ts in timestamps:
            week = ts.isocalendar()[1]
            weekly_counts[week] += 1
        
        avg_weekly = sum(weekly_counts.values()) / len(weekly_counts) if weekly_counts else 0
        
        if avg_weekly > 5:
            patterns.append(TemporalPattern(
                pattern_type="weekly",
                description=f"Weekly pattern detected with average of {avg_weekly:.1f} events/week",
                frequency=int(avg_weekly),
                first_occurrence=timestamps[0],
                last_occurrence=timestamps[-1],
                confidence=min(0.9, 0.5 + (len(timestamps) * 0.01))
            ))
        
        self.temporal_patterns = patterns
        return patterns
    
    def discover_category_patterns(self, categories: List[Dict[str, Any]]) -> List[CategoryPattern]:
        """Discover patterns in categories"""
        # Group by category
        category_groups = defaultdict(list)
        for cat in categories:
            cat_name = cat.get("name", "unknown")
            category_groups[cat_name].append(cat)
        
        patterns = []
        for cat_name, occurrences in category_groups.items():
            if len(occurrences) >= 3:
                # Extract common keywords
                keywords = []
                for occ in occurrences:
                    if "keywords" in occ:
                        keywords.extend(occ["keywords"])
                
                # Find subcategories
                subcats = list(set(occ.get("subcategory", "") for occ in occurrences if occ.get("subcategory")))
                
                confidence = min(0.9, 0.3 + (len(occurrences) * 0.05))
                
                patterns.append(CategoryPattern(
                    category=cat_name,
                    subcategories=subcats,
                    keywords=list(set(keywords))[:10],
                    occurrence_count=len(occurrences),
                    confidence=confidence
                ))
        
        self.category_patterns = patterns
        return patterns
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of discovered patterns"""
        return {
            "total_entity_patterns": len(self.entity_patterns),
            "total_temporal_patterns": len(self.temporal_patterns),
            "total_category_patterns": len(self.category_patterns),
            "entity_patterns": [
                {
                    "type": p.entity_type,
                    "name": p.name,
                    "occurrences": p.occurrences,
                    "confidence": p.confidence
                }
                for p in self.entity_patterns[:10]
            ],
            "temporal_patterns": [
                {
                    "type": p.pattern_type,
                    "description": p.description,
                    "frequency": p.frequency,
                    "confidence": p.confidence
                }
                for p in self.temporal_patterns[:10]
            ],
            "category_patterns": [
                {
                    "category": p.category,
                    "subcategories": p.subcategories,
                    "occurrence_count": p.occurrence_count,
                    "confidence": p.confidence
                }
                for p in self.category_patterns[:10]
            ]
        }