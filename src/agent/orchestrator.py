"""
Agent Orchestrator
Manages agent lifecycle and task routing
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from src.agent.base import BaseAgent, AgentContext, AgentResult
from src.agent.agents import (
    CollectionAgent,
    AnalysisAgent,
    AlertAgent,
    EntityAgent,
    CorrelationAgent,
    ReportAgent
)
from src.agent.skills import SkillRegistry
from src.agent.memory import AgentMemory


class AgentOrchestrator:
    """
    Orchestrates agent execution
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.skill_registry = SkillRegistry()
        self.memory = AgentMemory()
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, AgentResult] = {}
        self.running: bool = False
        
        # Register default agents
        self._register_default_agents()
    
    def _register_default_agents(self) -> None:
        """Register default agents"""
        agents = [
            CollectionAgent(),
            AnalysisAgent(),
            AlertAgent(),
            EntityAgent(),
            CorrelationAgent(),
            ReportAgent()
        ]
        for agent in agents:
            self.register_agent(agent)
    
    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent"""
        self.agents[agent.agent_id] = agent
    
    def register_skill(self, skill) -> None:
        """Register a skill"""
        self.skill_registry.register(skill)
    
    async def execute_task(self, task: Dict[str, Any]) -> AgentResult:
        """
        Execute a task using the appropriate agent
        
        Args:
            task: Task with type and parameters
        
        Returns:
            AgentResult from the executed task
        """
        task_id = task.get("task_id", str(uuid.uuid4()))
        task_type = task.get("type", "general")
        parameters = task.get("parameters", {})
        
        # Store task
        self.tasks[task_id] = {
            "task_id": task_id,
            "type": task_type,
            "parameters": parameters,
            "created_at": datetime.now().isoformat()
        }
        
        # Find suitable agent
        agent = self._find_agent(task)
        if not agent:
            return AgentResult(
                task_id=task_id,
                agent_id="unknown",
                status="failed",
                error=f"No agent found for task type: {task_type}"
            )
        
        # Create context
        context = AgentContext(
            agent_id=agent.agent_id,
            task_id=task_id,
            parameters=parameters
        )
        
        # Execute agent
        try:
            result = await agent.execute(context)
            self.results[task_id] = result
            return result
        except Exception as e:
            result = AgentResult(
                task_id=task_id,
                agent_id=agent.agent_id,
                status="failed",
                error=str(e)
            )
            self.results[task_id] = result
            return result
    
    async def execute_multiple(self, tasks: List[Dict[str, Any]]) -> List[AgentResult]:
        """Execute multiple tasks in parallel"""
        results = await asyncio.gather(
            *[self.execute_task(task) for task in tasks]
        )
        return list(results)
    
    def _find_agent(self, task: Dict[str, Any]) -> Optional[BaseAgent]:
        """Find the best agent for a task"""
        # First pass: exact match
        for agent in self.agents.values():
            if agent.can_handle(task):
                return agent
        
        # Second pass: any agent that might handle it
        for agent in self.agents.values():
            if hasattr(agent, "can_handle") and agent.can_handle(task):
                return agent
        
        return None
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "total_agents": len(self.agents),
            "agents": [
                {
                    "id": agent.agent_id,
                    "name": agent.name,
                    "description": agent.description,
                    "skills": agent.skills,
                    "tools": agent.tools
                }
                for agent in self.agents.values()
            ],
            "total_tasks": len(self.tasks),
            "total_results": len(self.results),
            "memory_stats": self.memory.get_stats()
        }
    
    def get_task_result(self, task_id: str) -> Optional[AgentResult]:
        """Get the result of a task"""
        return self.results.get(task_id)
    
    def get_task_summary(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of a task"""
        task = self.tasks.get(task_id)
        result = self.results.get(task_id)
        
        if not task:
            return None
        
        return {
            "task": task,
            "result": {
                "status": result.status if result else "pending",
                "data": result.data if result else None,
                "duration": result.duration if result else 0
            } if result else None
        }
    
    def clear_completed(self) -> None:
        """Clear completed tasks and results"""
        completed = [
            tid for tid, result in self.results.items()
            if result.status in ["success", "failed"]
        ]
        for tid in completed:
            self.tasks.pop(tid, None)
            self.results.pop(tid, None)


# Create a singleton instance
_orchestrator: Optional[AgentOrchestrator] = None


def get_orchestrator() -> AgentOrchestrator:
    """Get the singleton orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator