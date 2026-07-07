"""
Federation Protocol
Message formats and communication protocol
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import json


@dataclass
class FederationMessage:
    """Message exchanged between federation nodes"""
    message_type: str
    sender_id: str
    message_id: str = field(default_factory=lambda: f"MSG_{uuid.uuid4().hex[:8].upper()}")
    target_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: int = 60  # Time to live in seconds
    priority: int = 0  # 0-10, higher = more important
    signature: Optional[str] = None


class FederationProtocol:
    """
    Federation communication protocol
    """
    
    VERSION = "1.0"
    
    @staticmethod
    def create_discovery_message(node_id: str) -> FederationMessage:
        """Create a discovery message"""
        return FederationMessage(
            message_type="discovery",
            sender_id=node_id,
            payload={
                "version": FederationProtocol.VERSION,
                "capabilities": ["entity_sharing", "query", "sync"]
            }
        )
    
    @staticmethod
    def create_share_message(
        node_id: str,
        target_id: Optional[str],
        data_type: str,
        data: Dict[str, Any]
    ) -> FederationMessage:
        """Create a share message"""
        return FederationMessage(
            message_type="share",
            sender_id=node_id,
            target_id=target_id,
            payload={
                "data_type": data_type,
                "data": data
            }
        )
    
    @staticmethod
    def create_query_message(
        node_id: str,
        target_id: Optional[str],
        query: Dict[str, Any]
    ) -> FederationMessage:
        """Create a query message"""
        return FederationMessage(
            message_type="query",
            sender_id=node_id,
            target_id=target_id,
            payload={
                "query": query
            }
        )
    
    @staticmethod
    def create_response_message(
        node_id: str,
        original_message_id: str,
        data: Dict[str, Any]
    ) -> FederationMessage:
        """Create a response message"""
        return FederationMessage(
            message_type="response",
            sender_id=node_id,
            payload={
                "original_message_id": original_message_id,
                "data": data
            }
        )
    
    @staticmethod
    def create_sync_message(
        node_id: str,
        target_id: Optional[str],
        sync_type: str,
        data: Dict[str, Any]
    ) -> FederationMessage:
        """Create a sync message"""
        return FederationMessage(
            message_type="sync",
            sender_id=node_id,
            target_id=target_id,
            payload={
                "sync_type": sync_type,
                "data": data
            }
        )
    
    @staticmethod
    def validate_message(message: FederationMessage) -> bool:
        """Validate a message"""
        if not message.message_type or not message.sender_id:
            return False
        
        valid_types = ["discovery", "share", "query", "response", "sync"]
        if message.message_type not in valid_types:
            return False
        
        # Check TTL
        if message.ttl <= 0:
            return False
        
        return True
    
    @staticmethod
    def serialize(message: FederationMessage) -> str:
        """Serialize a message to JSON"""
        return json.dumps({
            "message_id": message.message_id,
            "message_type": message.message_type,
            "sender_id": message.sender_id,
            "target_id": message.target_id,
            "payload": message.payload,
            "timestamp": message.timestamp.isoformat(),
            "ttl": message.ttl,
            "priority": message.priority,
            "signature": message.signature
        })
    
    @staticmethod
    def deserialize(data: str) -> FederationMessage:
        """Deserialize a message from JSON"""
        obj = json.loads(data)
        return FederationMessage(
            message_type=obj.get("message_type"),
            sender_id=obj.get("sender_id"),
            message_id=obj.get("message_id"),
            target_id=obj.get("target_id"),
            payload=obj.get("payload", {}),
            timestamp=datetime.fromisoformat(obj.get("timestamp")),
            ttl=obj.get("ttl", 60),
            priority=obj.get("priority", 0),
            signature=obj.get("signature")
        )