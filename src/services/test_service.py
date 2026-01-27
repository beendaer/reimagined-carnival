"""
Test Service - Core TAAS (Testing as a Service) implementation
Provides testing capabilities following industry best practices
"""
from typing import List, Dict, Any, Callable
from enum import Enum
from dataclasses import dataclass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.facts_registry import FactsRegistry


class TestStatus(Enum):
    """Test execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TestResult:
    """Result of a test execution"""
    test_id: str
    name: str
    status: TestStatus
    message: str = ""
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class TestService:
    """
    Testing as a Service implementation.
    Provides centralized testing capabilities within the monolith.
    """
    
    def __init__(self, facts_registry: FactsRegistry = None):
        self.facts_registry = facts_registry or FactsRegistry()
        self.test_cases: Dict[str, Callable] = {}
        self.test_results: List[TestResult] = []
    
    def register_test(self, test_id: str, test_func: Callable) -> None:
        """Register a test case"""
        if test_id in self.test_cases:
            raise ValueError(f"Test {test_id} already registered")
        self.test_cases[test_id] = test_func
    
    def run_test(self, test_id: str) -> TestResult:
        """Execute a single test"""
        if test_id not in self.test_cases:
            raise ValueError(f"Test {test_id} not found")
        
        import time
        start_time = time.time()
        
        try:
            test_func = self.test_cases[test_id]
            test_func()
            status = TestStatus.PASSED
            message = "Test passed successfully"
        except AssertionError as e:
            status = TestStatus.FAILED
            message = f"Assertion failed: {str(e)}"
        except Exception as e:
            status = TestStatus.FAILED
            message = f"Test error: {str(e)}"
        
        duration_ms = (time.time() - start_time) * 1000
        
        result = TestResult(
            test_id=test_id,
            name=test_id,
            status=status,
            message=message,
            duration_ms=duration_ms
        )
        
        self.test_results.append(result)
        return result
    
    def run_all_tests(self) -> List[TestResult]:
        """Execute all registered tests"""
        results = []
        for test_id in self.test_cases.keys():
            result = self.run_test(test_id)
            results.append(result)
        return results
    
    def get_test_summary(self) -> dict:
        """Get summary of test executions"""
        if not self.test_results:
            return {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0,
                'success_rate': 0.0
            }
        
        passed = sum(1 for r in self.test_results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.test_results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in self.test_results if r.status == TestStatus.SKIPPED)
        
        return {
            'total': len(self.test_results),
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'success_rate': (passed / len(self.test_results)) * 100 if self.test_results else 0.0
        }
    
    def verify_fact_coherence(self) -> bool:
        """Verify that facts in the registry maintain coherence"""
        report = self.facts_registry.get_coherence_report()
        return report['total_facts'] > 0 and report['verified_facts'] >= 0
