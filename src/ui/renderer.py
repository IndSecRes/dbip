"""
UI Renderer
Renders UI components from schemas
"""

from typing import Dict, Any, List, Optional
from jinja2 import Template
import json

from src.ui.schemas import DashboardSchema, WidgetSchema
from src.ui.components import (
    Component,
    CardComponent,
    TableComponent,
    ChartComponent,
    GraphComponent,
    FormComponent
)


class ComponentRenderer:
    """
    Renders individual components
    """
    
    def render(self, component: Component) -> str:
        """Render a component to HTML"""
        if component.component_type == "card":
            return self._render_card(component)
        elif component.component_type == "table":
            return self._render_table(component)
        elif component.component_type == "chart":
            return self._render_chart(component)
        elif component.component_type == "graph":
            return self._render_graph(component)
        elif component.component_type == "form":
            return self._render_form(component)
        else:
            return self._render_generic(component)
    
    def _render_card(self, component: Component) -> str:
        """Render a card component"""
        props = component.props
        return f"""
        <div class="card" style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 8px;">
            {f'<h3>{props.get("title", "")}</h3>' if props.get("title") else ''}
            {f'<p>{props.get("content", "")}</p>' if props.get("content") else ''}
            {f'<div class="card-footer">{props.get("footer", "")}</div>' if props.get("footer") else ''}
        </div>
        """
    
    def _render_table(self, component: Component) -> str:
        """Render a table component"""
        props = component.props
        columns = props.get("columns", [])
        data = props.get("data", [])
        
        html = '<table style="width: 100%; border-collapse: collapse;">'
        html += '<thead><tr>'
        for col in columns:
            html += f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{col.get("title", "")}</th>'
        html += '</tr></thead><tbody>'
        
        for row in data:
            html += '<tr>'
            for col in columns:
                key = col.get("key", "")
                value = row.get(key, "")
                html += f'<td style="border: 1px solid #ddd; padding: 8px;">{value}</td>'
            html += '</tr>'
        
        html += '</tbody></table>'
        return html
    
    def _render_chart(self, component: Component) -> str:
        """Render a chart component"""
        props = component.props
        chart_type = props.get("chart_type", "bar")
        data = props.get("data", {})
        
        return f"""
        <div class="chart" data-type="{chart_type}" data-data='{json.dumps(data)}'>
            <div class="chart-placeholder" style="height: 300px; background: #f5f5f5; display: flex; align-items: center; justify-content: center; border-radius: 4px;">
                <span>Chart: {chart_type}</span>
            </div>
        </div>
        """
    
    def _render_graph(self, component: Component) -> str:
        """Render a graph component"""
        props = component.props
        nodes = props.get("nodes", [])
        edges = props.get("edges", [])
        
        return f"""
        <div class="graph" data-nodes='{json.dumps(nodes)}' data-edges='{json.dumps(edges)}'>
            <div class="graph-placeholder" style="height: 400px; background: #f5f5f5; display: flex; align-items: center; justify-content: center; border-radius: 4px;">
                <span>Graph: {len(nodes)} nodes, {len(edges)} edges</span>
            </div>
        </div>
        """
    
    def _render_form(self, component: Component) -> str:
        """Render a form component"""
        props = component.props
        fields = props.get("fields", [])
        
        html = f'<form method="{props.get("method", "POST")}" action="{props.get("submit_url", "#")}">'
        for field in fields:
            field_type = field.get("type", "text")
            field_name = field.get("name", "")
            field_label = field.get("label", field_name)
            field_value = field.get("value", "")
            required = "required" if field.get("required", False) else ""
            
            html += f"""
            <div style="margin: 8px 0;">
                <label style="display: block; margin-bottom: 4px;">{field_label}</label>
                <input type="{field_type}" name="{field_name}" value="{field_value}" {required} style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
            </div>
            """
        
        html += '<button type="submit" style="padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">Submit</button>'
        html += '</form>'
        return html
    
    def _render_generic(self, component: Component) -> str:
        """Render a generic component"""
        return f"""
        <div class="component" data-type="{component.component_type}">
            <pre>{json.dumps(component.props, indent=2)}</pre>
        </div>
        """


class RenderEngine:
    """
    Main rendering engine
    """
    
    def __init__(self):
        self.renderer = ComponentRenderer()
        self.template = self._get_template()
    
    def _get_template(self) -> str:
        """Get the base HTML template"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{{ title }}</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: #f8f9fa;
                    color: #212529;
                }
                .dashboard {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                .dashboard-header {
                    padding: 20px 0;
                    border-bottom: 1px solid #dee2e6;
                    margin-bottom: 20px;
                }
                .dashboard-title {
                    font-size: 24px;
                    font-weight: 600;
                    margin: 0;
                }
                .dashboard-description {
                    color: #6c757d;
                    margin: 8px 0 0 0;
                }
                .dashboard-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: 16px;
                }
                .dashboard-widget {
                    background: white;
                    border-radius: 8px;
                    padding: 16px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                }
                .widget-title {
                    font-size: 16px;
                    font-weight: 500;
                    margin: 0 0 12px 0;
                    color: #495057;
                }
                .refresh-info {
                    text-align: center;
                    padding: 20px;
                    color: #6c757d;
                    font-size: 14px;
                    border-top: 1px solid #dee2e6;
                    margin-top: 20px;
                }
                @media (max-width: 600px) {
                    .dashboard-grid {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <div class="dashboard">
                <div class="dashboard-header">
                    <h1 class="dashboard-title">{{ title }}</h1>
                    {% if description %}
                    <p class="dashboard-description">{{ description }}</p>
                    {% endif %}
                </div>
                <div class="dashboard-grid">
                    {% for widget in widgets %}
                    <div class="dashboard-widget">
                        <div class="widget-title">{{ widget.title }}</div>
                        {{ widget.html }}
                    </div>
                    {% endfor %}
                </div>
                <div class="refresh-info">
                    Updated: {{ timestamp }} | Auto-refresh: {{ refresh_interval }}s
                </div>
            </div>
            <script>
                // Auto-refresh
                let interval = {{ refresh_interval }} * 1000;
                if (interval > 0) {
                    setTimeout(() => location.reload(), interval);
                }
            </script>
        </body>
        </html>
        """
    
    def render_dashboard(self, dashboard: DashboardSchema) -> str:
        """Render a dashboard"""
        # Render each widget
        widgets_html = []
        for widget in dashboard.widgets:
            component = self._widget_to_component(widget)
            html = self.renderer.render(component)
            widgets_html.append({
                "title": widget.title,
                "html": html
            })
        
        # Render the template
        template = Template(self.template)
        return template.render(
            title=dashboard.title,
            description=dashboard.description,
            widgets=widgets_html,
            refresh_interval=dashboard.refresh_interval,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def _widget_to_component(self, widget: WidgetSchema) -> Component:
        """Convert a widget to a component"""
        config = widget.config
        
        if widget.widget_type == "card":
            return CardComponent(
                component_id=widget.widget_id,
                title=config.get("title", ""),
                content=config.get("content", ""),
                icon=config.get("icon"),
                footer=config.get("footer")
            )
        elif widget.widget_type == "table":
            return TableComponent(
                component_id=widget.widget_id,
                columns=config.get("columns", []),
                data=config.get("data", [])
            )
        elif widget.widget_type == "chart":
            return ChartComponent(
                component_id=widget.widget_id,
                chart_type=config.get("chart_type", "bar"),
                data=config.get("data", {}),
                options=config.get("options")
            )
        elif widget.widget_type == "graph":
            return GraphComponent(
                component_id=widget.widget_id,
                nodes=config.get("nodes", []),
                edges=config.get("edges", [])
            )
        elif widget.widget_type == "form":
            return FormComponent(
                component_id=widget.widget_id,
                fields=config.get("fields", []),
                submit_url=config.get("submit_url", "#"),
                method=config.get("method", "POST")
            )
        else:
            return Component(
                component_id=widget.widget_id,
                component_type="generic",
                props=config
            )


from datetime import datetime