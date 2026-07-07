"""
Federation Hub
Central coordination for federation
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

from src.federation.protocol import FederationMessage, FederationProtocol
from src.federation.registry import NodeRegistry, NodeInfo
from src.federation.router import FederationRouter


class FederationHub:
    """
    Central hub for federation coordination
    """
    
    def __init__(self, hub_id: str, name: str = "Federation Hub"):
        self.hub_id = hub_id
        self.name = name
        self.router = FederationRouter()
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Setup default message handlers"""
        self.router.add_handler("discovery", self._handle_discovery)
        self.router.add_handler("share", self._handle_share)
        self.router.add_handler("query", self._handle_query)
        self.router.add_handler("sync", self._handle_sync)
    
    async def _handle_discovery(self, message: FederationMessage) -> None:
        """Handle discovery message"""
        # Register the node
        payload = message.payload
        node_info = NodeInfo(
            node_id=message.sender_id,
            name=payload.get("name", f"Node_{message.sender_id[:8]}"),
            description=payload.get("description", ""),
            capabilities=payload.get("capabilities", []),
            url=payload.get("url"),
            version=payload.get("version", "1.0")
        )
        self.router.registry.register(node_info)
        
        # Send response with hub info
        response = FederationProtocol.create_response_message(
            node_id=self.hub_id,
            original_message_id=message.message_id,
            data={
                "hub_id": self.hub_id,
                "name": self.name,
                "supported_versions": ["1.0"],
                "active_nodes": len(self.router.registry.get_active_nodes())
            }
        )
        await self.router.send_message(response)
    
    async def _handle_share(self, message: FederationMessage) -> None:
        """Handle share message"""
        payload = message.payload
        data_type = payload.get("data_type")
        data = payload.get("data", {})
        
        # Store shared data
        self.router.registry.update_last_seen(message.sender_id)
        
        # Log the share
        print(f"📤 Node {message.sender_id} shared {data_type}: {len(data)} items")
    
    async def _handle_query(self, message: FederationMessage) -> None:
        """Handle query message"""
        payload = message.payload
        query = payload.get("query", {})
        
        self.router.registry.update_last_seen(message.sender_id)
        
        # Process query
        results = await self._process_query(query)
        
        # Send response
        response = FederationProtocol.create_response_message(
            node_id=self.hub_id,
            original_message_id=message.message_id,
            data=results
        )
        await self.router.send_message(response)
    
    async def _handle_sync(self, message: FederationMessage) -> None:
        """Handle sync message"""
        payload = message.payload
        sync_type = payload.get("sync_type")
        data = payload.get("data", {})
        
        self.router.registry.update_last_seen(message.sender_id)
        
        # Process sync based on type
        if sync_type == "entities":
            await self._sync_entities(message.sender_id, data)
        elif sync_type == "embeddings":
            await self._sync_embeddings(message.sender_id, data)
        elif sync_type == "summaries":
            await self._sync_summaries(message.sender_id, data)
    
    async def _process_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Process a query"""
        # Placeholder - would query local intelligence
        return {
            "status": "processed",
            "query": query,
            "results": []
        }
    
    async def _sync_entities(self, node_id: str, data: Dict[str, Any]) -> None:
        """Sync entities with a node"""
        # Placeholder - would sync entities
        pass
    
    async def _sync_embeddings(self, node_id: str, data: Dict[str, Any]) -> None:
        """Sync embeddings with a node"""
        # Placeholder - would sync embeddings
        pass
    
    async def _sync_summaries(self, node_id: str, data: Dict[str, Any]) -> None:
        """Sync summaries with a node"""
        # Placeholder - would sync summaries
        pass
    
    def register_node(self, node_info: NodeInfo) -> bool:
        """Register a node directly"""
        return self.router.registry.register(node_info)
    
    def get_status(self) -> Dict[str, Any]:
        """Get hub status"""
        registry_stats = self.router.registry.get_stats()
        router_stats = self.router.get_stats()
        
        return {
            "hub_id": self.hub_id,
            "name": self.name,
            "status": "active",
            "registry": registry_stats,
            "router": router_stats,
            "timestamp": datetime.now().isoformat()
        }