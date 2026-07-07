"""
Tests for configuration loading
"""

import pytest
from pathlib import Path
import yaml

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.config import ConfigLoader, config_loader, config


def test_config_loaded():
    """Test that configuration loaded successfully"""
    assert config is not None
    assert isinstance(config, dict)


def test_environment():
    """Test environment is correctly set"""
    assert config_loader.env in ["development", "staging", "production"]


def test_app_config():
    """Test app configuration"""
    assert config.get("app", {}).get("name") == "DBIP - Data Brokerage & Intelligence Platform"
    assert config.get("app", {}).get("version") == "6.0.0"


def test_pipeline_config():
    """Test pipeline configuration"""
    pipeline = config.get("pipeline", {})
    assert pipeline.get("fusion_threshold") == 0.75
    assert pipeline.get("default_confidence") == 0.5
    assert pipeline.get("retry_attempts") == 3


def test_entity_types():
    """Test entity types configuration"""
    entity_types = config.get("entity_types", [])
    assert "person" in entity_types
    assert "organization" in entity_types
    assert "domain" in entity_types
    assert len(entity_types) > 0


def test_relationship_types():
    """Test relationship types configuration"""
    relationship_types = config.get("relationship_types", [])
    assert "owns" in relationship_types
    assert "controls" in relationship_types
    assert "associated_with" in relationship_types
    assert len(relationship_types) > 0


def test_domains():
    """Test domains configuration"""
    domains = config.get("domains", [])
    assert "OSINT" in domains
    assert "CYBINT" in domains
    assert "FININT" in domains
    assert len(domains) > 0


def test_database_config():
    """Test database configuration structure"""
    database = config.get("database", {})
    assert "postgres" in database
    assert "redis" in database
    assert "neo4j" in database


def test_features_config():
    """Test features configuration"""
    features = config.get("features", {})
    assert "mdips_compliance" in features
    assert "multi_dimensional_confidence" in features
    assert "identity_resolution" in features


def test_config_override():
    """Test environment-specific override works"""
    # Development should have debug: true
    if config_loader.env == "development":
        debug_value = config_loader.get("server.debug")
        assert debug_value is True, f"Expected True, got {debug_value}"


def test_config_get_method():
    """Test the get method with dot notation"""
    app_name = config_loader.get("app.name")
    assert app_name == "DBIP - Data Brokerage & Intelligence Platform"
    
    fusion = config_loader.get("pipeline.fusion_threshold")
    assert fusion == 0.75


def test_config_get_default():
    """Test get method with default value"""
    missing = config_loader.get("nonexistent.key", "default")
    assert missing == "default"