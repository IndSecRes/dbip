"""
Federation Support
Multi-node intelligence sharing
"""

from .hub import FederationHub
from .node import FederationNode, NodeInfo
from .registry import NodeRegistry
from .router import FederationRouter
from .protocol import FederationProtocol, FederationMessage

__all__ = [
    "FederationHub",
    "FederationNode",
    "NodeInfo",
    "NodeRegistry",
    "FederationRouter",
    "FederationProtocol",
    "FederationMessage"
]