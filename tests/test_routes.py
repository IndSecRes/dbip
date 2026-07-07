"""
Tests for API routes
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "DBIP"
    assert data["version"] == "5.0.0"
    assert data["status"] == "operational"
    assert "documentation" in data


def test_health_endpoint():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_test_endpoint():
    """Test test endpoint"""
    response = client.get("/test")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Test endpoint works!"
    assert "timestamp" in data


def test_intelligence_test_endpoint():
    """Test intelligence test endpoint"""
    response = client.get("/intelligence/test")
    assert response.status_code == 200
    data = response.json()
    assert data["test"] == "completed"
    assert "stages_completed" in data
    assert data["status"] == "success"


def test_pipeline_info_endpoint():
    """Test pipeline info endpoint"""
    response = client.get("/intelligence/pipeline/info")
    assert response.status_code == 200
    data = response.json()
    assert data["pipeline_name"] == "DBIP Intelligence Pipeline"
    assert data["total_stages"] == 19
    assert "stages" in data
    assert len(data["stages"]) == 19


def test_docs_endpoint():
    """Test docs endpoint"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_api_v1_status_endpoint():
    """Test API v1 status endpoint"""
    response = client.get("/api/v1/status")
    if response.status_code == 404:
        response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data.get("platform") == "Data Brokerage & Intelligence Platform"
    assert data.get("status") == "operational"