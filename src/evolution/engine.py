"""
Evolution Engine
Self-improving system that learns from data and feedback
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

from src.evolution.patterns import PatternDiscovery
from src.evolution.taxonomy import TaxonomyManager
from src.evolution.feedback import FeedbackSystem


class EvolutionEngine:
    """
    Self-improving intelligence engine
    """
    
    def __init__(self):
        self.pattern_discovery = PatternDiscovery()
        self.taxonomy_manager = TaxonomyManager()
        self.feedback_system = FeedbackSystem()
        self.evolution_history: List[Dict[str, Any]] = []
        self.running = False
    
    async def evolve(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the evolution process on data
        
        Args:
            data: Data containing entities, timestamps, categories
            
        Returns:
            Evolution results
        """
        evolution_results = {
            "timestamp": datetime.now().isoformat(),
            "patterns": {},
            "proposals": {},
            "feedback": {},
            "changes": []
        }
        
        # 1. Discover patterns
        patterns = await self._discover_patterns(data)
        evolution_results["patterns"] = patterns
        
        # 2. Generate proposals
        proposals = await self._generate_proposals(patterns)
        evolution_results["proposals"] = proposals
        
        # 3. Analyze feedback
        feedback_analysis = await self._analyze_feedback()
        evolution_results["feedback"] = feedback_analysis
        
        # 4. Apply improvements
        changes = await self._apply_improvements(proposals, feedback_analysis)
        evolution_results["changes"] = changes
        
        # 5. Record history
        self.evolution_history.append(evolution_results)
        
        return evolution_results
    
    async def _discover_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Discover patterns in data"""
        entities = data.get("entities", [])
        timestamps = data.get("timestamps", [])
        categories = data.get("categories", [])
        
        # Parse timestamps if they're strings
        parsed_timestamps = []
        for ts in timestamps:
            if isinstance(ts, str):
                try:
                    parsed = datetime.fromisoformat(ts)
                    parsed_timestamps.append(parsed)
                except:
                    pass
            elif isinstance(ts, datetime):
                parsed_timestamps.append(ts)
        
        # Discover patterns
        entity_patterns = self.pattern_discovery.discover_entity_patterns(entities)
        temporal_patterns = self.pattern_discovery.discover_temporal_patterns(parsed_timestamps)
        category_patterns = self.pattern_discovery.discover_category_patterns(categories)
        
        return {
            "entity_patterns": [
                {
                    "type": p.entity_type,
                    "name": p.name,
                    "occurrences": p.occurrences,
                    "confidence": p.confidence
                }
                for p in entity_patterns
            ],
            "temporal_patterns": [
                {
                    "type": p.pattern_type,
                    "description": p.description,
                    "frequency": p.frequency,
                    "confidence": p.confidence
                }
                for p in temporal_patterns
            ],
            "category_patterns": [
                {
                    "category": p.category,
                    "subcategories": p.subcategories,
                    "occurrence_count": p.occurrence_count,
                    "confidence": p.confidence
                }
                for p in category_patterns
            ],
            "summary": self.pattern_discovery.get_summary()
        }
    
    async def _generate_proposals(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate proposals from patterns"""
        proposals = {
            "categories": [],
            "entity_types": []
        }
        
        # Generate category proposals from category patterns
        for cat_pattern in patterns.get("category_patterns", []):
            if cat_pattern.get("confidence", 0) > 0.7:
                # Check if category already exists
                existing = self.taxonomy_manager.categories.get(cat_pattern["category"])
                if not existing:
                    proposal = self.taxonomy_manager.propose_category(
                        name=cat_pattern["category"],
                        description=f"Discovered category: {cat_pattern['category']}",
                        evidence=[{
                            "type": "pattern_discovery",
                            "confidence": cat_pattern["confidence"],
                            "subcategories": cat_pattern.get("subcategories", [])
                        }]
                    )
                    proposals["categories"].append({
                        "id": proposal.proposal_id,
                        "name": proposal.name,
                        "confidence": proposal.confidence
                    })
        
        # Generate entity type proposals from entity patterns
        for ent_pattern in patterns.get("entity_patterns", []):
            if ent_pattern.get("confidence", 0) > 0.8:
                # Check if entity type already exists
                existing = self.taxonomy_manager.entity_types.get(ent_pattern["type"])
                if not existing:
                    proposal = self.taxonomy_manager.propose_entity_type(
                        name=ent_pattern["type"],
                        description=f"Discovered entity type: {ent_pattern['type']}",
                        evidence=[{
                            "type": "pattern_discovery",
                            "confidence": ent_pattern["confidence"],
                            "occurrences": ent_pattern.get("occurrences", 0)
                        }]
                    )
                    proposals["entity_types"].append({
                        "id": proposal.proposal_id,
                        "name": proposal.name,
                        "confidence": proposal.confidence
                    })
        
        return proposals
    
    async def _analyze_feedback(self) -> Dict[str, Any]:
        """Analyze feedback for learning"""
        stats = self.feedback_system.get_stats()
        
        # Find low-performing items
        low_performing = []
        for target_id, scores in self.feedback_system.aggregated_scores.items():
            avg_score = self.feedback_system.get_average_score(target_id)
            if avg_score < 0.6:
                low_performing.append({
                    "target_id": target_id,
                    "average_score": avg_score,
                    "scores": scores
                })
        
        return {
            "stats": stats,
            "low_performing": low_performing[:10],
            "recommendations": []
        }
    
    async def _apply_improvements(self, proposals: Dict[str, Any], feedback: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply improvements based on proposals and feedback"""
        changes = []
        
        # Auto-approve high-confidence proposals
        for category in proposals.get("categories", []):
            if category.get("confidence", 0) > 0.9:
                # Auto-implement high-confidence category proposals
                success = self.taxonomy_manager.implement_category(category["id"])
                if success:
                    changes.append({
                        "type": "category_implemented",
                        "name": category["name"],
                        "confidence": category["confidence"]
                    })
        
        # Use feedback to adjust thresholds
        low_performing = feedback.get("low_performing", [])
        if low_performing:
            changes.append({
                "type": "feedback_analysis",
                "low_performing_count": len(low_performing),
                "action": "review_required"
            })
        
        return changes
    
    def get_status(self) -> Dict[str, Any]:
        """Get evolution engine status"""
        return {
            "running": self.running,
            "pattern_count": {
                "entity": len(self.pattern_discovery.entity_patterns),
                "temporal": len(self.pattern_discovery.temporal_patterns),
                "category": len(self.pattern_discovery.category_patterns)
            },
            "taxonomy": self.taxonomy_manager.get_taxonomy(),
            "feedback": self.feedback_system.get_stats(),
            "pending_proposals": self.taxonomy_manager.get_pending_proposals(),
            "history_count": len(self.evolution_history)
        }
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get evolution history"""
        return self.evolution_history[-limit:]
    
    def clear_history(self) -> None:
        """Clear evolution history"""
        self.evolution_history.clear()


# Create a singleton instance
_evolution_engine: Optional[EvolutionEngine] = None


def get_evolution_engine() -> EvolutionEngine:
    """Get the singleton evolution engine"""
    global _evolution_engine
    if _evolution_engine is None:
        _evolution_engine = EvolutionEngine()
    return _evolution_engine