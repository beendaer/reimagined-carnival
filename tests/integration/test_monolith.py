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
    
    def test_validate_fact(self):
        """Test third-party validation of a fact"""
        self.orchestrator.initialize()
        
        # Create a valid fact
        fact = Fact(
            id="validation_test_001",
            category="testing",
            statement="This is a test fact for third-party validation with sufficient length",
            verified=True,
            timestamp=datetime.now(),
            tags=["testing", "validation", "coherence"]
        )
        
        self.orchestrator.facts_registry.register_fact(fact)
        
        # Validate the fact
        result = self.orchestrator.validate_fact("validation_test_001")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['fact_id'], "validation_test_001")
        self.assertIn('investigation', result)
        self.assertIn('record_check', result)
        self.assertIn('validation', result)
        self.assertIn('status', result['validation'])
        self.assertIn('confidence', result['validation'])
    
    def test_validate_all_facts(self):
        """Test validation of all facts in the system"""
        self.orchestrator.initialize()
        
        # Validate all default facts
        result = self.orchestrator.validate_all_facts()
        
        self.assertIn('summary', result)
        self.assertIn('results', result)
        self.assertGreater(result['summary']['total_validated'], 0)
        self.assertGreater(len(result['results']), 0)
    
    def test_register_and_validate_fact(self):
        """Test registering a fact with validation"""
        self.orchestrator.initialize()
        
        # Create a high-quality fact that should pass validation
        fact = Fact(
            id="validated_fact_001",
            category="architecture",
            statement="Validated facts ensure data quality and coherence within the system",
            verified=True,
            timestamp=datetime.now(),
            tags=["architecture", "validation", "quality"]
        )
        
        result = self.orchestrator.register_and_validate_fact(fact)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['fact_id'], "validated_fact_001")
        self.assertTrue(result['coherence_maintained'])
        self.assertIn('validation', result)
        self.assertGreaterEqual(result['validation']['confidence'], 0.5)
    
    def test_register_and_validate_low_quality_fact(self):
        """Test that low-quality facts fail validation"""
        self.orchestrator.initialize()
        
        # Create a low-quality fact that should fail validation
        fact = Fact(
            id="low_quality",
            category="test",
            statement="Bad",  # Too short
            verified=False,
            timestamp=datetime.now(),
            tags=[]  # No tags
        )
        
        result = self.orchestrator.register_and_validate_fact(fact)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        self.assertIn('validation', result)
        self.assertLess(result['validation']['confidence'], 0.5)
    
    def test_system_status_includes_validation(self):
        """Test that system status includes validation information"""
        self.orchestrator.initialize()
        
        # Perform some validations
        self.orchestrator.validate_all_facts()
        
        status = self.orchestrator.get_system_status()
        
        self.assertIn('validation', status)
        self.assertIn('total_validated', status['validation'])
        self.assertIn('coherent', status['validation'])
        self.assertIn('average_confidence', status['validation'])
    
    def test_validation_workflow_end_to_end(self):
        """Test complete validation workflow from registration to reporting"""
        self.orchestrator.initialize()
        
        # Step 1: Register multiple facts with validation
        facts = [
            Fact(
                id=f"workflow_fact_{i}",
                category="workflow",
                statement=f"Workflow test fact number {i} with sufficient content for validation",
                verified=True,
                timestamp=datetime.now(),
                tags=["workflow", "testing", "validation"]
            )
            for i in range(3)
        ]
        
        for fact in facts:
            result = self.orchestrator.register_and_validate_fact(fact)
            self.assertTrue(result['success'])
        
        # Step 2: Validate all facts
        validation_results = self.orchestrator.validate_all_facts()
        
        # Step 3: Check system status
        status = self.orchestrator.get_system_status()
        
        # Verify workflow completed successfully
        self.assertGreater(status['validation']['total_validated'], 0)
        self.assertGreater(validation_results['summary']['coherent'], 0)
        self.assertTrue(status['coherence_verified'])


if __name__ == '__main__':
    unittest.main()

