"""
Enhanced RAG utilities for better document processing and retrieval
"""

import re
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import hashlib


class DocumentProcessor:
    """Advanced document processing utilities"""
    
    @staticmethod
    def extract_keywords(text: str) -> List[str]:
        """Extract important keywords from text"""
        # Technical terms that should be preserved
        technical_patterns = [
            r'\b[A-Z][a-z]+[A-Z][a-zA-Z]*\b',  # CamelCase
            r'\b[a-z]+-[a-z]+(?:-[a-z]+)*\b',  # kebab-case
            r'\b[a-z]+_[a-z]+(?:_[a-z]+)*\b',  # snake_case
            r'\b\w+\.\w+\b',  # dotted notation
            r'\b\w+::\w+\b',  # namespaced terms
        ]
        
        keywords = []
        for pattern in technical_patterns:
            keywords.extend(re.findall(pattern, text))
        
        # Common technical keywords
        tech_keywords = [
            'kubernetes', 'docker', 'api', 'rest', 'yaml', 'json',
            'deployment', 'service', 'pod', 'container', 'image',
            'config', 'secret', 'ingress', 'namespace', 'cluster'
        ]
        
        text_lower = text.lower()
        keywords.extend([kw for kw in tech_keywords if kw in text_lower])
        
        return list(set(keywords))
    
    @staticmethod
    def calculate_content_quality(text: str) -> float:
        """Calculate content quality score (0-1)"""
        if not text or len(text.strip()) < 50:
            return 0.0
        
        # Factor 1: Length appropriateness (not too short, not too long)
        length_score = min(1.0, len(text) / 2000) * (1 - max(0, (len(text) - 5000) / 10000))
        
        # Factor 2: Technical content density
        keywords = DocumentProcessor.extract_keywords(text)
        tech_density = min(1.0, len(keywords) / 20)
        
        # Factor 3: Structure quality (presence of headers, lists, etc.)
        structure_indicators = [
            r'^#+\s',  # Headers
            r'^\*\s',  # Lists
            r'^\d+\.\s',  # Numbered lists
            r'```',  # Code blocks
        ]
        
        structure_score = sum(1 for pattern in structure_indicators 
                            if re.search(pattern, text, re.MULTILINE)) / len(structure_indicators)
        
        # Factor 4: Information density (avoid repetitive content)
        unique_words = len(set(text.lower().split()))
        total_words = len(text.split())
        diversity_score = unique_words / max(total_words, 1) if total_words > 0 else 0
        
        # Weighted combination
        quality_score = (
            length_score * 0.3 +
            tech_density * 0.3 +
            structure_score * 0.2 +
            diversity_score * 0.2
        )
        
        return min(1.0, quality_score)


class QueryEnhancer:
    """Enhanced query processing for better retrieval"""
    
    @staticmethod
    def expand_query(query: str) -> str:
        """Expand query with synonyms and related terms"""
        expansions = {
            'k8s': 'kubernetes',
            'kube': 'kubernetes',
            'deploy': 'deployment',
            'svc': 'service',
            'ing': 'ingress',
            'ns': 'namespace',
            'cm': 'configmap',
            'pv': 'persistentvolume',
            'pvc': 'persistentvolumeclaim',
        }
        
        expanded_query = query
        for abbrev, full_term in expansions.items():
            if abbrev in query.lower():
                expanded_query += f" {full_term}"
        
        return expanded_query
    
    @staticmethod
    def extract_intent(query: str) -> Dict[str, any]:
        """Extract intent and entities from query"""
        intent_patterns = {
            'how_to': [r'how\s+(?:do|to|can)', r'steps?\s+to', r'guide'],
            'what_is': [r'what\s+is', r'define', r'explain', r'meaning'],
            'troubleshoot': [r'error', r'issue', r'problem', r'not\s+working', r'fail', r'debug'],
            'list': [r'list', r'show\s+all', r'get\s+all', r'find\s+all'],
            'compare': [r'difference', r'compare', r'vs', r'versus', r'better'],
        }
        
        detected_intent = 'general'
        confidence = 0.0
        
        query_lower = query.lower()
        for intent, patterns in intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    detected_intent = intent
                    confidence = 0.8
                    break
            if confidence > 0:
                break
        
        # Extract entities (technical terms, product names, etc.)
        entities = DocumentProcessor.extract_keywords(query)
        
        return {
            'intent': detected_intent,
            'confidence': confidence,
            'entities': entities,
            'enhanced_query': QueryEnhancer.expand_query(query)
        }


class ResponseFormatter:
    """Format responses for better readability"""
    
    @staticmethod
    def format_technical_response(content: str, sources: List[str]) -> str:
        """Format technical responses with better structure"""
        # Add code block formatting
        content = re.sub(r'`([^`]+)`', r'**`\1`**', content)
        
        # Format command examples
        content = re.sub(r'(kubectl\s+[^\n]+)', r'\n```bash\n\1\n```\n', content)
        content = re.sub(r'(docker\s+[^\n]+)', r'\n```bash\n\1\n```\n', content)
        
        # Add source attribution
        if sources:
            unique_sources = list(set(sources))
            if len(unique_sources) <= 3:
                source_text = "\n\n**Sources:** " + ", ".join(unique_sources)
                content += source_text
        
        return content.strip()
    
    @staticmethod
    def add_helpful_tips(content: str, query_intent: str) -> str:
        """Add helpful tips based on query intent"""
        tips = {
            'troubleshoot': "\n\n💡 **Tip:** Check logs with `kubectl logs <pod-name>` for more details.",
            'how_to': "\n\n💡 **Tip:** Always test in a development environment first.",
            'what_is': "\n\n💡 **Tip:** See official documentation for complete details.",
        }
        
        if query_intent in tips:
            content += tips[query_intent]
        
        return content


class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'queries_processed': 0,
            'avg_response_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0,
        }
        self.response_times = []
    
    def log_query(self, response_time: float, cache_hit: bool = False):
        """Log query performance"""
        self.metrics['queries_processed'] += 1
        self.response_times.append(response_time)
        
        if cache_hit:
            self.metrics['cache_hits'] += 1
        else:
            self.metrics['cache_misses'] += 1
        
        # Calculate rolling average
        if len(self.response_times) > 100:
            self.response_times = self.response_times[-100:]
        
        self.metrics['avg_response_time'] = sum(self.response_times) / len(self.response_times)
    
    def get_stats(self) -> Dict[str, any]:
        """Get performance statistics"""
        total_requests = self.metrics['cache_hits'] + self.metrics['cache_misses']
        cache_hit_rate = (self.metrics['cache_hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            **self.metrics,
            'cache_hit_rate': cache_hit_rate,
            'total_requests': total_requests
        }


# Global performance monitor instance
performance_monitor = PerformanceMonitor()