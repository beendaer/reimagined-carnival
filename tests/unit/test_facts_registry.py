"""
Unit tests for the Facts Registry
Testing coherence maintenance within the monolith
"""
import unittest
from datetime import datetime
import sys
from pathlib import Path
import tempfile
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from models.fact import Fact
from core.facts_registry import FactsRegistry


class TestFactsRegistry(unittest.TestCase):
    """Test cases for the Facts Registry"""
    
    def setUp(self):
        """Reset registry before each test"""
        # Create a fresh registry instance
        FactsRegistry.reset_for_testing()
        self.registry = FactsRegistry()
    
    def test_singleton_pattern(self):
        """Test that registry follows singleton pattern"""
        registry1 = FactsRegistry()
        registry2 = FactsRegistry()
        
        self.assertIs(registry1, registry2)
    
    def test_register_fact(self):
        """Test registering a fact"""
        fact = Fact(
            id="reg_001",
            category="test",
            statement="Registry test fact",
            verified=True,
            timestamp=datetime.now(),
            tags=["test"]
        )
        
        self.registry.register_fact(fact)
        retrieved = self.registry.get_fact("reg_001")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, "reg_001")
    
    def test_duplicate_fact_raises_error(self):
        """Test that registering duplicate fact raises error"""
        fact = Fact(
            id="dup_001",
            category="test",
            statement="Duplicate test",
            verified=True,
            timestamp=datetime.now(),
            tags=["test"]
        )
        
        self.registry.register_fact(fact)
        
        with self.assertRaises(ValueError):
            self.registry.register_fact(fact)
    
    def test_get_facts_by_category(self):
        """Test retrieving facts by category"""
        fact1 = Fact(
            id="cat_001",
            category="architecture",
            statement="Architecture fact",
            verified=True,
            timestamp=datetime.now(),
            tags=["test"]
        )
        fact2 = Fact(
            id="cat_002",
            category="architecture",
            statement="Another architecture fact",
            verified=True,
            timestamp=datetime.now(),
            tags=["test"]
        )
        
        self.registry.register_fact(fact1)
        self.registry.register_fact(fact2)
        
        arch_facts = self.registry.get_facts_by_category("architecture")
        
        self.assertEqual(len(arch_facts), 2)
    
    def test_get_verified_facts(self):
        """Test retrieving only verified facts"""
        fact1 = Fact(
            id="ver_001",
            category="test",
            statement="Verified fact",
            verified=True,
            timestamp=datetime.now(),
            tags=["test"]
        )
        fact2 = Fact(
            id="ver_002",
            category="test",
            statement="Unverified fact",
            verified=False,
            timestamp=datetime.now(),
            tags=["test"]
        )
        
        self.registry.register_fact(fact1)
        self.registry.register_fact(fact2)
        
        verified = self.registry.get_verified_facts()
        
        self.assertEqual(len(verified), 1)
        self.assertEqual(verified[0].id, "ver_001")
    
    def test_get_facts_by_tag(self):
        """Test retrieving facts by tag"""
        fact1 = Fact(
            id="tag_001",
            category="test",
            statement="Tagged fact",
            verified=True,
            timestamp=datetime.now(),
            tags=["security", "audit"]
        )
        fact2 = Fact(
            id="tag_002",
            category="test",
            statement="Other fact",
            verified=True,
            timestamp=datetime.now(),
            tags=["audit"]
        )
        
        self.registry.register_fact(fact1)
        self.registry.register_fact(fact2)
        
        tagged = self.registry.get_facts_by_tag("security")
        
        self.assertEqual(len(tagged), 1)
        self.assertEqual(tagged[0].id, "tag_001")
    
    def test_coherence_report(self):
        """Test coherence report generation"""
        fact = Fact(
            id="coh_001",
            category="coherence",
            statement="Coherence test",
            verified=True,
            timestamp=datetime.now(),
            tags=["test"]
        )
        
        self.registry.register_fact(fact)
        report = self.registry.get_coherence_report()
        
        self.assertEqual(report['total_facts'], 1)
        self.assertEqual(report['verified_facts'], 1)
        self.assertIn('coherence', report['category_breakdown'])


if __name__ == '__main__':
    unittest.main()
