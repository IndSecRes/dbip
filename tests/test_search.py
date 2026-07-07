"""
Tests for Search Intelligence
"""

import pytest
from src.search import SearchEngine, SearchIndexer, DocumentIndex


def test_document_index_creation():
    """Test document index creation"""
    doc = DocumentIndex(
        doc_id="test_001",
        title="Test Document",
        content="This is test content",
        metadata={"domain": "OSINT"}
    )
    
    assert doc.doc_id == "test_001"
    assert doc.title == "Test Document"
    assert doc.content == "This is test content"


def test_search_indexer():
    """Test search indexer"""
    indexer = SearchIndexer()
    
    asset = {
        "asset_id": "AST_001",
        "title": "John Doe Profile",
        "content": {"name": "John Doe", "email": "john.doe@email.com"}
    }
    
    doc = indexer.index_asset(asset)
    
    assert doc.doc_id == "AST_001"
    assert "john" in doc.content.lower()
    assert doc.metadata is not None


def test_keyword_search():
    """Test keyword search"""
    indexer = SearchIndexer()
    
    assets = [
        {"asset_id": "001", "title": "John Doe", "content": {"info": "John works at ACME"}},
        {"asset_id": "002", "title": "Jane Smith", "content": {"info": "Jane works at Google"}}
    ]
    
    indexer.index_assets(assets)
    results = indexer.search_keyword("John")
    
    assert len(results) >= 1
    assert "John" in results[0]["content"] or "John" in results[0]["title"]


def test_search_engine():
    """Test search engine"""
    engine = SearchEngine()
    
    assets = [
        {"asset_id": "001", "title": "Test Asset", "content": {"info": "Test content"}}
    ]
    
    engine.index_assets(assets)
    results = engine.search("Test")
    
    assert "results" in results
    assert len(results["results"]) >= 1


def test_search_filters():
    """Test search filters"""
    engine = SearchEngine()
    
    assets = [
        {
            "asset_id": "001",
            "title": "Cyber Threat",
            "content": {"info": "Malware detected"},
            "metadata": {"classification": {"domains": ["cybint"]}}
        },
        {
            "asset_id": "002",
            "title": "Financial Report",
            "content": {"info": "Quarterly earnings"},
            "metadata": {"classification": {"domains": ["finint"]}}
        }
    ]
    
    engine.index_assets(assets)
    results = engine.search("threat", filters={"domains": ["cybint"]})
    
    assert len(results["results"]) >= 1


def test_search_query_classification():
    """Test query classification"""
    from src.search.router import SearchRouter
    router = SearchRouter()
    
    keyword_query = "find John Doe"
    entity_query = "Who is John Doe"
    relationship_query = "relationship between John and ACME"
    
    assert router._classify_query(keyword_query) == "keyword"
    assert router._classify_query(entity_query) == "entity"
    assert router._classify_query(relationship_query) == "relationship"