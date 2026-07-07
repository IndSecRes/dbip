"""
DBIP API Routes
"""

from fastapi import APIRouter
from datetime import datetime

print("✅ Routes file loaded!")

# Create router
router = APIRouter()


@router.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {"message": "Test endpoint works!", "timestamp": datetime.now().isoformat()}


@router.get("/intelligence/test")
async def test_pipeline():
    """Test the pipeline"""
    try:
        from src.orchestrator import PipelineOrchestrator
        orchestrator = PipelineOrchestrator()
        
        test_data = {
            "source_id": "api_test",
            "raw_content": "Test intelligence data from API",
            "metadata": {"source": "REST API", "priority": "high"}
        }
        
        result = await orchestrator.process_intelligence(test_data)
        
        return {
            "test": "completed",
            "request_id": result["request_id"],
            "stages_completed": result["summary"]["stages_completed"],
            "status": result["status"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@router.get("/intelligence/pipeline/info")
async def pipeline_info():
    """Pipeline information"""
    return {
        "pipeline_name": "DBIP Intelligence Pipeline",
        "version": "5.0.0",
        "total_stages": 19,
        "stages": [
            "Source Discovery", "Collection", "Quality Gate", "Raw Data Lake",
            "Normalization", "MDIPS Validation", "Ontology Mapping",
            "Entity Extraction", "Signal Fusion", "Relationship Construction",
            "Identity Resolution", "Evidence Assessment", "Signal Rating",
            "Confidence Calibration", "Temporal Intelligence", "Asset Builder",
            "Dataset Builder", "Intelligence Packaging", "ISCA Distribution"
        ],
        "timestamp": datetime.now().isoformat()
    }


@router.get("/status")
async def api_status():
    """API status"""
    return {
        "platform": "Data Brokerage & Intelligence Platform",
        "version": "5.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }
    
@router.get("/api/v1/status")
async def api_v1_status():
    """API v1 status endpoint"""
    from datetime import datetime
    return {
        "platform": "Data Brokerage & Intelligence Platform",
        "version": "6.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }