"""
Agent Memory
Stores and retrieves agent context and history
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class MemoryEntry:
    """A single memory entry"""
    key: str
    value: Any
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentMemory:
    """
    Memory system for agents
    """
    
    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self.short_term: Dict[str, Any] = {}
        self.long_term: List[MemoryEntry] = []
        self.episodic: List[MemoryEntry] = []
    
    def store(self, key: str, value: Any, memory_type: str = "short_term") -> None:
        """Store a memory"""
        entry = MemoryEntry(key=key, value=value)
        
        if memory_type == "short_term":
            self.short_term[key] = value
        elif memory_type == "long_term":
            self.long_term.append(entry)
            if len(self.long_term) > self.max_entries:
                self.long_term = self.long_term[-self.max_entries:]
        elif memory_type == "episodic":
            self.episodic.append(entry)
            if len(self.episodic) > self.max_entries:
                self.episodic = self.episodic[-self.max_entries:]
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a short-term memory"""
        return self.short_term.get(key)
    
    def retrieve_long_term(self, key: str) -> List[Any]:
        """Retrieve long-term memories by key"""
        return [e.value for e in self.long_term if e.key == key]
    
    def retrieve_episodic(self, key: str) -> List[Any]:
        """Retrieve episodic memories by key"""
        return [e.value for e in self.episodic if e.key == key]
    
    def clear_short_term(self) -> None:
        """Clear short-term memory"""
        self.short_term.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "short_term_entries": len(self.short_term),
            "long_term_entries": len(self.long_term),
            "episodic_entries": len(self.episodic)
        }
    
    def to_json(self) -> str:
        """Serialize memory to JSON"""
        return json.dumps({
            "short_term": self.short_term,
            "long_term": [(e.key, e.value, e.timestamp.isoformat()) for e in self.long_term],
            "episodic": [(e.key, e.value, e.timestamp.isoformat()) for e in self.episodic]
        })