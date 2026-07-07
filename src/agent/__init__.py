"""
Agent System
AI agents for autonomous intelligence gathering
"""

from .base import BaseAgent, AgentContext, AgentResult
from .orchestrator import AgentOrchestrator, get_orchestrator
from .agents import (
    CollectionAgent,
    AnalysisAgent,
    AlertAgent,
    EntityAgent,
    CorrelationAgent,
    ReportAgent
)
from .skills import SkillRegistry, Skill
from .memory import AgentMemory, MemoryEntry

__all__ = [
    "BaseAgent",
    "AgentContext",
    "AgentResult",
    "AgentOrchestrator",
    "get_orchestrator",
    "CollectionAgent",
    "AnalysisAgent",
    "AlertAgent",
    "EntityAgent",
    "CorrelationAgent",
    "ReportAgent",
    "SkillRegistry",
    "Skill",
    "AgentMemory",
    "MemoryEntry"
]