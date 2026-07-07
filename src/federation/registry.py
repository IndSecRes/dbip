"""
Node Registry
Manages registered federation nodes
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class NodeInfo:
    """Information about a federation node"""
    node_id: str
    name: str
    description: str
    capabilities: List[str] = field(default_factory=list)
    url: Optional[str] = None
    version: str = "1.0"
    status: str = "active"  # active, inactive, offline
    last_seen: datetime = field(default_factory=datetime.now)
    registered_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class NodeRegistry:
    """
    Registry of federation nodes
    """
    
    def __init__(self):
        self.nodes: Dict[str, NodeInfo] = {}
    
    def register(self, node_info: NodeInfo) -> bool:
        """Register a node"""
        if node_info.node_id in self.nodes:
            # Update existing node
            existing = self.nodes[node_info.node_id]
            existing.name = node_info.name
            existing.description = node_info.description
            existing.capabilities = node_info.capabilities
            existing.url = node_info.url
            existing.version = node_info.version
            existing.status = node_info.status
            existing.last_seen = datetime.now()
            existing.metadata = node_info.metadata
            return True
        else:
            # Register new node
            self.nodes[node_info.node_id] = node_info
            return True
    
    def unregister(self, node_id: str) -> bool:
        """Unregister a node"""
        if node_id in self.nodes:
            self.nodes[node_id].status = "offline"
            return True
        return False
    
    def get_node(self, node_id: str) -> Optional[NodeInfo]:
        """Get node information"""
        return self.nodes.get(node_id)
    
    def get_active_nodes(self) -> List[NodeInfo]:
        """Get all active nodes"""
        return [
            node for node in self.nodes.values()
            if node.status == "active"
        ]
    
    def get_nodes_by_capability(self, capability: str) -> List[NodeInfo]:
        """Get nodes with a specific capability"""
        return [
            node for node in self.nodes.values()
            if node.status == "active" and capability in node.capabilities
        ]
    
    def update_status(self, node_id: str, status: str) -> bool:
        """Update node status"""
        if node_id in self.nodes:
            self.nodes[node_id].status = status
            self.nodes[node_id].last_seen = datetime.now()
            return True
        return False
    
    def update_last_seen(self, node_id: str) -> bool:
        """Update node last seen timestamp"""
        if node_id in self.nodes:
            self.nodes[node_id].last_seen = datetime.now()
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        nodes = self.nodes.values()
        return {
            "total_nodes": len(nodes),
            "active_nodes": len([n for n in nodes if n.status == "active"]),
            "offline_nodes": len([n for n in nodes if n.status == "offline"]),
            "capabilities": list(set(
                cap for node in nodes for cap in node.capabilities
            )),
            "nodes": [
                {
                    "id": n.node_id,
                    "name": n.name,
                    "status": n.status,
                    "capabilities": n.capabilities,
                    "last_seen": n.last_seen.isoformat()
                }
                for n in nodes
            ]
        }