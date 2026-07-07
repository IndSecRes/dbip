"""
Dynamic UI
Schema-driven user interface
"""

from .schemas import (
    SchemaRegistry,
    EntitySchema,
    DashboardSchema,
    WidgetSchema
)
from .renderer import RenderEngine, ComponentRenderer
from .views import (
    DashboardView,
    EntityView,
    KnowledgeGraphView,
    AgentView,
    FederationView
)
from .components import (
    Component,
    CardComponent,
    TableComponent,
    ChartComponent,
    GraphComponent,
    FormComponent
)
from .router import UIRouter

__all__ = [
    "SchemaRegistry",
    "EntitySchema",
    "DashboardSchema",
    "WidgetSchema",
    "RenderEngine",
    "ComponentRenderer",
    "DashboardView",
    "EntityView",
    "KnowledgeGraphView",
    "AgentView",
    "FederationView",
    "Component",
    "CardComponent",
    "TableComponent",
    "ChartComponent",
    "GraphComponent",
    "FormComponent",
    "UIRouter"
]   