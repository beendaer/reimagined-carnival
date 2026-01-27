"""
Unit tests for the Test Service (TAAS)
Testing the Testing as a Service functionality
"""
import unittest
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from services.test_service import TestService, TestStatus
from core.facts_registry import FactsRegistry
from models.fact import Fact


class TestTestService(unittest.TestCase):
    """Test cases for the Test Service"""
    
    def setUp(self):
        """Set up test service before each test"""
        # Reset registry
        FactsRegistry.reset_for_testing()
        self.registry = FactsRegistry()
        self.test_service = TestService(self.registry)
    
    def test_register_test(self):
        """Test registering a test case"""
        def sample_test():
            assert True
        
        self.test_service.register_test("test_001", sample_test)
        
        self.assertIn("test_001", self.test_service.test_cases)
    
    def test_run_passing_test(self):
        """Test running a passing test"""
        def passing_test():
            assert 1 + 1 == 2
        
        self.test_service.register_test("pass_test", passing_test)
        result = self.test_service.run_test("pass_test")
        
        self.assertEqual(result.status, TestStatus.PASSED)
        self.assertEqual(result.test_id, "pass_test")
    
    def test_run_failing_test(self):
        """Test running a failing test"""
        def failing_test():
            assert 1 + 1 == 3
        
        self.test_service.register_test("fail_test", failing_test)
        result = self.test_service.run_test("fail_test")
        
        self.assertEqual(result.status, TestStatus.FAILED)
        self.assertIn("Assertion failed", result.message)
    
    def test_run_all_tests(self):
        """Test running all registered tests"""
        def test1():
            assert True
        
        def test2():
            assert True
        
        self.test_service.register_test("test_1", test1)
        self.test_service.register_test("test_2", test2)
        
        results = self.test_service.run_all_tests()
        
        self.assertEqual(len(results), 2)
    
    def test_get_test_summary(self):
        """Test getting test execution summary"""
        def passing_test():
            assert True
        
        def failing_test():
            assert False
        
        self.test_service.register_test("pass", passing_test)
        self.test_service.register_test("fail", failing_test)
        self.test_service.run_all_tests()
        
        summary = self.test_service.get_test_summary()
        
        self.assertEqual(summary['total'], 2)
        self.assertEqual(summary['passed'], 1)
        self.assertEqual(summary['failed'], 1)
        self.assertEqual(summary['success_rate'], 50.0)
    
    def test_verify_fact_coherence(self):
        """Test fact coherence verification"""
        fact = Fact(
            id="coherence_001",
            category="test",
            statement="Test coherence",
            verified=True,
            timestamp=datetime.now(),
            tags=["test"]
        )
        
        self.registry.register_fact(fact)
        
        coherence_ok = self.test_service.verify_fact_coherence()
        self.assertTrue(coherence_ok)


if __name__ == '__main__':
    unittest.main()
