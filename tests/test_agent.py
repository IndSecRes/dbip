"""
Tests for Agent System
"""

import pytest
import asyncio
from src.agent import (
    AgentOrchestrator,
    CollectionAgent,
    AnalysisAgent,
    AlertAgent,
    EntityAgent,
    CorrelationAgent,
    ReportAgent,
    AgentContext,
    AgentMemory
)


def test_agent_creation():
    """Test agent creation"""
    agent = CollectionAgent()
    assert agent.agent_id.startswith("AGENT_")
    assert agent.name == "Collection Agent"
    assert "collect_data" in agent.skills


def test_agent_memory():
    """Test agent memory"""
    memory = AgentMemory()
    
    memory.store("test_key", "test_value", "short_term")
    assert memory.retrieve("test_key") == "test_value"
    
    memory.store("long_term_key", "long_term_value", "long_term")
    result = memory.retrieve_long_term("long_term_key")
    assert len(result) >= 1


def test_agent_orchestrator():
    """Test agent orchestrator"""
    orchestrator = AgentOrchestrator()
    assert len(orchestrator.agents) >= 4  # At least default agents


@pytest.mark.asyncio
async def test_collection_agent():
    """Test collection agent"""
    agent = CollectionAgent()
    context = AgentContext(
        agent_id=agent.agent_id,
        task_id="test_task",
        parameters={"source": "telegram", "query": "test", "limit": 3}
    )
    
    result = await agent.execute(context)
    assert result.status == "success"
    assert "source" in result.data
    assert "items" in result.data


@pytest.mark.asyncio
async def test_analysis_agent():
    """Test analysis agent"""
    agent = AnalysisAgent()
    context = AgentContext(
        agent_id=agent.agent_id,
        task_id="test_task",
        parameters={"data": {"items": [1, 2, 3, 4, 5]}}
    )
    
    result = await agent.execute(context)
    assert result.status == "success"
    assert "patterns" in result.data


@pytest.mark.asyncio
async def test_alert_agent():
    """Test alert agent"""
    agent = AlertAgent()
    context = AgentContext(
        agent_id=agent.agent_id,
        task_id="test_task",
        parameters={"condition": "test_condition", "severity": "high", "message": "Test alert"}
    )
    
    result = await agent.execute(context)
    assert result.status == "success"
    assert "alert" in result.data


@pytest.mark.asyncio
async def test_orchestrator_execution():
    """Test orchestrator execution"""
    orchestrator = AgentOrchestrator()
    
    task = {
        "type": "collection",
        "parameters": {"source": "telegram", "query": "test"}
    }
    
    result = await orchestrator.execute_task(task)
    assert result.status == "success"
    assert result.agent_id is not None


@pytest.mark.asyncio
async def test_multiple_tasks():
    """Test multiple tasks"""
    orchestrator = AgentOrchestrator()
    
    tasks = [
        {"type": "collection", "parameters": {"source": "telegram"}},
        {"type": "analysis", "parameters": {"data": {"test": "data"}}},
        {"type": "alert", "parameters": {"message": "test alert"}}
    ]
    
    results = await orchestrator.execute_multiple(tasks)
    assert len(results) == 3
    assert all(r.status == "success" for r in results)