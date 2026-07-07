"""
Metadata Classifiers
Classify assets by domain, category, and generate tags
"""

import re
from typing import Dict, Any, List, Set, Optional
from collections import Counter
from datetime import datetime

from src.models.mdips import Domain


class Classifier:
    """Base classifier"""
    
    def classify(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Classify content"""
        raise NotImplementedError


class DomainClassifier(Classifier):
    """
    Classify content by intelligence domain
    """
    
    def __init__(self):
        self.domain_keywords = {
            Domain.OSINT: ["open source", "public", "web", "social", "media"],
            Domain.SOCMINT: ["social", "facebook", "twitter", "linkedin", "discord", "telegram"],
            Domain.CYBINT: ["cyber", "security", "malware", "attack", "vulnerability"],
            Domain.FININT: ["financial", "bank", "transaction", "investment", "market"],
            Domain.GEOINT: ["location", "geographic", "map", "coordinates", "address"],
            Domain.IMINT: ["image", "photo", "visual", "screenshot", "video"],
            Domain.DFIR: ["forensic", "digital", "evidence", "investigation"],
            Domain.SIGINT: ["signal", "communication", "radio", "frequency"]
        }
    
    def classify(self, content: Dict[str, Any]) -> List[str]:
        """Determine the domain(s) of the content"""
        domains = []
        
        # Extract text from content
        text = self._extract_text(content).lower()
        
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for kw in keywords if kw in text)
            if score >= 2:  # At least 2 keyword matches
                domains.append(domain.value)
        
        # If no domain detected, default to OSINT
        if not domains:
            domains.append(Domain.OSINT.value)
        
        return domains
    
    def _extract_text(self, content: Dict[str, Any]) -> str:
        """Extract text from content dict"""
        text = ""
        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, str):
                    text += f" {value}"
                elif isinstance(value, dict):
                    text += f" {self._extract_text(value)}"
        return text


class CategoryClassifier(Classifier):
    """
    Classify content into categories
    """
    
    def __init__(self):
        self.categories = {
            "individual": ["person", "individual", "profile", "identity"],
            "organization": ["company", "organization", "corp", "business"],
            "event": ["event", "meeting", "announcement", "conference"],
            "location": ["location", "place", "city", "region"],
            "financial": ["financial", "transaction", "investment"],
            "technical": ["technical", "code", "software", "repository"],
            "threat": ["threat", "malware", "attack", "vulnerability"],
            "intelligence": ["intelligence", "signal", "assessment"]
        }
    
    def classify(self, content: Dict[str, Any]) -> List[str]:
        """Determine the category(ies) of the content"""
        categories = []
        text = self._extract_text(content).lower()
        
        for category, keywords in self.categories.items():
            if any(kw in text for kw in keywords):
                categories.append(category)
        
        if not categories:
            categories.append("general")
        
        return categories
    
    def _extract_text(self, content: Dict[str, Any]) -> str:
        """Extract text from content dict"""
        text = ""
        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, str):
                    text += f" {value}"
                elif isinstance(value, dict):
                    text += f" {self._extract_text(value)}"
        return text


class TagGenerator(Classifier):
    """
    Generate tags from content
    """
    
    def __init__(self, max_tags: int = 10):
        self.max_tags = max_tags
        self.stopwords = {
            "the", "a", "an", "of", "to", "for", "with", "on", "at", "from",
            "by", "in", "is", "it", "and", "or", "but", "this", "that", "these",
            "those", "then", "than", "so", "very", "too", "also", "just"
        }
    
    def classify(self, content: Dict[str, Any]) -> List[str]:
        """Generate tags from content"""
        # Extract text
        text = self._extract_text(content)
        
        # Extract words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter stopwords and short words
        filtered = [w for w in words if w not in self.stopwords and len(w) > 2]
        
        # Count frequencies
        word_counts = Counter(filtered)
        
        # Get top tags
        tags = [word for word, _ in word_counts.most_common(self.max_tags)]
        
        return tags
    
    def _extract_text(self, content: Dict[str, Any]) -> str:
        """Extract text from content dict"""
        text = ""
        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, str):
                    text += f" {value}"
                elif isinstance(value, dict):
                    text += f" {self._extract_text(value)}"
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            text += f" {item}"
                        elif isinstance(item, dict):
                            text += f" {self._extract_text(item)}"
        return text