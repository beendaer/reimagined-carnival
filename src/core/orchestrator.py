"""
Monolith Orchestrator - Facade pattern for system coordination
Provides unified access to all monolith components
"""
from typing import Dict, Any, List
from datetime import datetime
from src.models.fact import Fact
from src.core.facts_registry import FactsRegistry
from src.services.test_service import TestService
from src.services.validation_service import ValidationService, ValidationStatus


class MonolithOrchestrator:
    """
    Monolith Orchestrator implementing the Facade pattern
    
    Provides a simplified interface to the entire monolith system,
    coordinating Facts Registry, Test Service, and Validation Service
    """
    
    def __init__(self):
        """Initialize orchestrator with all services"""
        self.facts_registry = FactsRegistry()
        self.test_service = TestService(self.facts_registry)
        self.validation_service = ValidationService(self.facts_registry)
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the monolith with default facts and tests"""
        if self._initialized:
            return
        
        # Create default facts
        default_facts = [
            Fact(
                id="default_001",
                category="architecture",
                statement="The monolith uses Singleton pattern for Facts Registry",
                verified=True,
                timestamp=datetime.now(),
                tags=["architecture", "pattern", "singleton"]
            ),
            Fact(
                id="default_002",
                category="architecture",
                statement="The orchestrator implements Facade pattern for simplified access",
                verified=True,
                timestamp=datetime.now(),
                tags=["architecture", "pattern", "facade"]
            ),
            Fact(
                id="default_003",
                category="testing",
                statement="TAAS provides comprehensive testing capabilities",
                verified=True,
                timestamp=datetime.now(),
                tags=["testing", "TAAS", "quality"]
            ),
            Fact(
                id="default_004",
                category="validation",
                statement="Third-party validation ensures fact quality and coherence",
                verified=True,
                timestamp=datetime.now(),
                tags=["validation", "quality", "coherence"]
            ),
        ]
        
        for fact in default_facts:
            # Avoid duplicate registrations if defaults already exist
            if self.facts_registry.get_fact(fact.id) is None:
                self.facts_registry.register_fact(fact)
        
        # Register default tests
        def test_registry_coherence():
            assert self.facts_registry.count() > 0
            assert all(f.id for f in self.facts_registry.get_all_facts())
        
        def test_fact_retrieval():
            fact = self.facts_registry.get_fact("default_001")
            assert fact is not None
            assert fact.id == "default_001"
        
        self.test_service.register_test("registry_coherence", test_registry_coherence)
        self.test_service.register_test("fact_retrieval", test_fact_retrieval)
        
        self._initialized = True
    
    def register_and_test_fact(self, fact: Fact) -> Dict[str, Any]:
        """
        Register a fact and verify coherence
        
        Args:
            fact: The fact to register
            
        Returns:
            Dictionary with registration results and coherence status
        """
        try:
            self.facts_registry.register_fact(fact)
            coherence_ok = self.test_service.verify_fact_coherence()
            
            return {
                'success': True,
                'fact_id': fact.id,
                'coherence_maintained': coherence_ok
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'coherence_maintained': False
            }
    
    def execute_tests(self) -> Dict[str, Any]:
        """
        Execute all registered tests
        
        Returns:
            Dictionary with test results and summary
        """
        results = self.test_service.run_all_tests()
        summary = self.test_service.get_test_summary()
        
        return {
            'results': [r.to_dict() for r in results],
            'summary': summary
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status
        
        Returns:
            Dictionary with system status information
        """
        facts_report = self.facts_registry.get_coherence_report()
        test_summary = self.test_service.get_test_summary()
        validation_summary = self.validation_service.get_validation_summary()
        
        return {
            'initialized': self._initialized,
            'facts': facts_report,
            'tests': test_summary,
            'validation': validation_summary,
            'coherence_verified': self.test_service.verify_fact_coherence()
        }
    
    def validate_fact(self, fact_id: str) -> Dict[str, Any]:
        """
        Perform third-party validation on a specific fact
        
        Args:
            fact_id: The fact identifier to validate
            
        Returns:
            Dictionary with validation results
        """
        fact = self.facts_registry.get_fact(fact_id)
        
        if fact is None:
            return {
                'success': False,
                'error': f"Fact '{fact_id}' not found"
            }
        
        # Investigate the fact
        investigation = self.validation_service.investigate_fact(fact)
        
        # Check records
        record_check = self.validation_service.check_records(fact_id)
        
        # Evaluate coherence
        validation_result = self.validation_service.evaluate_coherence(fact)
        
        return {
            'success': True,
            'fact_id': fact_id,
            'investigation': investigation,
            'record_check': record_check,
            'validation': {
                'status': validation_result.status.value,
                'confidence': validation_result.confidence,
                'findings': validation_result.findings
            }
        }
    
    def validate_all_facts(self) -> Dict[str, Any]:
        """
        Validate all facts in the registry
        
        Returns:
            Dictionary with validation results for all facts
        """
        results = self.validation_service.validate_all_facts()
        summary = self.validation_service.get_validation_summary()
        
        return {
            'results': [r.to_dict() for r in results],
            'summary': summary
        }
    
    def register_and_validate_fact(self, fact: Fact) -> Dict[str, Any]:
        """
        Register a fact with third-party validation
        Rejects low-quality facts that fail validation
        
        Args:
            fact: The fact to register and validate
            
        Returns:
            Dictionary with registration and validation results
        """
        # First, evaluate coherence before registering
        validation_result = self.validation_service.evaluate_coherence(fact)
        
        # Reject if confidence is too low (below 0.5)
        if validation_result.confidence < 0.5:
            return {
                'success': False,
                'fact_id': fact.id,
                'error': 'Fact rejected due to low quality/coherence',
                'validation': {
                    'status': validation_result.status.value,
                    'confidence': validation_result.confidence,
                    'findings': validation_result.findings
                },
                'coherence_maintained': False
            }
        
        # Register the fact
        try:
            self.facts_registry.register_fact(fact)
            coherence_ok = self.test_service.verify_fact_coherence()
            
            return {
                'success': True,
                'fact_id': fact.id,
                'coherence_maintained': coherence_ok,
                'validation': {
                    'status': validation_result.status.value,
                    'confidence': validation_result.confidence,
                    'findings': validation_result.findings
                }
            }
        except Exception as e:
            return {
                'success': False,
                'fact_id': fact.id,
                'error': str(e),
                'coherence_maintained': False,
                'validation': {
                    'status': validation_result.status.value,
                    'confidence': validation_result.confidence,
                    'findings': validation_result.findings
                }
            }
