"""
DBIP - Data Brokerage & Intelligence Platform
Clean Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import traceback

# Create FastAPI instance
app = FastAPI(
    title="DBIP - Data Brokerage & Intelligence Platform",
    description="Trusted information brokerage layer of the Intelligence Ecosystem",
    version="5.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# BASIC ROUTES
# ============================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "DBIP",
        "version": "5.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "documentation": "/docs",
        "endpoints": [
            "/health",
            "/test",
            "/intelligence/test",
            "/intelligence/pipeline/info"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {
        "message": "Test endpoint works!",
        "timestamp": datetime.now().isoformat()
    }


# ============================================
# INTELLIGENCE PIPELINE ROUTES
# ============================================

@app.get("/intelligence/test")
async def test_pipeline():
    """Test the full intelligence pipeline"""
    print("\n" + "="*60)
    print("📌 /intelligence/test called")
    print("="*60)
    
    try:
        print("📌 Importing orchestrator...")
        from src.orchestrator import PipelineOrchestrator
        print("✅ Orchestrator imported")
        
        print("📌 Creating orchestrator instance...")
        orchestrator = PipelineOrchestrator()
        print("✅ Orchestrator created")
        
        test_data = {
            "source_id": "api_test",
            "raw_content": "Test intelligence data from API",
            "metadata": {"source": "REST API", "priority": "high"}
        }
        
        print("📌 Running pipeline...")
        result = await orchestrator.process_intelligence(test_data)
        print(f"✅ Pipeline completed with {result['summary']['stages_completed']} stages")
        
        return {
            "test": "completed",
            "request_id": result["request_id"],
            "stages_completed": result["summary"]["stages_completed"],
            "status": result["status"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ ERROR: {error_details}")
        return {
            "error": str(e),
            "traceback": error_details.split("\n"),
            "timestamp": datetime.now().isoformat()
        }


@app.get("/intelligence/pipeline/info")
async def pipeline_info():
    """Get information about the pipeline"""
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
    
@app.get("/api/v1/status")
async def api_v1_status():
    """API v1 status endpoint"""
    from datetime import datetime
    return {
        "platform": "Data Brokerage & Intelligence Platform",
        "version": "6.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }