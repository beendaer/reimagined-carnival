"""
Unit tests for ValidationService
Tests third-party validation functionality
"""
import unittest
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))
from services.validation_service import ValidationService, ValidationStatus, ValidationResult
from models.fact import Fact
from core.facts_registry import FactsRegistry


class TestValidationService(unittest.TestCase):
    """Test suite for ValidationService"""
    
    def setUp(self):
        """Set up test fixtures"""
        FactsRegistry.reset_for_testing()
        self.registry = FactsRegistry()
        self.validation_service = ValidationService(self.registry)
        
        # Create sample facts
        self.valid_fact = Fact(
            id="test_001",
            category="testing",
            statement="This is a valid test fact with sufficient length",
            verified=True,
            timestamp=datetime.now(),
            tags=["test", "validation", "testing"]
        )
        
        self.short_fact = Fact(
            id="test_002",
            category="testing",
            statement="Bad",  # Only 3 characters - should fail
            verified=False,
            timestamp=datetime.now(),
            tags=["test"]
        )
        
        self.no_tags_fact = Fact(
            id="test_003",
            category="testing",
            statement="This fact has no tags which may affect coherence",
            verified=True,
            timestamp=datetime.now(),
            tags=[]
        )
    
    def tearDown(self):
        """Clean up after tests"""
        FactsRegistry.reset_for_testing()
    
    def test_investigate_fact(self):
        """Test investigating a fact"""
        self.registry.register_fact(self.valid_fact)
        investigation = self.validation_service.investigate_fact(self.valid_fact)
        
        self.assertEqual(investigation['fact_id'], 'test_001')
        self.assertEqual(investigation['category'], 'testing')
        self.assertGreater(investigation['statement_length'], 0)
        self.assertEqual(investigation['tag_count'], 3)
        self.assertTrue(investigation['verified'])
        self.assertIn('tag_coherence', investigation)
    
    def test_check_records(self):
        """Test checking records for a fact"""
        self.registry.register_fact(self.valid_fact)
        checks = self.validation_service.check_records('test_001')
        
        self.assertTrue(checks['found'])
        self.assertEqual(checks['fact_id'], 'test_001')
        self.assertTrue(checks['has_valid_id'])
        self.assertTrue(checks['has_valid_statement'])
        self.assertTrue(checks['has_category'])
        self.assertTrue(checks['tags_present'])
    
    def test_check_records_not_found(self):
        """Test checking records for non-existent fact"""
        checks = self.validation_service.check_records('nonexistent')
        
        self.assertFalse(checks['found'])
        self.assertIn('error', checks)
    
    def test_evaluate_coherence_valid_fact(self):
        """Test evaluating coherence for a valid fact"""
        self.registry.register_fact(self.valid_fact)
        result = self.validation_service.evaluate_coherence(self.valid_fact)
        
        self.assertIsInstance(result, ValidationResult)
        self.assertEqual(result.fact_id, 'test_001')
        self.assertEqual(result.status, ValidationStatus.COHERENT)
        self.assertGreaterEqual(result.confidence, 0.8)
        self.assertIsInstance(result.findings, list)
    
    def test_evaluate_coherence_short_statement(self):
        """Test evaluating coherence for fact with short statement"""
        self.registry.register_fact(self.short_fact)
        result = self.validation_service.evaluate_coherence(self.short_fact)
        
        self.assertIsInstance(result, ValidationResult)
        self.assertEqual(result.fact_id, 'test_002')
        self.assertIn(result.status, [ValidationStatus.SUSPICIOUS, ValidationStatus.NOISE])
        self.assertLess(result.confidence, 0.8)
    
    def test_evaluate_coherence_no_tags(self):
        """Test evaluating coherence for fact with no tags"""
        self.registry.register_fact(self.no_tags_fact)
        result = self.validation_service.evaluate_coherence(self.no_tags_fact)
        
        self.assertIsInstance(result, ValidationResult)
        self.assertEqual(result.fact_id, 'test_003')
        # Should have lower confidence due to missing tags
        self.assertGreater(len(result.findings), 0)
    
    def test_validate_all_facts(self):
        """Test validating all facts in registry"""
        self.registry.register_fact(self.valid_fact)
        self.registry.register_fact(self.short_fact)
        self.registry.register_fact(self.no_tags_fact)
        
        results = self.validation_service.validate_all_facts()
        
        self.assertEqual(len(results), 3)
        self.assertTrue(all(isinstance(r, ValidationResult) for r in results))
    
    def test_get_validation_summary(self):
        """Test getting validation summary"""
        self.registry.register_fact(self.valid_fact)
        self.registry.register_fact(self.short_fact)
        
        self.validation_service.validate_all_facts()
        summary = self.validation_service.get_validation_summary()
        
        self.assertEqual(summary['total_validated'], 2)
        self.assertIn('coherent', summary)
        self.assertIn('suspicious', summary)
        self.assertIn('noise', summary)
        self.assertIn('average_confidence', summary)
        self.assertIn('coherence_rate', summary)
    
    def test_get_validation_summary_empty(self):
        """Test getting validation summary with no validations"""
        summary = self.validation_service.get_validation_summary()
        
        self.assertEqual(summary['total_validated'], 0)
        self.assertEqual(summary['coherent'], 0)
        self.assertEqual(summary['average_confidence'], 0.0)
    
    def test_validation_status_enum(self):
        """Test ValidationStatus enum values"""
        self.assertEqual(ValidationStatus.COHERENT.value, "coherent")
        self.assertEqual(ValidationStatus.NOISE.value, "noise")
        self.assertEqual(ValidationStatus.SUSPICIOUS.value, "suspicious")
        self.assertEqual(ValidationStatus.UNVALIDATED.value, "unvalidated")
    
    def test_validation_result_confidence_bounds(self):
        """Test ValidationResult confidence must be between 0 and 1"""
        with self.assertRaises(ValueError):
            ValidationResult(
                fact_id="test",
                status=ValidationStatus.COHERENT,
                confidence=1.5,
                findings=[],
                metadata={}
            )
        
        with self.assertRaises(ValueError):
            ValidationResult(
                fact_id="test",
                status=ValidationStatus.COHERENT,
                confidence=-0.1,
                findings=[],
                metadata={}
            )
    
    def test_validation_rules_initialization(self):
        """Test that default validation rules are initialized"""
        self.assertGreater(len(self.validation_service.validation_rules), 0)
        self.assertTrue(all(callable(rule) for rule in self.validation_service.validation_rules))
    
    def test_check_statement_length_rule(self):
        """Test statement length validation rule"""
        # Too short
        short_fact = Fact(
            id="test",
            category="test",
            statement="Hi",
            verified=True,
            timestamp=datetime.now(),
            tags=["test"]
        )
        result = self.validation_service._check_statement_length(short_fact)
        self.assertFalse(result['passed'])
        
        # Valid length
        result = self.validation_service._check_statement_length(self.valid_fact)
        self.assertTrue(result['passed'])
    
    def test_check_category_validity_rule(self):
        """Test category validity validation rule"""
        result = self.validation_service._check_category_validity(self.valid_fact)
        self.assertTrue(result['passed'])
    
    def test_check_tag_coherence_rule(self):
        """Test tag coherence validation rule"""
        result = self.validation_service._check_tag_coherence(self.valid_fact)
        self.assertTrue(result['passed'])
        
        # Test fact with no tags
        result = self.validation_service._check_tag_coherence(self.no_tags_fact)
        self.assertFalse(result['passed'])
    
    def test_analyze_tag_coherence(self):
        """Test tag coherence analysis"""
        # Valid tags
        score = self.validation_service._analyze_tag_coherence(self.valid_fact)
        self.assertGreater(score, 0.0)
        self.assertLessEqual(score, 1.0)
        
        # No tags
        score = self.validation_service._analyze_tag_coherence(self.no_tags_fact)
        self.assertEqual(score, 0.0)
        
        # Too many tags
        many_tags_fact = Fact(
            id="test",
            category="test",
            statement="Test",
            verified=True,
            timestamp=datetime.now(),
            tags=[f"tag{i}" for i in range(15)]
        )
        score = self.validation_service._analyze_tag_coherence(many_tags_fact)
        self.assertLess(score, 1.0)
    
    def test_validation_result_stored(self):
        """Test that validation results are stored"""
        self.registry.register_fact(self.valid_fact)
        result = self.validation_service.evaluate_coherence(self.valid_fact)
        
        self.assertIn('test_001', self.validation_service.validation_results)
        stored_result = self.validation_service.validation_results['test_001']
        self.assertEqual(stored_result.fact_id, result.fact_id)
        self.assertEqual(stored_result.status, result.status)


if __name__ == '__main__':
    unittest.main()
