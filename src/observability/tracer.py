"""
Distributed Tracing
Provides tracing with spans and context propagation
"""

import time
import uuid
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from contextvars import ContextVar


# Context variable for trace propagation
_trace_context: ContextVar[Optional['TraceContext']] = ContextVar('trace_context', default=None)


@dataclass
class Span:
    """Represents a span in a trace"""
    name: str
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)
    
    def end(self) -> None:
        """End the span"""
        self.end_time = time.time()
    
    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Add an event to the span"""
        self.events.append({
            "name": name,
            "timestamp": time.time(),
            "attributes": attributes or {}
        })
    
    @property
    def duration(self) -> Optional[float]:
        """Get the duration of the span"""
        if self.end_time is not None:
            return self.end_time - self.start_time
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "attributes": self.attributes,
            "events": self.events
        }


@dataclass
class TraceContext:
    """Trace context for propagation"""
    trace_id: str
    spans: List[Span] = field(default_factory=list)
    
    def start_span(self, name: str) -> Span:
        """Start a new span in this trace"""
        span = Span(
            name=name,
            trace_id=self.trace_id,
            span_id=f"span_{uuid.uuid4().hex[:8]}",
            parent_span_id=self.spans[-1].span_id if self.spans else None
        )
        self.spans.append(span)
        return span
    
    def get_current_span(self) -> Optional[Span]:
        """Get the most recent span"""
        return self.spans[-1] if self.spans else None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "trace_id": self.trace_id,
            "spans": [s.to_dict() for s in self.spans]
        }


class Tracer:
    """
    Distributed tracer
    """
    
    def __init__(self, service_name: str = "dbip"):
        self.service_name = service_name
        self.traces: List[TraceContext] = []
    
    def start_trace(self, name: str) -> TraceContext:
        """Start a new trace"""
        trace_id = f"trace_{uuid.uuid4().hex[:8]}"
        context = TraceContext(trace_id=trace_id)
        self.traces.append(context)
        
        # Set as current context
        _trace_context.set(context)
        
        # Start root span
        context.start_span(name)
        
        return context
    
    def get_current_trace(self) -> Optional[TraceContext]:
        """Get the current trace context"""
        return _trace_context.get()
    
    def get_traces(self, limit: int = 100) -> List[TraceContext]:
        """Get stored traces"""
        return self.traces[-limit:]
    
    def clear(self) -> None:
        """Clear stored traces"""
        self.traces.clear()
    
    def get_trace_summary(self) -> Dict[str, Any]:
        """Get summary of traces"""
        if not self.traces:
            return {"total_traces": 0}
        
        total_spans = sum(len(t.spans) for t in self.traces)
        return {
            "total_traces": len(self.traces),
            "total_spans": total_spans,
            "avg_spans_per_trace": total_spans / len(self.traces)
        }


# Global tracer
_global_tracer: Optional[Tracer] = None


def get_tracer(service_name: str = "dbip") -> Tracer:
    """Get or create a tracer"""
    global _global_tracer
    if _global_tracer is None:
        _global_tracer = Tracer(service_name)
    return _global_tracer