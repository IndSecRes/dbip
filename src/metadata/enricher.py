"""
Metadata Enricher
Adds rich metadata to intelligence assets
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

from src.metadata.classifiers import DomainClassifier, CategoryClassifier, TagGenerator
from src.metadata.extractor import ContextExtractor, EntityExtractor
from src.models.mdips import MDIPSIntelligenceProduct, ConfidenceModel


@dataclass
class EnrichedMetadata:
    """Rich metadata for intelligence assets"""
    classification: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    entities: Dict[str, Any] = field(default_factory=dict)
    enrichments: Dict[str, Any] = field(default_factory=dict)
    quality: Dict[str, Any] = field(default_factory=dict)
    extracted_at: str = field(default_factory=lambda: datetime.now().isoformat())


class MetadataEnricher:
    """
    Enriches intelligence assets with rich metadata
    """
    
    def __init__(self):
        self.domain_classifier = DomainClassifier()
        self.category_classifier = CategoryClassifier()
        self.tag_generator = TagGenerator(max_tags=10)
        self.context_extractor = ContextExtractor()
        self.entity_extractor = EntityExtractor()
    
    def enrich_asset(self, asset: MDIPSIntelligenceProduct) -> MDIPSIntelligenceProduct:
        """Enrich an intelligence asset with metadata"""
        
        # Extract text from content
        content_text = self._extract_text(asset.content)
        
        # Classification
        classification = self._classify_content(asset.content)
        
        # Context extraction
        context = self._extract_context(asset.content)
        
        # Entity extraction
        entities = self._extract_entities(content_text)
        
        # Generate enriched metadata
        metadata = EnrichedMetadata(
            classification=classification,
            context=context,
            entities=entities,
            enrichments={
                "word_count": len(content_text.split()),
                "char_count": len(content_text),
                "has_entities": len(entities.get("names", [])) > 0,
                "has_locations": len(context.get("geographic", {}).get("detected_locations", [])) > 0
            },
            quality={
                "metadata_completeness": self._calculate_completeness(classification, context, entities)
            }
        )
        
        # Update asset with enriched metadata
        if not hasattr(asset, "metadata"):
            asset.metadata = {}
        
        asset.metadata.update({
            "enriched": {
                "classification": metadata.classification,
                "context": metadata.context,
                "entities": metadata.entities,
                "enrichments": metadata.enrichments,
                "quality": metadata.quality,
                "extracted_at": metadata.extracted_at
            }
        })
        
        return asset
    
    def enrich_dictionary(self, asset: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich a dictionary-based asset"""
        
        # Extract text from content
        content = asset.get("content", {})
        content_text = self._extract_text(content)
        
        # Classification
        classification = self._classify_content(content)
        
        # Context extraction
        context = self._extract_context(content)
        
        # Entity extraction
        entities = self._extract_entities(content_text)
        
        # Build enriched metadata
        asset["metadata"] = {
            "classification": classification,
            "context": context,
            "entities": entities,
            "enrichments": {
                "word_count": len(content_text.split()),
                "char_count": len(content_text),
                "has_entities": len(entities.get("names", [])) > 0,
                "has_locations": len(context.get("geographic", {}).get("detected_locations", [])) > 0
            },
            "quality": {
                "metadata_completeness": self._calculate_completeness(classification, context, entities)
            },
            "extracted_at": datetime.now().isoformat()
        }
        
        return asset
    
    def _classify_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Classify content by domain, category, and tags"""
        return {
            "domains": self.domain_classifier.classify(content),
            "categories": self.category_classifier.classify(content),
            "tags": self.tag_generator.classify(content)
        }
    
    def _extract_context(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract contextual information"""
        return {
            "temporal": self.context_extractor.extract_temporal(content),
            "geographic": self.context_extractor.extract_geographic(content),
            "sentiment": self.context_extractor.extract_sentiment(content)
        }
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text"""
        return {
            "names": self.entity_extractor.extract_person_names(text),
            "organizations": self.entity_extractor.extract_organizations(text),
            "technologies": self.entity_extractor.extract_technologies(text),
            "total_count": len(self.entity_extractor.extract_person_names(text)) + 
                          len(self.entity_extractor.extract_organizations(text)) +
                          len(self.entity_extractor.extract_technologies(text))
        }
    
    def _extract_text(self, content: Dict[str, Any]) -> str:
        """Extract text from content dict"""
        text = ""
        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, str):
                    text += f" {value}"
                elif isinstance(value, dict):
                    text += f" {self._extract_text(value)}"
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            text += f" {item}"
                        elif isinstance(item, dict):
                            text += f" {self._extract_text(item)}"
        return text.strip()
    
    def _calculate_completeness(self, classification: Dict, context: Dict, entities: Dict) -> float:
        """Calculate metadata completeness score"""
        score = 0.0
        total = 4.0  # Number of categories checked
        
        # Check classification
        if classification.get("domains"):
            score += 1.0
        if classification.get("categories"):
            score += 1.0
        if classification.get("tags"):
            score += 1.0
        
        # Check entities
        if entities.get("total_count", 0) > 0:
            score += 1.0
        
        return round(score / total, 3) if total > 0 else 0.0


def enrich_asset(asset: Dict[str, Any]) -> Dict[str, Any]:
    """Factory function to enrich an asset"""
    enricher = MetadataEnricher()
    return enricher.enrich_dictionary(asset)