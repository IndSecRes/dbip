"""
Tests for Knowledge Graph Integration
"""

import pytest
from src.graph import Neo4jClient, KnowledgeGraphRepository, GraphNode, GraphRelationship
from src.models.mdips import MDIPSEntity, EntityType, RelationshipType, ConfidenceModel


@pytest.mark.asyncio
async def test_graph_connection():
    """Test Neo4j connection"""
    client = Neo4jClient()
    # Skip if Neo4j not running
    if not client.connect():
        pytest.skip("Neo4j not available")
    
    assert client.is_connected()
    client.disconnect()


@pytest.mark.asyncio
async def test_create_node():
    """Test creating a node"""
    client = Neo4jClient()
    if not client.connect():
        pytest.skip("Neo4j not available")
    
    repo = KnowledgeGraphRepository()
    node = GraphNode(
        label="PERSON",
        properties={"name": "Test Person", "id": "test_001"}
    )
    
    node_id = await repo.create_node(node)
    assert node_id is not None
    
    # Clean up
    await client.run_query("MATCH (n {id: $id}) DETACH DELETE n", {"id": node_id})
    client.disconnect()


@pytest.mark.asyncio
async def test_create_relationship():
    """Test creating a relationship"""
    client = Neo4jClient()
    if not client.connect():
        pytest.skip("Neo4j not available")
    
    repo = KnowledgeGraphRepository()
    
    # Create two nodes
    node1 = GraphNode(label="PERSON", properties={"name": "John"})
    node2 = GraphNode(label="COMPANY", properties={"name": "ACME"})
    
    id1 = await repo.create_node(node1)
    id2 = await repo.create_node(node2)
    
    # Create relationship
    rel = GraphRelationship(
        source_id=id1,
        target_id=id2,
        rel_type="WORKS_AT",
        properties={"role": "Developer", "since": 2024}
    )
    
    result = await repo.create_relationship(rel)
    assert result is True
    
    # Clean up
    await client.run_query("MATCH (n) DETACH DELETE n")
    client.disconnect()


@pytest.mark.asyncio
async def test_get_related_entities():
    """Test getting related entities"""
    client = Neo4jClient()
    if not client.connect():
        pytest.skip("Neo4j not available")
    
    repo = KnowledgeGraphRepository()
    
    # Create nodes and relationships
    await client.run_query("""
        CREATE (a:PERSON {id: 'p1', name: 'John'})
        CREATE (b:PERSON {id: 'p2', name: 'Jane'})
        CREATE (c:COMPANY {id: 'c1', name: 'ACME'})
        CREATE (a)-[:WORKS_AT {role: 'Dev'}]->(c)
        CREATE (b)-[:WORKS_AT {role: 'Manager'}]->(c)
        CREATE (a)-[:FRIEND_OF]->(b)
    """)
    
    related = await repo.get_related_entities("p1", max_depth=2)
    
    assert len(related) >= 2
    
    # Clean up
    await client.run_query("MATCH (n) DETACH DELETE n")
    client.disconnect()