"""
Search Router
Routes queries to appropriate search methods
"""

from typing import Dict, Any, List, Optional
import re

from src.graph import KnowledgeGraphRepository, get_neo4j_client
from src.search.indexer import SearchIndexer, DocumentIndex


class SearchRouter:
    """
    Routes search queries to the appropriate search method
    """
    
    def __init__(self):
        self.indexer = SearchIndexer()
        self.graph_repo = KnowledgeGraphRepository()
    
    def search(self, query: str, assets: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Search intelligence assets
        
        Args:
            query: Search query
            assets: List of assets to search (optional)
            
        Returns:
            Search results with type classification
        """
        
        # Determine query type
        query_type = self._classify_query(query)
        
        # Index assets if provided
        if assets:
            self.indexer.index_assets(assets)
        
        # Perform search based on type
        results = []
        context = {}
        
        if query_type == "keyword":
            results = self._keyword_search(query)
            context["search_type"] = "keyword"
        elif query_type == "entity":
            results = self._entity_search(query)
            context["search_type"] = "entity"
        elif query_type == "relationship":
            results = self._relationship_search(query)
            context["search_type"] = "relationship"
        else:
            results = self._keyword_search(query)
            context["search_type"] = "hybrid"
        
        return {
            "query": query,
            "query_type": query_type,
            "results": results[:20],
            "total_results": len(results),
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
    
    def _classify_query(self, query: str) -> str:
        """Classify query type"""
        query_lower = query.lower()
        
        # Entity search: mentions of specific entities
        entity_patterns = [
            r'\b(?:person|individual|who is)\b',
            r'\b(?:company|organization)\b',
            r'\b(?:acme|google|microsoft|apple)\b'
        ]
        
        # Relationship search: asks about connections
        relationship_patterns = [
            r'\b(?:relationship|connected|linked|related)\b',
            r'\b(?:works at|belongs to|owns|controls)\b'
        ]
        
        for pattern in relationship_patterns:
            if re.search(pattern, query_lower):
                return "relationship"
        
        for pattern in entity_patterns:
            if re.search(pattern, query_lower):
                return "entity"
        
        return "keyword"
    
    def _keyword_search(self, query: str) -> List[Dict[str, Any]]:
        """Perform keyword search"""
        return self.indexer.search_keyword(query)
    
    def _entity_search(self, query: str) -> List[Dict[str, Any]]:
        """Perform entity search"""
        # Extract entity name from query
        entity_name = self._extract_entity_name(query)
        
        results = []
        
        # Search in index
        if entity_name:
            # Get all indexed documents
            for doc_id, doc in self.indexer.index.items():
                if entity_name.lower() in doc.content.lower() or entity_name.lower() in doc.title.lower():
                    result = doc.to_dict()
                    result["relevance_score"] = 0.9
                    results.append(result)
        
        # Also search in graph
        try:
            graph_results = self._search_graph_entity(entity_name)
            results.extend(graph_results)
        except:
            pass
        
        return results
    
    def _relationship_search(self, query: str) -> List[Dict[str, Any]]:
        """Perform relationship search"""
        # Extract entities from query
        entities = self._extract_entities_from_query(query)
        
        results = []
        
        # Search in graph
        if len(entities) >= 2:
            try:
                graph_results = self._search_graph_relationship(entities[0], entities[1])
                results.extend(graph_results)
            except:
                pass
        
        return results
    
    def _extract_entity_name(self, query: str) -> str:
        """Extract entity name from query"""
        # Simple extraction: look for capitalized words or quoted phrases
        # Remove common prefixes
        prefixes = ["who is", "what is", "about", "find", "search", "entity"]
        clean_query = query.lower()
        for prefix in prefixes:
            if clean_query.startswith(prefix):
                clean_query = clean_query[len(prefix):].strip()
        
        return clean_query
    
    def _extract_entities_from_query(self, query: str) -> List[str]:
        """Extract multiple entities from query"""
        # Look for patterns like "X and Y" or "X to Y"
        import re
        
        # Split by common separators
        separators = [" and ", " to ", " between ", " from ", " with "]
        entities = []
        for sep in separators:
            if sep in query:
                parts = query.split(sep)
                entities = [p.strip() for p in parts[:2]]
                break
        
        if not entities:
            # Try to find capitalized words
            words = re.findall(r'\b[A-Z][a-z]+\b', query)
            entities = words[:2]
        
        return entities
    
    def _search_graph_entity(self, entity_name: str) -> List[Dict[str, Any]]:
        """Search for entity in graph"""
        # This would query Neo4j
        # For now, return empty list
        return []
    
    def _search_graph_relationship(self, entity1: str, entity2: str) -> List[Dict[str, Any]]:
        """Search for relationship in graph"""
        # This would query Neo4j
        # For now, return empty list
        return []


from datetime import datetime