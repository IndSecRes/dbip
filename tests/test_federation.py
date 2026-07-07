"""
Tests for Federation Support
"""

import pytest
import asyncio
from src.federation import (
    FederationHub,
    FederationNode,
    NodeRegistry,
    NodeInfo,
    FederationRouter,
    FederationMessage,
    FederationProtocol
)


def test_node_registry():
    """Test node registry"""
    registry = NodeRegistry()
    
    node_info = NodeInfo(
        node_id="test_node_001",
        name="Test Node",
        description="Test node description",
        capabilities=["test"]
    )
    
    registry.register(node_info)
    assert registry.get_node("test_node_001") is not None
    assert len(registry.get_active_nodes()) == 1


def test_federation_protocol():
    """Test federation protocol"""
    message = FederationProtocol.create_discovery_message("test_node")
    
    assert message.message_type == "discovery"
    assert message.sender_id == "test_node"
    assert FederationProtocol.validate_message(message) is True


def test_federation_hub():
    """Test federation hub"""
    hub = FederationHub("hub_001", "Test Hub")
    
    status = hub.get_status()
    assert status["hub_id"] == "hub_001"
    assert status["status"] == "active"
    assert "registry" in status


def test_federation_node():
    """Test federation node"""
    node = FederationNode(name="Test Node")
    
    assert node.node_id.startswith("NODE_")
    assert node.name == "Test Node"
    assert "entity_sharing" in node.capabilities


@pytest.mark.asyncio
async def test_node_registration():
    """Test node registration with hub"""
    hub = FederationHub("hub_001", "Test Hub")
    node = FederationNode(name="Test Node")
    
    # Register node
    result = await node.register_with_hub(hub)
    
    # Node should be registered
    assert result is True
    assert node.registered is True


@pytest.mark.asyncio
async def test_data_sharing():
    """Test data sharing"""
    hub = FederationHub("hub_001", "Test Hub")
    node = FederationNode(name="Test Node")
    
    # Register node
    await node.register_with_hub(hub)
    
    # Share data
    result = await node.share_data(
        hub,
        "entities",
        {"entity": "Test Entity"}
    )
    
    assert result is True


def test_router_handlers():
    """Test router message handlers"""
    router = FederationRouter()
    
    # Add handler
    handler_called = False
    
    async def test_handler(message):
        nonlocal handler_called
        handler_called = True
    
    router.add_handler("test", test_handler)
    
    # Create test message
    message = FederationMessage(
        message_type="test",
        sender_id="test_node",
        ttl=60
    )
    
    # Process message
    asyncio.run(router._process_message(message))
    
    assert handler_called is True