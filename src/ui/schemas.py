"""
UI Schemas
Defines the schemas for UI rendering
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class WidgetSchema:
    """Schema for a UI widget"""
    widget_id: str
    widget_type: str  # card, table, chart, graph, form
    title: str
    description: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)
    data_source: Optional[str] = None
    query: Optional[Dict[str, Any]] = None
    position: Dict[str, Any] = field(default_factory=lambda: {"x": 0, "y": 0, "w": 1, "h": 1})


@dataclass
class DashboardSchema:
    """Schema for a dashboard"""
    dashboard_id: str
    title: str
    description: Optional[str] = None
    widgets: List[WidgetSchema] = field(default_factory=list)
    layout: str = "grid"  # grid, flex, columns
    theme: str = "light"
    refresh_interval: int = 60
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class EntitySchema:
    """Schema for entity display"""
    entity_id: str
    entity_type: str
    display_fields: List[Dict[str, Any]] = field(default_factory=list)
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    views: Dict[str, Any] = field(default_factory=dict)


class SchemaRegistry:
    """
    Registry of UI schemas
    """
    
    def __init__(self):
        self.dashboards: Dict[str, DashboardSchema] = {}
        self.widgets: Dict[str, WidgetSchema] = {}
        self.entities: Dict[str, EntitySchema] = {}
    
    def register_dashboard(self, dashboard: DashboardSchema) -> None:
        """Register a dashboard schema"""
        self.dashboards[dashboard.dashboard_id] = dashboard
    
    def register_widget(self, widget: WidgetSchema) -> None:
        """Register a widget schema"""
        self.widgets[widget.widget_id] = widget
    
    def register_entity(self, entity: EntitySchema) -> None:
        """Register an entity schema"""
        self.entities[entity.entity_id] = entity
    
    def get_dashboard(self, dashboard_id: str) -> Optional[DashboardSchema]:
        """Get a dashboard schema"""
        return self.dashboards.get(dashboard_id)
    
    def get_widget(self, widget_id: str) -> Optional[WidgetSchema]:
        """Get a widget schema"""
        return self.widgets.get(widget_id)
    
    def get_entity(self, entity_id: str) -> Optional[EntitySchema]:
        """Get an entity schema"""
        return self.entities.get(entity_id)
    
    def list_dashboards(self) -> List[Dict[str, Any]]:
        """List all dashboards"""
        return [
            {
                "id": d.dashboard_id,
                "title": d.title,
                "description": d.description,
                "widget_count": len(d.widgets)
            }
            for d in self.dashboards.values()
        ]
    
    def to_json(self) -> str:
        """Serialize schemas to JSON"""
        return json.dumps({
            "dashboards": [
                {
                    "id": d.dashboard_id,
                    "title": d.title,
                    "description": d.description,
                    "widgets": [
                        {
                            "id": w.widget_id,
                            "type": w.widget_type,
                            "title": w.title,
                            "config": w.config
                        }
                        for w in d.widgets
                    ]
                }
                for d in self.dashboards.values()
            ],
            "widgets": [
                {
                    "id": w.widget_id,
                    "type": w.widget_type,
                    "title": w.title,
                    "config": w.config
                }
                for w in self.widgets.values()
            ],
            "entities": list(self.entities.keys())
        })