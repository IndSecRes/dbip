"""
Context and Entity Extractors
Extract contextual information and entities from content
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta


class ContextExtractor:
    """
    Extract contextual information from content
    """
    
    def extract_temporal(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract temporal context"""
        text = self._extract_text(content)
        
        # Look for date patterns
        dates = self._find_dates(text)
        time_references = self._find_time_references(text)
        
        return {
            "detected_dates": dates,
            "time_references": time_references,
            "temporal_span": self._calculate_temporal_span(dates) if dates else None
        }
    
    def extract_geographic(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract geographic context"""
        text = self._extract_text(content)
        
        # Look for location patterns
        locations = self._find_locations(text)
        
        return {
            "detected_locations": locations,
            "location_count": len(locations)
        }
    
    def extract_sentiment(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract sentiment from content"""
        text = self._extract_text(content)
        
        # Simple sentiment analysis
        positive_words = ["good", "great", "excellent", "positive", "success", "happy", "improved"]
        negative_words = ["bad", "poor", "negative", "failure", "problem", "issue", "risk"]
        
        positive_count = sum(1 for w in positive_words if w in text.lower())
        negative_count = sum(1 for w in negative_words if w in text.lower())
        
        total = positive_count + negative_count
        if total == 0:
            sentiment = "neutral"
            score = 0.0
        else:
            score = (positive_count - negative_count) / total
            if score > 0.2:
                sentiment = "positive"
            elif score < -0.2:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "score": round(score, 3),
            "positive_count": positive_count,
            "negative_count": negative_count
        }
    
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
    
    def _find_dates(self, text: str) -> List[str]:
        """Find date patterns in text"""
        patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
            r'\w+ \d{1,2},? \d{4}',  # Month DD, YYYY
            r'\d{1,2} \w+ \d{4}',  # DD Month YYYY
        ]
        
        dates = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)
        
        return dates[:10]  # Limit to 10 dates
    
    def _find_time_references(self, text: str) -> List[str]:
        """Find time reference patterns"""
        time_patterns = [
            r'\d{1,2}:\d{2}\s*(?:AM|PM)?',  # Time with AM/PM
            r'\d{1,2}:\d{2}',  # Time
            r'today', r'tomorrow', r'yesterday',
            r'next week', r'last week', r'this month'
        ]
        
        references = []
        for pattern in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            references.extend([m.lower() for m in matches])
        
        return references[:10]
    
    def _calculate_temporal_span(self, dates: List[str]) -> Optional[str]:
        """Calculate temporal span from dates"""
        if len(dates) < 2:
            return None
        
        try:
            parsed_dates = []
            for d in dates:
                try:
                    parsed = datetime.strptime(d, "%Y-%m-%d")
                    parsed_dates.append(parsed)
                except ValueError:
                    pass
            
            if parsed_dates:
                min_date = min(parsed_dates)
                max_date = max(parsed_dates)
                delta = max_date - min_date
                return f"{delta.days} days"
        except:
            pass
        
        return None
    
    def _find_locations(self, text: str) -> List[str]:
        """Find location mentions in text"""
        location_keywords = {
            "nyc": "New York City",
            "new york": "New York City",
            "la": "Los Angeles",
            "los angeles": "Los Angeles",
            "sf": "San Francisco",
            "san francisco": "San Francisco",
            "london": "London",
            "paris": "Paris",
            "tokyo": "Tokyo",
            "berlin": "Berlin",
            "mumbai": "Mumbai",
            "bangalore": "Bangalore",
            "delhi": "Delhi",
            "singapore": "Singapore",
            "sydney": "Sydney"
        }
        
        locations = []
        text_lower = text.lower()
        
        for key, value in location_keywords.items():
            if key in text_lower:
                locations.append(value)
        
        return list(set(locations))


class EntityExtractor:
    """
    Extract entities from content
    """
    
    def extract_person_names(self, text: str) -> List[str]:
        """Extract person names from text"""
        # Simple pattern: Capitalized words (potential names)
        pattern = r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)*\b'
        matches = re.findall(pattern, text)
        
        # Filter common non-name words
        stop_names = {"The", "A", "An", "And", "Or", "But", "For", "Nor", "On", "At"}
        
        # Also filter out single letters and common words
        names = [
            m for m in matches 
            if len(m) > 2 
            and m not in stop_names
            and m.lower() not in {"is", "are", "was", "were", "this", "that", "there", "their"}
        ]
        
        return names[:20]  # Limit to 20 names
    
    def extract_organizations(self, text: str) -> List[str]:
        """Extract organization names from text"""
        # Look for patterns like "ACME Corp", "ACME Corporation", "ACME Inc."
        patterns = [
            r'[A-Z][A-Za-z]+ (?:Corp|Corporation|Inc|Incorporated|LLC|Ltd|Limited|GmbH|AG|SA)',
            r'[A-Z][A-Za-z]+ (?:company|organization|group)'
        ]
        
        organizations = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            organizations.extend(matches)
        
        return list(set(organizations))[:10]
    
    def extract_technologies(self, text: str) -> List[str]:
        """Extract technology names from text"""
        tech_keywords = [
            "Python", "Java", "JavaScript", "C++", "Go", "Rust",
            "TensorFlow", "PyTorch", "Keras", "scikit-learn",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP",
            "Neo4j", "PostgreSQL", "Redis", "Kafka",
            "FastAPI", "Django", "Flask", "Spring"
        ]
        
        technologies = []
        text_lower = text.lower()
        
        for tech in tech_keywords:
            if tech.lower() in text_lower or tech in text:
                technologies.append(tech)
        
        return list(set(technologies))