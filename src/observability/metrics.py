"""
Metrics Collection
Collects and exposes metrics using Prometheus
"""

import time
from typing import Dict, Any, Optional, List
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
import threading


@dataclass
class Metric:
    """Base metric"""
    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class MetricsRegistry:
    """In-memory metrics registry"""
    
    def __init__(self):
        self.metrics: Dict[str, List[Metric]] = defaultdict(list)
        self.counter_metrics: Dict[str, int] = defaultdict(int)
        self.gauge_metrics: Dict[str, float] = defaultdict(float)
        self.histogram_metrics: Dict[str, List[float]] = defaultdict(list)
    
    def counter(self, name: str, value: int = 1, labels: Optional[Dict[str, str]] = None) -> int:
        """Increment a counter metric"""
        key = self._build_key(name, labels or {})
        self.counter_metrics[key] += value
        return self.counter_metrics[key]
    
    def gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> float:
        """Set a gauge metric"""
        key = self._build_key(name, labels or {})
        self.gauge_metrics[key] = value
        return value
    
    def histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Record a histogram metric"""
        key = self._build_key(name, labels or {})
        self.histogram_metrics[key].append(value)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics"""
        return {
            "counters": dict(self.counter_metrics),
            "gauges": dict(self.gauge_metrics),
            "histograms": {k: {"values": v, "count": len(v), "sum": sum(v), "avg": sum(v)/len(v) if v else 0} 
                          for k, v in self.histogram_metrics.items()}
        }
    
    def clear(self):
        """Clear all metrics"""
        self.counter_metrics.clear()
        self.gauge_metrics.clear()
        self.histogram_metrics.clear()
    
    def _build_key(self, name: str, labels: Dict[str, str]) -> str:
        """Build a key from name and labels"""
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}" if label_str else name


class MetricsCollector:
    """
    Collects and exposes metrics
    """
    
    def __init__(self):
        self.registry = MetricsRegistry()
        self.pipeline_metrics = {
            "requests_total": 0,
            "requests_failed": 0,
            "processing_time": [],
            "assets_created": 0
        }
    
    def record_request(self, endpoint: str, duration: float) -> None:
        """Record an API request"""
        self.registry.counter(f"api_requests_total", labels={"endpoint": endpoint})
        self.registry.histogram(f"api_request_duration", duration, labels={"endpoint": endpoint})
    
    def record_pipeline_run(self, stages_completed: int, duration: float, success: bool) -> None:
        """Record a pipeline run"""
        status = "success" if success else "failed"
        self.registry.counter(f"pipeline_runs_total", labels={"status": status})
        self.registry.gauge(f"pipeline_stages_completed", stages_completed)
        self.registry.histogram(f"pipeline_duration", duration, labels={"status": status})
        
        if success:
            self.pipeline_metrics["assets_created"] += 1
    
    def record_asset_created(self, asset_type: str, confidence_rating: str) -> None:
        """Record asset creation"""
        self.registry.counter(f"assets_created_total", labels={"type": asset_type, "rating": confidence_rating})
    
    def record_error(self, error_type: str, component: str) -> None:
        """Record an error"""
        self.registry.counter(f"errors_total", labels={"type": error_type, "component": component})
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics"""
        return {
            "registry": self.registry.get_metrics(),
            "pipeline": self.pipeline_metrics,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_formatted_metrics(self) -> str:
        """Get metrics in Prometheus format"""
        metrics = self.registry.get_metrics()
        output = []
        
        # Counter metrics
        for key, value in metrics.get("counters", {}).items():
            output.append(f"# HELP {key} Counter metric")
            output.append(f"# TYPE {key} counter")
            output.append(f"{key} {value}")
        
        # Gauge metrics
        for key, value in metrics.get("gauges", {}).items():
            output.append(f"# HELP {key} Gauge metric")
            output.append(f"# TYPE {key} gauge")
            output.append(f"{key} {value}")
        
        # Histogram metrics
        for key, data in metrics.get("histograms", {}).items():
            output.append(f"# HELP {key} Histogram metric")
            output.append(f"# TYPE {key} histogram")
            for i, v in enumerate(data.get("values", [])[:100]):  # Limit to 100 samples
                output.append(f"{key} {{quantile=\"0.{i}\"}} {v}")
            output.append(f"{key}_count {data.get('count', 0)}")
            output.append(f"{key}_sum {data.get('sum', 0)}")
        
        return "\n".join(output)