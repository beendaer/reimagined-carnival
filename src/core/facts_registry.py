"""
Facts Registry - Single source of truth for determined facts
Implements Singleton pattern to maintain coherence across the monolith
"""
from typing import Dict, List, Optional, Any
from src.models.fact import Fact


class FactsRegistry:
    """
    Singleton registry for managing facts
    Maintains coherence by serving as the single source of truth
    """
    
    _instance: Optional['FactsRegistry'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """Ensure only one instance exists (Singleton pattern)"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize registry if not already initialized"""
        if not FactsRegistry._initialized:
            self._facts: Dict[str, Fact] = {}
            FactsRegistry._initialized = True
    
    @classmethod
    def reset_for_testing(cls):
        """Reset the singleton instance for testing purposes"""
        cls._instance = None
        cls._initialized = False
    
    def register_fact(self, fact: Fact) -> None:
        """
        Register a fact in the registry
        
        Args:
            fact: The fact to register
            
        Raises:
            ValueError: If fact with same ID already exists
        """
        if fact.id in self._facts:
            raise ValueError(f"Fact with ID '{fact.id}' already exists")
        
        self._facts[fact.id] = fact
    
    def get_fact(self, fact_id: str) -> Optional[Fact]:
        """
        Retrieve a fact by ID
        
        Args:
            fact_id: The fact identifier
            
        Returns:
            The fact if found, None otherwise
        """
        return self._facts.get(fact_id)
    
    def get_all_facts(self) -> List[Fact]:
        """
        Get all registered facts
        
        Returns:
            List of all facts
        """
        return list(self._facts.values())
    
    def get_facts_by_category(self, category: str) -> List[Fact]:
        """
        Get facts filtered by category
        
        Args:
            category: The category to filter by
            
        Returns:
            List of facts in the specified category
        """
        return [fact for fact in self._facts.values() if fact.category == category]
    
    def get_verified_facts(self) -> List[Fact]:
        """
        Get only verified facts
        
        Returns:
            List of verified facts
        """
        return [fact for fact in self._facts.values() if fact.verified]
    
    def get_facts_by_tag(self, tag: str) -> List[Fact]:
        """
        Get facts filtered by tag
        
        Args:
            tag: The tag to filter by
            
        Returns:
            List of facts with the specified tag
        """
        return [fact for fact in self._facts.values() if tag in fact.tags]
    
    def update_fact(self, fact_id: str, updated_fact: Fact) -> bool:
        """
        Update an existing fact
        
        Args:
            fact_id: The ID of the fact to update
            updated_fact: The updated fact data
            
        Returns:
            True if updated successfully, False if not found
        """
        if fact_id in self._facts:
            self._facts[fact_id] = updated_fact
            return True
        return False
    
    def delete_fact(self, fact_id: str) -> bool:
        """
        Delete a fact from the registry
        
        Args:
            fact_id: The ID of the fact to delete
            
        Returns:
            True if deleted successfully, False if not found
        """
        if fact_id in self._facts:
            del self._facts[fact_id]
            return True
        return False
    
    def get_coherence_report(self) -> Dict[str, Any]:
        """
        Generate a coherence report for all facts
        
        Returns:
            Dictionary containing coherence statistics
        """
        total = len(self._facts)
        verified = len(self.get_verified_facts())
        
        # Category breakdown
        categories = {}
        for fact in self._facts.values():
            categories[fact.category] = categories.get(fact.category, 0) + 1
        
        return {
            'total_facts': total,
            'verified_facts': verified,
            'unverified_facts': total - verified,
            'verification_rate': (verified / total * 100) if total > 0 else 0.0,
            'category_breakdown': categories,
            'categories_count': len(categories)
        }
    
    def count(self) -> int:
        """
        Get the total number of facts
        
        Returns:
            Number of facts in the registry
        """
        return len(self._facts)
    
    def clear(self) -> None:
        """Clear all facts from the registry (use with caution)"""
        self._facts.clear()
