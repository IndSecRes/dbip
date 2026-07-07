"""
Federation Node
Individual node in the federation
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import asyncio

from src.federation.protocol import FederationMessage, FederationProtocol
from src.federation.registry import NodeInfo


class FederationNode:
    """
    Federation node for intelligence sharing
    """
    
    def __init__(
        self,
        node_id: Optional[str] = None,
        name: str = "DBIP Node",
        description: str = "",
        hub_url: Optional[str] = None
    ):
        self.node_id = node_id or f"NODE_{uuid.uuid4().hex[:8].upper()}"
        self.name = name
        self.description = description
        self.hub_url = hub_url
        self.capabilities: List[str] = [
            "entity_sharing",
            "query",
            "sync",
            "embeddings"
        ]
        self.connected_nodes: List[str] = []
        self.message_history: List[FederationMessage] = []
        self.registered = False
    
    def register_capability(self, capability: str) -> None:
        """Add a capability to the node"""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
    
    def get_node_info(self) -> NodeInfo:
        """Get node information"""
        return NodeInfo(
            node_id=self.node_id,
            name=self.name,
            description=self.description,
            capabilities=self.capabilities,
            url=self.hub_url,
            version="1.0"
        )
    
    async def register_with_hub(self, hub) -> bool:
        """Register with a federation hub"""
        # Create discovery message
        discovery = FederationProtocol.create_discovery_message(self.node_id)
        discovery.payload.update({
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "url": self.hub_url,
            "version": "1.0"
        })
        
        # Send to hub
        result = await hub.router.send_message(discovery)
        if result:
            self.registered = True
            self.connected_nodes.append(hub.hub_id)
        
        return result
    
    async def share_data(self, hub, data_type: str, data: Dict[str, Any]) -> bool:
        """Share data with the federation"""
        if not self.registered:
            return False
        
        message = FederationProtocol.create_share_message(
            node_id=self.node_id,
            target_id=None,  # Broadcast
            data_type=data_type,
            data=data
        )
        
        return await hub.router.send_message(message)
    
    async def query_federation(self, hub, query: Dict[str, Any]) -> Dict[str, Any]:
        """Query the federation"""
        if not self.registered:
            return {"error": "Not registered with federation"}
        
        message = FederationProtocol.create_query_message(
            node_id=self.node_id,
            target_id=None,
            query=query
        )
        
        # Send and wait for response
        result = await hub.router.send_message(message)
        if result:
            # In a real implementation, would wait for response
            return {"status": "query_sent", "query_id": message.message_id}
        
        return {"error": "Failed to send query"}
    
    def get_status(self) -> Dict[str, Any]:
        """Get node status"""
        return {
            "node_id": self.node_id,
            "name": self.name,
            "description": self.description,
            "registered": self.registered,
            "capabilities": self.capabilities,
            "connected_nodes": self.connected_nodes,
            "message_count": len(self.message_history)
        }
    
    def get_shareable_data(self, data_type: str) -> Dict[str, Any]:
        """Get data to share with the federation"""
        # Placeholder - would return actual data
        return {
            "node_id": self.node_id,
            "data_type": data_type,
            "timestamp": datetime.now().isoformat(),
            "data": {
                "sample": "This is shareable data"
            }
        }