"""
Tests for Evolution Engine
"""

import pytest
from datetime import datetime, timedelta
from src.evolution import (
    EvolutionEngine,
    PatternDiscovery,
    TaxonomyManager,
    FeedbackSystem
)


def test_pattern_discovery():
    """Test pattern discovery"""
    discovery = PatternDiscovery()
    
    entities = [
        {"type": "person", "name": "John Doe", "source": "telegram"},
        {"type": "person", "name": "John Doe", "source": "discord"},
        {"type": "person", "name": "John Doe", "source": "twitter"},
        {"type": "person", "name": "Jane Smith", "source": "telegram"}
    ]
    
    patterns = discovery.discover_entity_patterns(entities)
    assert len(patterns) >= 1
    assert patterns[0].occurrences >= 2


def test_taxonomy_manager():
    """Test taxonomy manager"""
    taxonomy = TaxonomyManager()
    
    proposal = taxonomy.propose_category(
        name="test_category",
        description="Test category",
        evidence=[{"type": "test"}]
    )
    
    assert proposal.proposal_id.startswith("PROP_")
    assert proposal.status == "proposed"
    
    taxonomy.approve_category(proposal.proposal_id)
    assert proposal.status == "approved"
    
    taxonomy.implement_category(proposal.proposal_id)
    assert proposal.status == "implemented"
    assert "test_category" in taxonomy.categories


def test_feedback_system():
    """Test feedback system"""
    feedback = FeedbackSystem()
    
    entry = feedback.add_feedback(
        feedback_type="accuracy",
        rating=0.85,
        target_id="test_001",
        target_type="entity"
    )
    
    assert entry.feedback_id.startswith("FDB_")
    assert entry.rating == 0.85
    assert feedback.get_average_score("test_001") > 0


def test_evolution_engine():
    """Test evolution engine"""
    engine = EvolutionEngine()
    
    data = {
        "entities": [
            {"type": "person", "name": "John Doe", "source": "telegram"},
            {"type": "person", "name": "John Doe", "source": "discord"},
            {"type": "person", "name": "Jane Smith", "source": "telegram"}
        ],
        "timestamps": [
            datetime.now(),
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=2)
        ],
        "categories": [
            {"name": "test_category", "keywords": ["test", "example"]}
        ]
    }
    
    # This is async, so we need to run it
    import asyncio
    result = asyncio.run(engine.evolve(data))
    
    assert "patterns" in result
    assert "proposals" in result
    assert "changes" in result


def test_evolution_status():
    """Test evolution engine status"""
    engine = EvolutionEngine()
    status = engine.get_status()
    
    assert "pattern_count" in status
    assert "taxonomy" in status
    assert "feedback" in status
    assert "pending_proposals" in status