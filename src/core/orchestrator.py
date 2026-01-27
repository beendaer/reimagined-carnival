"""
Monolith Orchestrator - Central coordination for TAAS monolith
Manages the integration of all components following best practices
"""
from typing import Dict, Any, List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.facts_registry import FactsRegistry
from services.test_service import TestService
from services.validation_service import ValidationService, ValidationResult
from models.fact import Fact


class MonolithOrchestrator:
    """
    Central orchestrator for the TAAS monolith.
    Coordinates between facts registry and test services.
    Follows the facade pattern to provide a unified interface.
    """
    
    def __init__(self):
        self.facts_registry = FactsRegistry()
        self.test_service = TestService(self.facts_registry)
        self.validation_service = ValidationService(self.facts_registry)
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the monolith with default configuration"""
        if self._initialized:
            return
        
        # Initialize with foundational facts
        self._load_default_facts()
        self._initialized = True
    
    def _load_default_facts(self) -> None:
        """Load default determined facts into the registry"""
        from datetime import datetime
        
        default_facts = [
            Fact(
                id="fact_001",
                category="architecture",
                statement="Monolithic architecture provides coherence through centralized coordination",
                verified=True,
                timestamp=datetime.now(),
                tags=["architecture", "design", "monolith"]
            ),
            Fact(
                id="fact_002",
                category="testing",
                statement="TAAS enables scalable testing through service-oriented interfaces",
                verified=True,
                timestamp=datetime.now(),
                tags=["testing", "taas", "services"]
            ),
            Fact(
                id="fact_003",
                category="coherence",
                statement="Facts registry maintains single source of truth for determined facts",
                verified=True,
                timestamp=datetime.now(),
                tags=["coherence", "facts", "registry"]
            ),
            Fact(
                id="fact_004",
                category="best_practices",
                statement="Following industry patterns ensures maintainability and scalability",
                verified=True,
                timestamp=datetime.now(),
                tags=["best_practices", "patterns", "scalability"]
            )
        ]
        
        for fact in default_facts:
            self.facts_registry.register_fact(fact)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        coherence_report = self.facts_registry.get_coherence_report()
        test_summary = self.test_service.get_test_summary()
        validation_summary = self.validation_service.get_validation_summary()
        
        return {
            'initialized': self._initialized,
            'facts': coherence_report,
            'tests': test_summary,
            'validation': validation_summary,
            'coherence_verified': self.test_service.verify_fact_coherence()
        }
    
    def register_and_test_fact(self, fact: Fact) -> Dict[str, Any]:
        """Register a fact and verify coherence"""
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
                'error': str(e)
            }
    
    def execute_tests(self) -> Dict[str, Any]:
        """Execute all registered tests and return results"""
        results = self.test_service.run_all_tests()
        summary = self.test_service.get_test_summary()
        
        return {
            'summary': summary,
            'results': [
                {
                    'test_id': r.test_id,
                    'status': r.status.value,
                    'message': r.message,
                    'duration_ms': r.duration_ms
                }
                for r in results
            ]
        }
    
    def validate_fact(self, fact_id: str) -> Dict[str, Any]:
        """
        Perform third-party validation on a specific fact.
        Investigates, checks records, and evaluates coherence.
        Best practice: validate facts before trusting them.
        """
        fact = self.facts_registry.get_fact(fact_id)
        if not fact:
            return {
                'success': False,
                'error': f"Fact {fact_id} not found"
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
        Validate all facts in the registry.
        Best practice: comprehensive validation of entire dataset.
        """
        results = self.validation_service.validate_all_facts()
        summary = self.validation_service.get_validation_summary()
        
        return {
            'summary': summary,
            'results': [
                {
                    'fact_id': r.fact_id,
                    'status': r.status.value,
                    'confidence': r.confidence,
                    'findings': r.findings
                }
                for r in results
            ]
        }
    
    def register_and_validate_fact(self, fact: Fact) -> Dict[str, Any]:
        """
        Register a fact with third-party validation.
        Best practice: validate before committing to registry.
        """
        try:
            # First, validate the fact before registering
            pre_validation = self.validation_service.evaluate_coherence(fact)
            
            # Only register if validation passes coherence threshold
            if pre_validation.confidence < 0.5:
                return {
                    'success': False,
                    'error': 'Fact failed validation - appears to be noise',
                    'validation': {
                        'status': pre_validation.status.value,
                        'confidence': pre_validation.confidence,
                        'findings': pre_validation.findings
                    }
                }
            
            # Register the fact
            self.facts_registry.register_fact(fact)
            
            # Verify coherence
            coherence_ok = self.test_service.verify_fact_coherence()
            
            return {
                'success': True,
                'fact_id': fact.id,
                'coherence_maintained': coherence_ok,
                'validation': {
                    'status': pre_validation.status.value,
                    'confidence': pre_validation.confidence,
                    'findings': pre_validation.findings
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

