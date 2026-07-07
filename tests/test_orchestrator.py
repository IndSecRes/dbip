"""
Tests for pipeline orchestrator
"""

import pytest
import asyncio
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.orchestrator import PipelineOrchestrator, PipelineContext
from src.models import ProvenanceNode


@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test orchestrator initialization"""
    orchestrator = PipelineOrchestrator()
    assert orchestrator is not None
    assert orchestrator.logger is not None


@pytest.mark.asyncio
async def test_pipeline_context_creation():
    """Test pipeline context creation"""
    context = PipelineContext()
    assert context.request_id is not None
    assert context.start_time is not None
    assert context.current_stage == "init"
    assert context.provenance_chain == []


@pytest.mark.asyncio
async def test_pipeline_context_add_provenance():
    """Test adding provenance to context"""
    context = PipelineContext()
    provenance = ProvenanceNode(
        source_id="test_source",
        source_type="API",
        confidence_score=0.9
    )
    context.add_provenance(provenance)
    assert len(context.provenance_chain) == 1
    assert context.provenance_chain[0].source_id == "test_source"


@pytest.mark.asyncio
async def test_orchestrator_process_intelligence():
    """Test full pipeline processing"""
    orchestrator = PipelineOrchestrator()
    
    test_data = {
        "source_id": "test_source",
        "raw_content": "Test intelligence data",
        "metadata": {"priority": "high"}
    }
    
    result = await orchestrator.process_intelligence(test_data)
    
    assert result["status"] == "success"
    assert "request_id" in result
    assert "summary" in result
    assert result["summary"]["stages_completed"] == 19


@pytest.mark.asyncio
async def test_orchestrator_stage_execution():
    """Test individual stage execution"""
    orchestrator = PipelineOrchestrator()
    context = PipelineContext()
    
    test_data = {"test": "data"}
    
    # Test source discovery stage
    result = await orchestrator._source_discovery(test_data, context)
    assert "sources_discovered" in result
    assert len(result["sources_discovered"]) > 0


@pytest.mark.asyncio
async def test_orchestrator_error_handling():
    """Test orchestrator error handling"""
    orchestrator = PipelineOrchestrator()
    
    # Test with empty data (should handle gracefully)
    result = await orchestrator.process_intelligence({})
    # Should handle gracefully - either success or failure with error
    assert result["status"] in ["success", "failed"]
    assert "request_id" in result


@pytest.mark.asyncio
async def test_orchestrator_stage_methods():
    """Test all stage methods exist and return expected format"""
    orchestrator = PipelineOrchestrator()
    context = PipelineContext()
    
    stages = [
        "_source_discovery",
        "_collection",
        "_quality_gate",
        "_raw_data_lake",
        "_normalization",
        "_mdips_validation",
        "_ontology_mapping",
        "_entity_extraction",
        "_signal_fusion",
        "_relationship_construction",
        "_identity_resolution",
        "_evidence_assessment",
        "_signal_rating",
        "_confidence_calibration",
        "_temporal_intelligence",
        "_asset_builder",
        "_dataset_builder",
        "_intelligence_packaging",
        "_isca_distribution"
    ]
    
    test_data = {"test": "data"}
    
    for stage_name in stages:
        stage_method = getattr(orchestrator, stage_name, None)
        assert stage_method is not None, f"Stage {stage_name} does not exist"
        
        result = await stage_method(test_data, context)
        assert result is not None, f"Stage {stage_name} returned None"
        assert isinstance(result, dict), f"Stage {stage_name} did not return dict"