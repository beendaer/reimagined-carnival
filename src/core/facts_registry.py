"""
Facts Registry - Central repository for maintaining determined facts
Ensures coherence within the monolith following established patterns
"""
from typing import List, Optional, Dict
from datetime import datetime
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.fact import Fact
from utils.helpers import serialize_datetime


class FactsRegistry:
    """
    Centralized registry for managing determined facts within the monolith.
    Follows singleton pattern to ensure coherence across the system.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._facts: Dict[str, Fact] = {}
        self._initialized = True
    
    @classmethod
    def reset_for_testing(cls) -> None:
        """Reset the singleton instance for testing purposes"""
        cls._instance = None
    
    def register_fact(self, fact: Fact) -> None:
        """Register a new fact in the registry"""
        if fact.id in self._facts:
            raise ValueError(f"Fact with id {fact.id} already exists")
        self._facts[fact.id] = fact
    
    def get_fact(self, fact_id: str) -> Optional[Fact]:
        """Retrieve a fact by its ID"""
        return self._facts.get(fact_id)
    
    def get_facts_by_category(self, category: str) -> List[Fact]:
        """Retrieve all facts in a specific category"""
        return [f for f in self._facts.values() if f.category == category]
    
    def get_verified_facts(self) -> List[Fact]:
        """Retrieve all verified facts"""
        return [f for f in self._facts.values() if f.verified]
    
    def update_fact(self, fact_id: str, **updates) -> None:
        """Update an existing fact"""
        if fact_id not in self._facts:
            raise ValueError(f"Fact with id {fact_id} not found")
        
        fact = self._facts[fact_id]
        for key, value in updates.items():
            if hasattr(fact, key):
                setattr(fact, key, value)
    
    def export_facts(self, filepath: Path) -> None:
        """Export all facts to a JSON file"""
        data = {fid: fact.to_dict() for fid, fact in self._facts.items()}
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=serialize_datetime)
    
    def import_facts(self, filepath: Path) -> None:
        """Import facts from a JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for fact_id, fact_data in data.items():
            fact = Fact.from_dict(fact_data)
            self._facts[fact_id] = fact
    
    def get_coherence_report(self) -> dict:
        """Generate a report on fact coherence within the monolith"""
        return {
            'total_facts': len(self._facts),
            'verified_facts': len(self.get_verified_facts()),
            'categories': len(set(f.category for f in self._facts.values())),
            'category_breakdown': self._get_category_breakdown()
        }
    
    def _get_category_breakdown(self) -> dict:
        """Get breakdown of facts by category"""
        breakdown = {}
        for fact in self._facts.values():
            breakdown[fact.category] = breakdown.get(fact.category, 0) + 1
        return breakdown
