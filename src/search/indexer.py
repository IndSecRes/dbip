"""
Search Indexer
Indexes intelligence assets for search
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict

from src.metadata.enricher import MetadataEnricher


class DocumentIndex:
    """Represents an indexed document"""
    
    def __init__(
        self,
        doc_id: str,
        title: str,
        content: str,
        metadata: Dict[str, Any],
        source: str = "dbip",
        timestamp: Optional[str] = None
    ):
        self.doc_id = doc_id
        self.title = title
        self.content = content
        self.metadata = metadata
        self.source = source
        self.timestamp = timestamp or datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.doc_id,
            "title": self.title,
            "content": self.content,
            "metadata": self.metadata,
            "source": self.source,
            "timestamp": self.timestamp
        }


class SearchIndexer:
    """
    Indexes assets for search
    """
    
    def __init__(self):
        self.index: Dict[str, DocumentIndex] = {}
        self.inverted_index: Dict[str, List[str]] = defaultdict(list)
        self.metadata_enricher = MetadataEnricher()
    
    def index_asset(self, asset: Dict[str, Any]) -> DocumentIndex:
        """Index a single asset"""
        
        # Extract content
        content = asset.get("content", {})
        title = asset.get("title", "Untitled")
        asset_id = asset.get("asset_id", str(len(self.index) + 1))
        
        # Enrich metadata if not already enriched
        if "metadata" not in asset:
            enriched = self.metadata_enricher.enrich_dictionary(asset)
            metadata = enriched.get("metadata", {})
        else:
            metadata = asset.get("metadata", {})
        
        # Build searchable text
        searchable_text = self._build_searchable_text(content, title, metadata)
        
        # Create document
        doc = DocumentIndex(
            doc_id=asset_id,
            title=title,
            content=searchable_text,
            metadata=metadata,
            timestamp=asset.get("timestamp", datetime.now().isoformat())
        )
        
        # Store in index
        self.index[asset_id] = doc
        
        # Build inverted index
        self._build_inverted_index(asset_id, searchable_text)
        
        return doc
    
    def index_assets(self, assets: List[Dict[str, Any]]) -> List[DocumentIndex]:
        """Index multiple assets"""
        docs = []
        for asset in assets:
            doc = self.index_asset(asset)
            docs.append(doc)
        return docs
    
    def _build_searchable_text(self, content: Dict[str, Any], title: str, metadata: Dict[str, Any]) -> str:
        """Build searchable text from content and metadata"""
        text_parts = [title]
        
        # Extract text from content
        text_parts.append(self._extract_text(content))
        
        # Add metadata
        if metadata:
            classification = metadata.get("classification", {})
            text_parts.append(" ".join(classification.get("domains", [])))
            text_parts.append(" ".join(classification.get("categories", [])))
            text_parts.append(" ".join(classification.get("tags", [])))
            
            context = metadata.get("context", {})
            geographic = context.get("geographic", {})
            text_parts.append(" ".join(geographic.get("detected_locations", [])))
            
            entities = metadata.get("entities", {})
            text_parts.append(" ".join(entities.get("names", [])))
            text_parts.append(" ".join(entities.get("organizations", [])))
            text_parts.append(" ".join(entities.get("technologies", [])))
        
        return " ".join(text_parts)
    
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
        return text
    
    def _build_inverted_index(self, doc_id: str, text: str):
        """Build inverted index for document"""
        # Simple tokenization
        words = text.lower().split()
        for word in words:
            if len(word) > 2:
                self.inverted_index[word].append(doc_id)
    
    def get_document(self, doc_id: str) -> Optional[DocumentIndex]:
        """Get a document by ID"""
        return self.index.get(doc_id)
    
    def search_keyword(self, query: str) -> List[Dict[str, Any]]:
        """Search by keyword using inverted index"""
        words = query.lower().split()
        results = []
        
        # Find documents matching any word
        matched_docs = set()
        for word in words:
            if len(word) > 2 and word in self.inverted_index:
                matched_docs.update(self.inverted_index[word])
        
        # Score documents
        doc_scores = {}
        for doc_id in matched_docs:
            score = self._calculate_relevance(doc_id, query)
            doc_scores[doc_id] = score
        
        # Sort by score
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return results
        for doc_id, score in sorted_docs[:20]:
            doc = self.index.get(doc_id)
            if doc:
                result = doc.to_dict()
                result["relevance_score"] = score
                results.append(result)
        
        return results
    
    def _calculate_relevance(self, doc_id: str, query: str) -> float:
        """Calculate relevance score for a document"""
        doc = self.index.get(doc_id)
        if not doc:
            return 0.0
        
        query_words = set(query.lower().split())
        content_words = set(doc.content.lower().split())
        
        # Jaccard similarity
        if not query_words or not content_words:
            return 0.0
        
        intersection = len(query_words.intersection(content_words))
        union = len(query_words.union(content_words))
        
        return intersection / union if union > 0 else 0.0
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the index"""
        return {
            "total_documents": len(self.index),
            "total_terms": len(self.inverted_index),
            "avg_doc_size": sum(len(doc.content.split()) for doc in self.index.values()) / len(self.index) if self.index else 0
        }