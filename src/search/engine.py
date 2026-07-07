"""
Search Engine
Main search interface combining all search methods
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from src.search.indexer import SearchIndexer
from src.search.router import SearchRouter


@dataclass
class SearchQuery:
    """Search query object"""
    text: str
    query_type: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    limit: int = 20


@dataclass
class SearchResult:
    """Search result object"""
    id: str
    title: str
    content: str
    score: float
    metadata: Dict[str, Any]
    source: str = "dbip"
    timestamp: str = ""


class SearchEngine:
    """
    Main Search Engine
    Provides unified search interface
    """
    
    def __init__(self):
        self.indexer = SearchIndexer()
        self.router = SearchRouter()
        self.indexed_assets: List[Dict[str, Any]] = []
    
    def index_assets(self, assets: List[Dict[str, Any]]) -> int:
        """Index assets for search"""
        docs = self.indexer.index_assets(assets)
        self.indexed_assets = assets
        return len(docs)
    
    def search(self, query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search indexed assets
        
        Args:
            query: Search query text
            filters: Optional filters (domain, category, tags, etc.)
            
        Returns:
            Search results with metadata
        """
        
        # If no assets indexed, return empty
        if not self.indexed_assets:
            return {
                "query": query,
                "results": [],
                "total_results": 0,
                "message": "No assets indexed. Use index_assets() first."
            }
        
        # Perform search using router
        results = self.router.search(query, self.indexed_assets)
        
        # Apply filters if provided
        if filters:
            filtered = self._apply_filters(results.get("results", []), filters)
            results["results"] = filtered
            results["total_results"] = len(filtered)
            results["filters_applied"] = filters
        
        return results
    
    def search_semantic(self, query: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Semantic search using embeddings
        
        Note: This is a placeholder for future embedding-based search
        """
        # Placeholder: use keyword search as fallback
        results = self.indexer.search_keyword(query)
        return results[:top_n]
    
    def search_graph(self, query: str) -> List[Dict[str, Any]]:
        """
        Graph-based search using Neo4j
        
        Note: This is a placeholder for future graph search
        """
        # Placeholder: return empty for now
        return []
    
    def _apply_filters(self, results: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply filters to search results"""
        filtered = []
        
        for result in results:
            metadata = result.get("metadata", {})
            classification = metadata.get("classification", {})
            entities = metadata.get("entities", {})
            context = metadata.get("context", {})
            
            # Domain filter
            if "domains" in filters:
                domains = classification.get("domains", [])
                if not any(d in domains for d in filters["domains"]):
                    continue
            
            # Category filter
            if "categories" in filters:
                categories = classification.get("categories", [])
                if not any(c in categories for c in filters["categories"]):
                    continue
            
            # Tag filter
            if "tags" in filters:
                tags = classification.get("tags", [])
                if not any(t in tags for t in filters["tags"]):
                    continue
            
            # Entity filter
            if "entities" in filters:
                entity_names = entities.get("names", [])
                if not any(e in entity_names for e in filters["entities"]):
                    continue
            
            filtered.append(result)
        
        return filtered
    
    def get_stats(self) -> Dict[str, Any]:
        """Get search engine statistics"""
        return {
            "indexed_assets": len(self.indexed_assets),
            "index_stats": self.indexer.get_index_stats()
        }