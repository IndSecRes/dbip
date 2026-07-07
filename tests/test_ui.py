"""
Tests for Dynamic UI
"""

import pytest
from src.ui import (
    SchemaRegistry,
    DashboardSchema,
    WidgetSchema,
    RenderEngine,
    ComponentRenderer,
    DashboardView,
    UIRouter
)


def test_schema_registry():
    """Test schema registry"""
    registry = SchemaRegistry()
    
    dashboard = DashboardSchema(
        dashboard_id="test_dashboard",
        title="Test Dashboard"
    )
    
    registry.register_dashboard(dashboard)
    assert registry.get_dashboard("test_dashboard") is not None
    assert len(registry.list_dashboards()) >= 1


def test_widget_schema():
    """Test widget schema"""
    widget = WidgetSchema(
        widget_id="test_widget",
        widget_type="card",
        title="Test Widget"
    )
    
    assert widget.widget_id == "test_widget"
    assert widget.widget_type == "card"
    assert widget.title == "Test Widget"


def test_dashboard_schema():
    """Test dashboard schema"""
    dashboard = DashboardSchema(
        dashboard_id="test_dashboard",
        title="Test Dashboard",
        description="A test dashboard"
    )
    
    assert dashboard.dashboard_id == "test_dashboard"
    assert dashboard.title == "Test Dashboard"
    assert dashboard.description == "A test dashboard"


def test_render_engine():
    """Test render engine"""
    engine = RenderEngine()
    
    dashboard = DashboardView.create_overview_dashboard()
    html = engine.render_dashboard(dashboard)
    
    assert "DBIP Overview" in html
    assert "System Status" in html


def test_component_renderer():
    """Test component renderer"""
    renderer = ComponentRenderer()
    
    from src.ui.components import CardComponent
    component = CardComponent(
        component_id="test_card",
        title="Test Card",
        content="Test content"
    )
    
    html = renderer.render(component)
    assert "Test Card" in html
    assert "Test content" in html


def test_ui_router():
    """Test UI router"""
    router = UIRouter()
    assert router.get_router() is not None