"""
Dashboard Generator
Generates dashboard configurations for Grafana
"""

from typing import Dict, Any, List


class DashboardGenerator:
    """
    Generates dashboard configurations
    """
    
    def generate_pipeline_dashboard(self) -> Dict[str, Any]:
        """Generate pipeline monitoring dashboard"""
        return {
            "title": "DBIP Pipeline Dashboard",
            "panels": [
                self._pipeline_health_panel(),
                self._pipeline_duration_panel(),
                self._assets_created_panel(),
                self._error_rate_panel()
            ]
        }
    
    def generate_system_dashboard(self) -> Dict[str, Any]:
        """Generate system monitoring dashboard"""
        return {
            "title": "DBIP System Dashboard",
            "panels": [
                self._cpu_usage_panel(),
                self._memory_usage_panel(),
                self._api_requests_panel(),
                self._database_connections_panel()
            ]
        }
    
    def generate_health_dashboard(self) -> Dict[str, Any]:
        """Generate health dashboard"""
        return {
            "title": "DBIP Health Dashboard",
            "panels": [
                self._health_status_panel(),
                self._service_status_panel(),
                self._recent_alerts_panel()
            ]
        }
    
    def _pipeline_health_panel(self) -> Dict[str, Any]:
        return {
            "title": "Pipeline Health",
            "type": "stat",
            "targets": [
                {"expr": "pipeline_runs_total{status='success'} / pipeline_runs_total * 100"}
            ]
        }
    
    def _pipeline_duration_panel(self) -> Dict[str, Any]:
        return {
            "title": "Pipeline Duration",
            "type": "graph",
            "targets": [
                {"expr": "histogram_quantile(0.95, pipeline_duration)"}
            ]
        }
    
    def _assets_created_panel(self) -> Dict[str, Any]:
        return {
            "title": "Assets Created",
            "type": "bargauge",
            "targets": [
                {"expr": "sum by (type) (assets_created_total)"}
            ]
        }
    
    def _error_rate_panel(self) -> Dict[str, Any]:
        return {
            "title": "Error Rate",
            "type": "graph",
            "targets": [
                {"expr": "rate(errors_total[5m])"}
            ]
        }
    
    def _cpu_usage_panel(self) -> Dict[str, Any]:
        return {
            "title": "CPU Usage",
            "type": "graph",
            "targets": [
                {"expr": "system_cpu_usage"}
            ]
        }
    
    def _memory_usage_panel(self) -> Dict[str, Any]:
        return {
            "title": "Memory Usage",
            "type": "graph",
            "targets": [
                {"expr": "system_memory_usage"}
            ]
        }
    
    def _api_requests_panel(self) -> Dict[str, Any]:
        return {
            "title": "API Requests",
            "type": "graph",
            "targets": [
                {"expr": "rate(api_requests_total[5m])"}
            ]
        }
    
    def _database_connections_panel(self) -> Dict[str, Any]:
        return {
            "title": "Database Connections",
            "type": "stat",
            "targets": [
                {"expr": "database_connections_active"}
            ]
        }
    
    def _health_status_panel(self) -> Dict[str, Any]:
        return {
            "title": "Health Status",
            "type": "stat",
            "targets": [
                {"expr": "health_status"}
            ]
        }
    
    def _service_status_panel(self) -> Dict[str, Any]:
        return {
            "title": "Service Status",
            "type": "table",
            "targets": [
                {"expr": "service_status"}
            ]
        }
    
    def _recent_alerts_panel(self) -> Dict[str, Any]:
        return {
            "title": "Recent Alerts",
            "type": "table",
            "targets": [
                {"expr": "alerts_total"}
            ]
        }