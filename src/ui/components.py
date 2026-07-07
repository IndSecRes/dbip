"""
UI Components
Reusable UI components
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class Component:
    """Base UI component"""
    component_id: str
    component_type: str
    props: Dict[str, Any] = field(default_factory=dict)
    children: List['Component'] = field(default_factory=list)
    styles: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CardComponent(Component):
    """Card component"""
    def __init__(self, component_id: str, title: str, content: str, icon: Optional[str] = None, footer: Optional[str] = None):
        super().__init__(
            component_id=component_id,
            component_type="card",
            props={
                "title": title,
                "content": content,
                "icon": icon,
                "footer": footer
            }
        )


@dataclass
class TableComponent(Component):
    """Table component"""
    def __init__(self, component_id: str, columns: List[Dict[str, Any]], data: List[Dict[str, Any]]):
        super().__init__(
            component_id=component_id,
            component_type="table",
            props={
                "columns": columns,
                "data": data
            }
        )


@dataclass
class ChartComponent(Component):
    """Chart component"""
    def __init__(self, component_id: str, chart_type: str, data: Dict[str, Any], options: Optional[Dict[str, Any]] = None):
        super().__init__(
            component_id=component_id,
            component_type="chart",
            props={
                "chart_type": chart_type,
                "data": data,
                "options": options or {}
            }
        )


@dataclass
class GraphComponent(Component):
    """Graph visualization component"""
    def __init__(self, component_id: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]):
        super().__init__(
            component_id=component_id,
            component_type="graph",
            props={
                "nodes": nodes,
                "edges": edges
            }
        )


@dataclass
class FormComponent(Component):
    """Form component"""
    def __init__(self, component_id: str, fields: List[Dict[str, Any]], submit_url: str, method: str = "POST"):
        super().__init__(
            component_id=component_id,
            component_type="form",
            props={
                "fields": fields,
                "submit_url": submit_url,
                "method": method
            }
        )