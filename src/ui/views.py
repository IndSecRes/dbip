"""
UI Views
Pre-defined views for the UI
"""
from src.ui.schemas import DashboardSchema, WidgetSchema
from typing import Dict, Any, List
from datetime import datetime

from src.ui.schemas import DashboardSchema, WidgetSchema
from src.ui.renderer import RenderEngine


class DashboardView:
    """Dashboard view"""
    
    @staticmethod
    def create_overview_dashboard() -> DashboardSchema:
        """Create an overview dashboard"""
        return DashboardSchema(
            dashboard_id="overview",
            title="DBIP Overview",
            description="Intelligence Platform Overview Dashboard",
            widgets=[
                WidgetSchema(
                    widget_id="stats_card",
                    widget_type="card",
                    title="System Status",
                    config={
                        "title": "System Status",
                        "content": "✅ All systems operational",
                        "footer": "Last checked: Now"
                    }
                ),
                WidgetSchema(
                    widget_id="entities_table",
                    widget_type="table",
                    title="Recent Entities",
                    config={
                        "columns": [
                            {"key": "id", "title": "ID"},
                            {"key": "type", "title": "Type"},
                            {"key": "label", "title": "Label"},
                            {"key": "confidence", "title": "Confidence"}
                        ],
                        "data": [
                            {"id": "ENT_001", "type": "Person", "label": "John Doe", "confidence": 0.92},
                            {"id": "ENT_002", "type": "Organization", "label": "ACME Corp", "confidence": 0.85},
                            {"id": "ENT_003", "type": "Location", "label": "New York", "confidence": 0.78}
                        ]
                    }
                )
            ],
            refresh_interval=30
        )
    
    @staticmethod
    def create_entity_dashboard() -> DashboardSchema:
        """Create an entity dashboard"""
        return DashboardSchema(
            dashboard_id="entities",
            title="Entity Dashboard",
            description="Entity Intelligence and Tracking",
            widgets=[
                WidgetSchema(
                    widget_id="entity_stats",
                    widget_type="card",
                    title="Entity Statistics",
                    config={
                        "title": "Entity Statistics",
                        "content": "Total Entities: 1,234 | Active: 89 | New: 12",
                        "footer": "Updated: Now"
                    }
                ),
                WidgetSchema(
                    widget_id="entity_graph",
                    widget_type="graph",
                    title="Entity Relationship Graph",
                    config={
                        "nodes": [
                            {"id": "1", "label": "Person", "color": "#ff6b6b"},
                            {"id": "2", "label": "Organization", "color": "#4ecdc4"},
                            {"id": "3", "label": "Location", "color": "#45b7d1"}
                        ],
                        "edges": [
                            {"source": "1", "target": "2", "label": "works_for"},
                            {"source": "2", "target": "3", "label": "located_in"}
                        ]
                    }
                )
            ],
            refresh_interval=60
        )
    
    @staticmethod
    def create_analytics_dashboard() -> DashboardSchema:
        """Create an analytics dashboard"""
        return DashboardSchema(
            dashboard_id="analytics",
            title="Analytics Dashboard",
            description="Intelligence Analytics and Insights",
            widgets=[
                WidgetSchema(
                    widget_id="confidence_chart",
                    widget_type="chart",
                    title="Confidence Distribution",
                    config={
                        "chart_type": "bar",
                        "data": {
                            "labels": ["A", "B", "C", "D"],
                            "values": [25, 35, 30, 10]
                        }
                    }
                ),
                WidgetSchema(
                    widget_id="source_table",
                    widget_type="table",
                    title="Top Sources",
                    config={
                        "columns": [
                            {"key": "source", "title": "Source"},
                            {"key": "signals", "title": "Signals"},
                            {"key": "confidence", "title": "Avg Confidence"}
                        ],
                        "data": [
                            {"source": "Telegram", "signals": 1250, "confidence": 0.88},
                            {"source": "Discord", "signals": 890, "confidence": 0.84},
                            {"source": "Twitter", "signals": 670, "confidence": 0.82}
                        ]
                    }
                )
            ],
            refresh_interval=60
        )
    
    @staticmethod
    def create_search_view() -> DashboardSchema:
        """Create a search view"""
        return DashboardSchema(
            dashboard_id="search",
            title="Search Intelligence",
            description="Search across intelligence assets",
            widgets=[
                WidgetSchema(
                    widget_id="search_form",
                    widget_type="form",
                    title="Search",
                    config={
                        "fields": [
                            {"name": "query", "label": "Search Query", "type": "text", "required": True},
                            {"name": "type", "label": "Type", "type": "select", "options": ["All", "Entity", "Asset", "Signal"]}
                        ],
                        "submit_url": "/api/v1/search",
                        "method": "GET"
                    }
                ),
                WidgetSchema(
                    widget_id="results_table",
                    widget_type="table",
                    title="Results",
                    config={
                        "columns": [
                            {"key": "title", "title": "Title"},
                            {"key": "type", "title": "Type"},
                            {"key": "score", "title": "Relevance Score"}
                        ],
                        "data": [
                            {"title": "ACME Corp Expansion", "type": "Asset", "score": 0.95},
                            {"title": "John Doe Profile", "type": "Entity", "score": 0.89}
                        ]
                    }
                )
            ],
            refresh_interval=0
        )


class EntityView:
    """Entity detail view"""
    
    @staticmethod
    def render_entity(entity_data: Dict[str, Any]) -> str:
        """Render an entity detail view"""
        # This would render a detailed entity page
        return f"""
        <div class="entity-view">
            <h1>{entity_data.get('label', 'Entity')}</h1>
            <p>Type: {entity_data.get('type', 'Unknown')}</p>
            <p>Confidence: {entity_data.get('confidence', 0)}</p>
            <h3>Attributes</h3>
            <ul>
                {''.join(f'<li>{k}: {v}</li>' for k, v in entity_data.get('attributes', {}).items())}
            </ul>
        </div>
        """


class KnowledgeGraphView:
    """Knowledge graph view"""
    
    @staticmethod
    def render_graph(nodes: List[Dict], edges: List[Dict]) -> str:
        """Render a knowledge graph view"""
        return f"""
        <div class="graph-view">
            <h2>Knowledge Graph</h2>
            <div class="graph-container" style="height: 500px;">
                <p>Nodes: {len(nodes)} | Edges: {len(edges)}</p>
                <!-- Graph visualization would go here -->
            </div>
        </div>
        """


class AgentView:
    """Agent monitoring view"""
    
    @staticmethod
    def render_agent_status(agents: List[Dict]) -> str:
        """Render agent status view"""
        return f"""
        <div class="agent-view">
            <h2>Agent Status</h2>
            <table>
                <thead>
                    <tr>
                        <th>Agent</th>
                        <th>Status</th>
                        <th>Tasks</th>
                        <th>Last Active</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f'''
                    <tr>
                        <td>{agent.get('name', 'Unknown')}</td>
                        <td>{agent.get('status', 'Unknown')}</td>
                        <td>{agent.get('tasks', 0)}</td>
                        <td>{agent.get('last_active', 'Never')}</td>
                    </tr>
                    ''' for agent in agents)}
                </tbody>
            </table>
        </div>
        """


class FederationView:
    """Federation view"""
    
    @staticmethod
    def render_federation_status(nodes: List[Dict]) -> str:
        """Render federation status view"""
        return f"""
        <div class="federation-view">
            <h2>Federation Status</h2>
            <table>
                <thead>
                    <tr>
                        <th>Node</th>
                        <th>Status</th>
                        <th>Capabilities</th>
                        <th>Last Seen</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f'''
                    <tr>
                        <td>{node.get('name', 'Unknown')}</td>
                        <td>{node.get('status', 'Unknown')}</td>
                        <td>{', '.join(node.get('capabilities', []))}</td>
                        <td>{node.get('last_seen', 'Never')}</td>
                    </tr>
                    ''' for node in nodes)}
                </tbody>
            </table>
        </div>
        """
class SearchView:
    """Search view"""
    
    @staticmethod
    def create_search_dashboard() -> DashboardSchema:
        """Create a search dashboard"""
        return DashboardSchema(
            dashboard_id="search",
            title="Search Intelligence",
            description="Search across intelligence assets",
            widgets=[
                WidgetSchema(
                    widget_id="search_form",
                    widget_type="form",
                    title="Search",
                    config={
                        "fields": [
                            {"name": "query", "label": "Search Query", "type": "text", "required": True},
                            {"name": "type", "label": "Type", "type": "select", "options": ["All", "Entity", "Asset", "Signal"]}
                        ],
                        "submit_url": "/api/v1/search",
                        "method": "GET"
                    }
                ),
                WidgetSchema(
                    widget_id="results_table",
                    widget_type="table",
                    title="Results",
                    config={
                        "columns": [
                            {"key": "title", "title": "Title"},
                            {"key": "type", "title": "Type"},
                            {"key": "score", "title": "Relevance Score"}
                        ],
                        "data": [
                            {"title": "ACME Corp Expansion", "type": "Asset", "score": 0.95},
                            {"title": "John Doe Profile", "type": "Entity", "score": 0.89}
                        ]
                    }
                )
            ],
            refresh_interval=0
        )
    
    @staticmethod
    def render_search_results(results: List[Dict[str, Any]]) -> str:
        """Render search results"""
        return f"""
        <div class="search-results">
            <h3>Search Results ({len(results)} found)</h3>
            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Type</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f'''
                    <tr>
                        <td>{r.get('title', 'Unknown')}</td>
                        <td>{r.get('type', 'Unknown')}</td>
                        <td>{r.get('score', 0)}</td>
                    </tr>
                    ''' for r in results)}
                </tbody>
            </table>
        </div>
        """