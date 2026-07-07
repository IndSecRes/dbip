"""
Federation Router
Routes messages between federation nodes
"""

from typing import Dict, Any, List, Optional, Callable
from collections import defaultdict
import asyncio

from src.federation.protocol import FederationMessage, FederationProtocol
from src.federation.registry import NodeRegistry, NodeInfo


class FederationRouter:
    """
    Routes messages between federation nodes
    """
    
    def __init__(self):
        self.registry = NodeRegistry()
        self.message_handlers: Dict[str, List[Callable]] = defaultdict(list)
        self.message_queue: List[FederationMessage] = []
        self.message_history: List[FederationMessage] = []
        self.running = False
    
    def add_handler(self, message_type: str, handler: Callable) -> None:
        """Add a message handler"""
        self.message_handlers[message_type].append(handler)
    
    async def send_message(self, message: FederationMessage) -> bool:
        """Send a message to a node"""
        # Validate message
        if not FederationProtocol.validate_message(message):
            return False
        
        # Check if target exists
        target_id = message.target_id
        if target_id:
            target = self.registry.get_node(target_id)
            if not target or target.status != "active":
                return False
        
        # Process message
        await self._process_message(message)
        return True
    
    async def broadcast(self, message: FederationMessage, exclude: Optional[List[str]] = None) -> None:
        """Broadcast a message to all active nodes"""
        active_nodes = self.registry.get_active_nodes()
        exclude = exclude or []
        
        for node in active_nodes:
            if node.node_id not in exclude and node.node_id != message.sender_id:
                # Create a copy for this node
                broadcast_msg = FederationMessage(
                    message_type=message.message_type,
                    sender_id=message.sender_id,
                    target_id=node.node_id,
                    payload=message.payload,
                    ttl=message.ttl,
                    priority=message.priority
                )
                await self._process_message(broadcast_msg)
    
    async def _process_message(self, message: FederationMessage) -> None:
        """Process a message"""
        # Add to queue
        self.message_queue.append(message)
        
        # Update TTL
        message.ttl -= 1
        if message.ttl <= 0:
            return
        
        # Find handlers
        handlers = self.message_handlers.get(message.message_type, [])
        
        # Execute handlers
        for handler in handlers:
            try:
                await handler(message)
            except Exception as e:
                # Log error
                pass
        
        # Store in history
        self.message_history.append(message)
    
    def get_queue_size(self) -> int:
        """Get queue size"""
        return len(self.message_queue)
    
    def get_history(self, limit: int = 100) -> List[FederationMessage]:
        """Get message history"""
        return self.message_history[-limit:]
    
    def clear_queue(self) -> None:
        """Clear message queue"""
        self.message_queue.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get router statistics"""
        return {
            "queue_size": len(self.message_queue),
            "history_size": len(self.message_history),
            "active_nodes": len(self.registry.get_active_nodes()),
            "total_nodes": len(self.registry.nodes)
        }