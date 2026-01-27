"""
Monolith Orchestrator - Central coordination for TAAS monolith
Manages the integration of all components following best practices
"""
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.facts_registry import FactsRegistry
from services.test_service import TestService
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
        
        return {
            'initialized': self._initialized,
            'facts': coherence_report,
            'tests': test_summary,
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
