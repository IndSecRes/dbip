"""
UI Router
Routes UI requests to appropriate views
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from src.ui.views import (
    DashboardView,
    EntityView,
    KnowledgeGraphView,
    AgentView,
    FederationView
)
from src.ui.schemas import SchemaRegistry
from src.ui.renderer import RenderEngine
from src.ui.components import CardComponent, TableComponent


class UIRouter:
    """
    Routes UI requests
    """
    
    def __init__(self):
        self.router = APIRouter(prefix="/ui", tags=["UI"])
        self.schema_registry = SchemaRegistry()
        self.render_engine = RenderEngine()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup UI routes"""
        
        @self.router.get("/", response_class=HTMLResponse)
        async def home():
            return self.render_dashboard("overview")
        
        @self.router.get("/dashboard/{dashboard_id}", response_class=HTMLResponse)
        async def get_dashboard(dashboard_id: str):
            return self.render_dashboard(dashboard_id)
        
        @self.router.get("/entity/{entity_id}", response_class=HTMLResponse)
        async def get_entity(entity_id: str):
            return self.render_entity(entity_id)
        
        @self.router.get("/graph", response_class=HTMLResponse)
        async def get_graph():
            return self.render_graph()
        
        @self.router.get("/agents", response_class=HTMLResponse)
        async def get_agents():
            return self.render_agents()
        
        @self.router.get("/federation", response_class=HTMLResponse)
        async def get_federation():
            return self.render_federation()
    
    def render_dashboard(self, dashboard_id: str) -> str:
        """Render a dashboard"""
        # Get dashboard schema
        dashboard = self.schema_registry.get_dashboard(dashboard_id)
        
        if not dashboard:
            # Return a default dashboard if not found
            dashboard = DashboardView.create_overview_dashboard()
        
        return self.render_engine.render_dashboard(dashboard)
    
    def render_entity(self, entity_id: str) -> str:
        """Render an entity"""
        # Placeholder entity data
        entity_data = {
            "id": entity_id,
            "label": "John Doe",
            "type": "Person",
            "confidence": 0.92,
            "attributes": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-123-4567"
            }
        }
        return EntityView.render_entity(entity_data)
    
    def render_graph(self) -> str:
        """Render the knowledge graph"""
        nodes = [
            {"id": "1", "label": "Person"},
            {"id": "2", "label": "Organization"},
            {"id": "3", "label": "Location"}
        ]
        edges = [
            {"source": "1", "target": "2", "label": "works_for"},
            {"source": "2", "target": "3", "label": "located_in"}
        ]
        return KnowledgeGraphView.render_graph(nodes, edges)
    
    def render_agents(self) -> str:
        """Render agent status"""
        agents = [
            {
                "name": "Collection Agent",
                "status": "active",
                "tasks": 125,
                "last_active": "2026-07-07 14:30:00"
            },
            {
                "name": "Analysis Agent",
                "status": "active",
                "tasks": 89,
                "last_active": "2026-07-07 14:28:00"
            },
            {
                "name": "Alert Agent",
                "status": "idle",
                "tasks": 12,
                "last_active": "2026-07-07 14:00:00"
            }
        ]
        return AgentView.render_agent_status(agents)
    
    def render_federation(self) -> str:
        """Render federation status"""
        nodes = [
            {
                "name": "Node A - Cyber",
                "status": "active",
                "capabilities": ["entity_sharing", "query"],
                "last_seen": "2026-07-07 14:30:00"
            },
            {
                "name": "Node B - Financial",
                "status": "active",
                "capabilities": ["entity_sharing", "sync"],
                "last_seen": "2026-07-07 14:25:00"
            }
        ]
        return FederationView.render_federation_status(nodes)
    
    def register_dashboard(self, dashboard_id: str, dashboard):
        """Register a dashboard with the UI"""
        self.schema_registry.register_dashboard(dashboard)
    
    def get_router(self):
        """Get the FastAPI router"""
        return self.router