"""
Knowledge Graph Repository
High-level operations for the knowledge graph
"""

import json
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
import uuid

from src.graph.neo4j_client import get_neo4j_client
from src.models.mdips import MDIPSEntity, MDIPSRelationship


class GraphNode:
    """Represents a node in the knowledge graph"""
    
    def __init__(
        self,
        label: str,
        properties: Dict[str, Any],
        node_id: Optional[str] = None
    ):
        self.id = node_id or f"NODE_{uuid.uuid4().hex[:8].upper()}"
        self.label = label
        self.properties = properties
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for Neo4j"""
        return {
            "id": self.id,
            "label": self.label,
            **self.properties,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class GraphRelationship:
    """Represents a relationship in the knowledge graph"""
    
    def __init__(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        properties: Optional[Dict[str, Any]] = None
    ):
        self.source_id = source_id
        self.target_id = target_id
        self.type = rel_type
        self.properties = properties or {}
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for Neo4j"""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "type": self.type,
            **self.properties,
            "created_at": self.created_at.isoformat()
        }


class KnowledgeGraphRepository:
    """
    High-level operations for the knowledge graph
    """
    
    def __init__(self):
        self.client = get_neo4j_client()
    
    async def create_node(self, node: GraphNode) -> str:
        """Create a node in the graph"""
        query = """
        CREATE (n:`{label}` {{
            id: $id,
            properties: $properties,
            created_at: $created_at,
            updated_at: $updated_at
        }})
        RETURN n.id as node_id
        """.format(label=node.label)
        
        params = {
            "id": node.id,
            "properties": json.dumps(node.properties),
            "created_at": node.created_at.isoformat(),
            "updated_at": node.updated_at.isoformat()
        }
        
        result = await self.client.run_query(query, params)
        return result[0]["node_id"] if result else None
    
    async def create_relationship(self, relationship: GraphRelationship) -> bool:
        """Create a relationship in the graph"""
        query = """
        MATCH (a {{id: $source_id}})
        MATCH (b {{id: $target_id}})
        CREATE (a)-[r:`{rel_type}` {{
            properties: $properties,
            created_at: $created_at
        }}]->(b)
        RETURN count(r) as count
        """.format(rel_type=relationship.type)
        
        params = {
            "source_id": relationship.source_id,
            "target_id": relationship.target_id,
            "properties": json.dumps(relationship.properties),
            "created_at": relationship.created_at.isoformat()
        }
        
        result = await self.client.run_query(query, params)
        return result[0]["count"] > 0 if result else False
    
    async def create_entity_node(self, entity: MDIPSEntity) -> str:
        """Create a node from an MDIPS entity"""
        node = GraphNode(
            label=entity.entity_type.value,
            properties={
                "entity_id": entity.entity_id,
                "label": entity.label,
                "description": entity.description,
                "attributes": entity.attributes,
                "domains": [d.value for d in entity.domains],
                "confidence": entity.confidence.dict(),
                "created_time": entity.created_time.isoformat(),
                "updated_time": entity.updated_time.isoformat()
            }
        )
        return await self.create_node(node)
    
    async def create_relationship_from_mdips(self, rel: MDIPSRelationship) -> bool:
        """Create a relationship from an MDIPS relationship object"""
        relationship = GraphRelationship(
            source_id=rel.source_entity_id,
            target_id=rel.target_entity_id,
            rel_type=rel.relationship_type.value,
            properties={
                "relationship_id": rel.relationship_id,
                "confidence": rel.confidence.dict(),
                "timestamp": rel.timestamp.isoformat(),
                "attributes": rel.attributes
            }
        )
        return await self.create_relationship(relationship)
    
    async def find_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Find an entity by ID"""
        query = """
        MATCH (n)
        WHERE n.properties.entity_id = $entity_id
        RETURN n.id as id, n.label as label, n.properties as properties
        """
        result = await self.client.run_query(query, {"entity_id": entity_id})
        if result:
            return result[0]
        return None
    
    async def get_relationships(self, entity_id: str, direction: str = "BOTH") -> List[Dict[str, Any]]:
        """Get all relationships for an entity"""
        if direction == "IN":
            query = """
            MATCH (a {{id: $entity_id}})<-[r]-(b)
            RETURN b.id as target_id, b.label as target_label, TYPE(r) as relationship_type, r.properties as properties
            """
        elif direction == "OUT":
            query = """
            MATCH (a {{id: $entity_id}})-[r]->(b)
            RETURN b.id as target_id, b.label as target_label, TYPE(r) as relationship_type, r.properties as properties
            """
        else:
            query = """
            MATCH (a {{id: $entity_id}})-[r]-(b)
            RETURN b.id as target_id, b.label as target_label, TYPE(r) as relationship_type, r.properties as properties
            """
        
        return await self.client.run_query(query, {"entity_id": entity_id})
    
    async def get_related_entities(
        self,
        entity_id: str,
        relationship_type: Optional[str] = None,
        max_depth: int = 2
    ) -> List[Dict[str, Any]]:
        """Get entities related to a given entity"""
        
        if relationship_type:
            query = """
            MATCH path = (a {{id: $entity_id}})-[:`{rel_type}`*1..{max_depth}]-(b)
            WHERE a.id <> b.id
            RETURN DISTINCT b.id as id, b.label as label, b.properties as properties,
                   length(path) as distance
            ORDER BY distance
            LIMIT 100
            """.format(rel_type=relationship_type, max_depth=max_depth)
        else:
            query = """
            MATCH path = (a {{id: $entity_id}})-[*1..{max_depth}]-(b)
            WHERE a.id <> b.id
            RETURN DISTINCT b.id as id, b.label as label, b.properties as properties,
                   length(path) as distance
            ORDER BY distance
            LIMIT 100
            """.format(max_depth=max_depth)
        
        return await self.client.run_query(query, {"entity_id": entity_id})
    
    async def find_connections(self, entity1_id: str, entity2_id: str, max_depth: int = 3) -> List[Dict[str, Any]]:
        """Find paths between two entities"""
        query = """
        MATCH path = shortestPath((a {{id: $entity1_id}})-[*1..{max_depth}]-(b {{id: $entity2_id}}))
        RETURN [node in nodes(path) | {{id: node.id, label: node.label}}] as nodes,
               [rel in relationships(path) | {{type: TYPE(rel), properties: rel.properties}}] as relationships
        """.format(max_depth=max_depth)
        
        return await self.client.run_query(query, {
            "entity1_id": entity1_id,
            "entity2_id": entity2_id
        })
    
    async def get_graph_summary(self) -> Dict[str, Any]:
        """Get summary of the knowledge graph"""
        query = """
        MATCH (n)
        RETURN count(n) as total_nodes,
               collect(DISTINCT labels(n)) as node_labels
        """
        node_result = await self.client.run_query(query)
        
        query = """
        MATCH ()-[r]->()
        RETURN count(r) as total_relationships,
               collect(DISTINCT TYPE(r)) as relationship_types
        """
        rel_result = await self.client.run_query(query)
        
        return {
            "total_nodes": node_result[0]["total_nodes"] if node_result else 0,
            "node_labels": node_result[0]["node_labels"] if node_result else [],
            "total_relationships": rel_result[0]["total_relationships"] if rel_result else 0,
            "relationship_types": rel_result[0]["relationship_types"] if rel_result else []
        }
    
    async def clear_graph(self) -> Dict[str, Any]:
        """Clear all nodes and relationships"""
        query = "MATCH (n) DETACH DELETE n"
        result = await self.client.run_write(query)
        return result