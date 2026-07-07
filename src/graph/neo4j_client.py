"""
Neo4j Client
Handles connection and basic operations
"""

import logging
from typing import Optional, Dict, Any, List, Tuple
from neo4j import GraphDatabase, Driver, Session, Result, AsyncDriver, AsyncSession
from neo4j.exceptions import ServiceUnavailable, AuthError
from contextlib import contextmanager
from dataclasses import dataclass

from src.config import config

logger = logging.getLogger("DBIP.Graph")


class Neo4jClient:
    """
    Neo4j Database Client
    Manages connections and provides CRUD operations
    """
    
    def __init__(self):
        self.driver: Optional[Driver] = None
        self.uri = config.get("neo4j.uri", "bolt://localhost:7687")
        self.user = config.get("neo4j.user", "neo4j")
        self.password = config.get("neo4j.password", "password")
        self.database = config.get("neo4j.database", "neo4j")
        self._connected = False
    
    def connect(self) -> bool:
        """Establish connection to Neo4j"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Test connection
            with self.driver.session(database=self.database) as session:
                result = session.run("RETURN 1 as test")
                result.single()
            self._connected = True
            logger.info(f"✅ Connected to Neo4j at {self.uri}")
            return True
        except AuthError:
            logger.error(f"❌ Authentication failed for Neo4j at {self.uri}")
            return False
        except ServiceUnavailable:
            logger.error(f"❌ Service unavailable for Neo4j at {self.uri}")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to connect to Neo4j: {e}")
            return False
    
    def disconnect(self):
        """Close connection to Neo4j"""
        if self.driver:
            self.driver.close()
            self._connected = False
            logger.info("Disconnected from Neo4j")
    
    def is_connected(self) -> bool:
        """Check if connected to Neo4j"""
        return self._connected
    
    @contextmanager
    def get_session(self) -> Session:
        """Get a session for executing queries"""
        if not self.driver:
            self.connect()
        if not self._connected:
            raise RuntimeError("Not connected to Neo4j")
        
        session = self.driver.session(database=self.database)
        try:
            yield session
        finally:
            session.close()
    
    async def run_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Run a Cypher query and return results"""
        results = []
        try:
            with self.get_session() as session:
                result = session.run(query, parameters or {})
                for record in result:
                    results.append(record.data())
            return results
        except Exception as e:
            logger.error(f"Query failed: {e}")
            logger.debug(f"Query: {query}")
            raise
    
    async def run_write(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run a write query and return summary"""
        try:
            with self.get_session() as session:
                result = session.run(query, parameters or {})
                summary = result.consume()
                return {
                    "nodes_created": summary.counters.nodes_created,
                    "nodes_deleted": summary.counters.nodes_deleted,
                    "relationships_created": summary.counters.relationships_created,
                    "relationships_deleted": summary.counters.relationships_deleted,
                    "properties_set": summary.counters.properties_set
                }
        except Exception as e:
            logger.error(f"Write query failed: {e}")
            logger.debug(f"Query: {query}")
            raise


# Singleton instance
_neo4j_client: Optional[Neo4jClient] = None


def get_neo4j_client() -> Neo4jClient:
    """Get the singleton Neo4j client"""
    global _neo4j_client
    if _neo4j_client is None:
        _neo4j_client = Neo4jClient()
        _neo4j_client.connect()
    return _neo4j_client