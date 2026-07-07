"""
Base Agent
Defines the core agent interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class AgentContext:
    """Context for agent execution"""
    agent_id: str
    task_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    memory: Dict[str, Any] = field(default_factory=dict)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    status: str = "running"
    error: Optional[str] = None


@dataclass
class AgentResult:
    """Result of agent execution"""
    task_id: str
    agent_id: str
    status: str  # "success", "failed", "partial"
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Abstract base class for all agents
    """
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.skills: List[str] = []
        self.tools: List[str] = []
    
    @abstractmethod
    async def execute(self, context: AgentContext) -> AgentResult:
        """Execute the agent's primary function"""
        pass
    
    @abstractmethod
    def can_handle(self, task: Dict[str, Any]) -> bool:
        """Check if this agent can handle a task"""
        pass
    
    def add_skill(self, skill_id: str) -> None:
        """Add a skill to the agent"""
        if skill_id not in self.skills:
            self.skills.append(skill_id)
    
    def add_tool(self, tool_id: str) -> None:
        """Add a tool to the agent"""
        if tool_id not in self.tools:
            self.tools.append(tool_id)
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "skills": self.skills,
            "tools": self.tools
        }