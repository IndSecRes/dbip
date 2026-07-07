"""
Pytest configuration for DBIP tests
"""

import pytest
import asyncio
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_telegram_data() -> Dict[str, Any]:
    """Sample Telegram signal data"""
    return {
        "source": "telegram",
        "username": "@test_user",
        "message": "ACME Corp is opening a new office in NYC",
        "timestamp": "2026-07-07T14:30:00Z",
        "chat_id": "123456789",
        "message_id": "987654321"
    }


@pytest.fixture
def sample_discord_data() -> Dict[str, Any]:
    """Sample Discord signal data"""
    return {
        "source": "discord",
        "username": "test_user#1234",
        "message": "Anyone know about ACME's NYC expansion?",
        "timestamp": "2026-07-07T14:35:00Z",
        "server_id": "123456789",
        "channel_id": "987654321"
    }


@pytest.fixture
def sample_twitter_data() -> Dict[str, Any]:
    """Sample Twitter signal data"""
    return {
        "source": "twitter",
        "username": "@test_user_nyc",
        "tweet": "Excited about ACME Corp's new NYC office!",
        "timestamp": "2026-07-07T14:40:00Z",
        "tweet_id": "1234567890123456789",
        "retweets": 10,
        "likes": 25
    }


@pytest.fixture
def sample_github_data() -> Dict[str, Any]:
    """Sample GitHub signal data"""
    return {
        "source": "github",
        "username": "testuser",
        "repository": "acme-corp",
        "commit": "Adding nyc office plans",
        "timestamp": "2026-07-07T14:45:00Z",
        "commit_hash": "abc123def456",
        "files": ["planning/nyc_office.md"]
    }


@pytest.fixture
def sample_reddit_data() -> Dict[str, Any]:
    """Sample Reddit signal data"""
    return {
        "source": "reddit",
        "username": "u/test_user_nyc",
        "subreddit": "r/nyc",
        "title": "ACME Corp opening office in NYC?",
        "post_id": "abc123",
        "timestamp": "2026-07-07T14:50:00Z",
        "comments": 5,
        "upvotes": 15
    }


@pytest.fixture
def sample_linkedin_data() -> Dict[str, Any]:
    """Sample LinkedIn signal data"""
    return {
        "source": "linkedin",
        "company": "ACME Corp",
        "job_posting": "NYC Office Manager",
        "location": "New York, NY",
        "timestamp": "2026-07-07T14:55:00Z",
        "job_id": "job_123456789",
        "posting_url": "https://linkedin.com/jobs/123456789"
    }


@pytest.fixture
def sample_multi_signals() -> Dict[str, Any]:
    """Combined signal data"""
    return {
        "signals": [
            {
                "source": "telegram",
                "username": "@test_user",
                "message": "ACME Corp is opening a new office in NYC",
                "timestamp": "2026-07-07T14:30:00Z"
            },
            {
                "source": "discord",
                "username": "test_user#1234",
                "message": "Anyone know about ACME's NYC expansion?",
                "timestamp": "2026-07-07T14:35:00Z"
            },
            {
                "source": "twitter",
                "username": "@test_user_nyc",
                "tweet": "Excited about ACME Corp's new NYC office!",
                "timestamp": "2026-07-07T14:40:00Z"
            }
        ]
    }


@pytest.fixture
def sample_entity() -> Dict[str, Any]:
    """Sample canonical entity"""
    return {
        "entity_id": "ENT_001",
        "entity_type": "person",
        "label": "John Doe",
        "description": "Individual identified through chatter analysis",
        "attributes": {
            "phone_numbers": ["+1-555-123-4567"],
            "emails": ["john.doe@email.com"],
            "social_media": {
                "telegram": "@johndoe",
                "twitter": "@johndoe_nyc"
            }
        },
        "domains": ["OSINT", "SOCMINT"],
        "confidence": 0.92,
        "provenance": [
            {
                "source": "telegram_api",
                "timestamp": "2026-07-07T14:30:00Z",
                "operation": "collection"
            }
        ]
    }


@pytest.fixture
def sample_relationship() -> Dict[str, Any]:
    """Sample relationship object"""
    return {
        "relationship_id": "REL_001",
        "source_entity": "ENT_001",
        "target_entity": "ENT_002",
        "type": "associated_with",
        "confidence": 0.85,
        "timestamp": "2026-07-07T14:30:00Z",
        "source_chain": ["telegram_api", "entity_resolver"],
        "evidence": [
            "Multiple sources confirm association"
        ]
    }


@pytest.fixture
def sample_intelligence_asset() -> Dict[str, Any]:
    """Sample intelligence asset"""
    return {
        "asset_id": "AST_001",
        "title": "John Doe - Complete Intelligence Profile",
        "asset_type": "identity_profile",
        "confidence_score": 0.92,
        "evidence_rating": "A",
        "content": {
            "identity": {
                "canonical_name": "John Doe",
                "aliases": ["J. Doe", "Johnathan Doe"],
                "location": "New York City, NY, USA"
            },
            "contact": {
                "phone_numbers": ["+1-555-123-4567"],
                "emails": ["john.doe@email.com"]
            },
            "social_media": {
                "telegram": "@johndoe",
                "twitter": "@johndoe_nyc"
            }
        },
        "provenance": [
            {
                "source": "telegram_api",
                "timestamp": "2026-07-07T14:30:00Z"
            },
            {
                "source": "entity_resolver",
                "timestamp": "2026-07-07T14:35:00Z"
            }
        ]
    }


@pytest.fixture
def app():
    """FastAPI test client"""
    from fastapi.testclient import TestClient
    from src.main import app
    return TestClient(app)