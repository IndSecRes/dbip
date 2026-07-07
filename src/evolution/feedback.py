"""
Feedback System
Collects and processes feedback for improvement
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class FeedbackEntry:
    """A feedback entry"""
    feedback_type: str  # accuracy, quality, relevance, completeness
    rating: float  # 0-1 scale
    target_id: str
    target_type: str
    feedback_id: str = field(default_factory=lambda: f"FDB_{uuid.uuid4().hex[:8].upper()}")
    comment: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class FeedbackSystem:
    """
    Collects and processes feedback
    """
    
    def __init__(self):
        self.feedback: List[FeedbackEntry] = []
        self.aggregated_scores: Dict[str, Dict[str, float]] = {}
    
    def add_feedback(
        self,
        feedback_type: str,
        rating: float,
        target_id: str,
        target_type: str,
        comment: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> FeedbackEntry:
        """Add feedback"""
        entry = FeedbackEntry(
            feedback_type=feedback_type,
            rating=max(0, min(1, rating)),  # Clamp to 0-1
            target_id=target_id,
            target_type=target_type,
            comment=comment,
            metadata=metadata or {}
        )
        self.feedback.append(entry)
        self._aggregate_feedback(target_id, target_type)
        return entry
    
    def get_scores(self, target_id: str) -> Dict[str, float]:
        """Get scores for a target"""
        return self.aggregated_scores.get(target_id, {})
    
    def get_average_score(self, target_id: str) -> float:
        """Get average score for a target"""
        scores = self.get_scores(target_id)
        if not scores:
            return 0.0
        
        # Weighted average of all feedback types
        weights = {
            "accuracy": 0.4,
            "quality": 0.3,
            "relevance": 0.2,
            "completeness": 0.1
        }
        
        total_weighted = 0
        total_weight = 0
        
        for feedback_type, score in scores.items():
            weight = weights.get(feedback_type, 0.25)
            total_weighted += score * weight
            total_weight += weight
        
        return total_weighted / total_weight if total_weight > 0 else 0.0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get feedback statistics"""
        if not self.feedback:
            return {"total_feedback": 0}
        
        ratings = [f.rating for f in self.feedback]
        
        return {
            "total_feedback": len(self.feedback),
            "average_rating": sum(ratings) / len(ratings),
            "max_rating": max(ratings),
            "min_rating": min(ratings),
            "feedback_types": {
                "accuracy": len([f for f in self.feedback if f.feedback_type == "accuracy"]),
                "quality": len([f for f in self.feedback if f.feedback_type == "quality"]),
                "relevance": len([f for f in self.feedback if f.feedback_type == "relevance"]),
                "completeness": len([f for f in self.feedback if f.feedback_type == "completeness"])
            },
            "unique_targets": len(set(f.target_id for f in self.feedback))
        }
    
    def _aggregate_feedback(self, target_id: str, target_type: str) -> None:
        """Aggregate feedback for a target"""
        relevant_feedback = [
            f for f in self.feedback
            if f.target_id == target_id
        ]
        
        scores = {}
        for fb_type in ["accuracy", "quality", "relevance", "completeness"]:
            type_feedback = [
                f for f in relevant_feedback
                if f.feedback_type == fb_type
            ]
            if type_feedback:
                scores[fb_type] = sum(f.rating for f in type_feedback) / len(type_feedback)
        
        if scores:
            self.aggregated_scores[target_id] = scores
    
    def get_improvement_recommendations(self, target_id: str) -> List[Dict[str, Any]]:
        """Get recommendations for improvement"""
        scores = self.get_scores(target_id)
        if not scores:
            return []
        
        recommendations = []
        for feedback_type, score in scores.items():
            if score < 0.7:
                recommendations.append({
                    "feedback_type": feedback_type,
                    "score": score,
                    "priority": "high" if score < 0.5 else "medium",
                    "suggestion": f"Improve {feedback_type} score from {score:.2f} to above 0.7"
                })
        
        return recommendations