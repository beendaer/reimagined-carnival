"""
Integration tests for the TAAS Monolith
Testing the complete system integration following best practices
"""
import unittest
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from core.orchestrator import MonolithOrchestrator
from models.fact import Fact


class TestMonolithIntegration(unittest.TestCase):
    """Integration tests for the complete monolith"""
    
    def setUp(self):
        """Set up orchestrator before each test"""
        from core.facts_registry import FactsRegistry
        FactsRegistry.reset_for_testing()
        self.orchestrator = MonolithOrchestrator()
    
    def test_initialize_monolith(self):
        """Test monolith initialization"""
        self.orchestrator.initialize()
        
        status = self.orchestrator.get_system_status()
        
        self.assertTrue(status['initialized'])
        self.assertGreater(status['facts']['total_facts'], 0)
    
    def test_register_and_test_fact(self):
        """Test registering a fact and verifying coherence"""
        self.orchestrator.initialize()
        
        new_fact = Fact(
            id="integration_001",
            category="integration",
            statement="Integration test fact",
            verified=True,
            timestamp=datetime.now(),
            tags=["integration", "test"]
        )
        
        result = self.orchestrator.register_and_test_fact(new_fact)
        
        self.assertTrue(result['success'])
        self.assertTrue(result['coherence_maintained'])
    
    def test_execute_tests(self):
        """Test executing tests through orchestrator"""
        self.orchestrator.initialize()
        
        # Register a test
        def sample_test():
            assert True
        
        self.orchestrator.test_service.register_test("integration_test", sample_test)
        
        # Execute tests
        results = self.orchestrator.execute_tests()
        
        self.assertIn('summary', results)
        self.assertIn('results', results)
    
    def test_system_status(self):
        """Test getting complete system status"""
        self.orchestrator.initialize()
        
        status = self.orchestrator.get_system_status()
        
        self.assertIn('initialized', status)
        self.assertIn('facts', status)
        self.assertIn('tests', status)
        self.assertIn('coherence_verified', status)
    
    def test_fact_coherence_across_services(self):
        """Test that facts maintain coherence across services"""
        self.orchestrator.initialize()
        
        # Add a fact through orchestrator
        fact = Fact(
            id="coherence_test",
            category="coherence",
            statement="Cross-service coherence test",
            verified=True,
            timestamp=datetime.now(),
            tags=["coherence"]
        )
        
        self.orchestrator.register_and_test_fact(fact)
        
        # Verify through facts registry
        retrieved = self.orchestrator.facts_registry.get_fact("coherence_test")
        self.assertIsNotNone(retrieved)
        
        # Verify through test service
        coherence_ok = self.orchestrator.test_service.verify_fact_coherence()
        self.assertTrue(coherence_ok)


if __name__ == '__main__':
    unittest.main()
