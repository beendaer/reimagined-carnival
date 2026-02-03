"""
Test Service - Testing as a Service (TAAS) implementation
Provides test registration, execution, and reporting capabilities
"""
from enum import Enum
from typing import Dict, List, Callable, Optional, Any
from datetime import datetime
from src.core.facts_registry import FactsRegistry


class TestStatus(Enum):
    """Test execution status enumeration"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class TestResult:
    """
    Result of a test execution
    
    Attributes:
        test_id: Identifier of the test
        status: Execution status
        message: Result message or error details
        duration: Execution duration in seconds
        timestamp: When the test was executed
    """
    
    def __init__(
        self,
        test_id: str,
        status: TestStatus,
        message: str = "",
        duration: float = 0.0
    ):
        """Initialize test result"""
        self.test_id = test_id
        self.status = status
        self.message = message
        self.duration = duration
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            'test_id': self.test_id,
            'status': self.status.value,
            'message': self.message,
            'duration': self.duration,
            'timestamp': self.timestamp.isoformat()
        }


class TestService:
    """
    Testing as a Service (TAAS) implementation
    
    Provides comprehensive testing capabilities for the monolith
    """
    
    def __init__(self, registry: Optional[FactsRegistry] = None):
        """
        Initialize the test service
        
        Args:
            registry: Facts registry instance (creates new if not provided)
        """
        self.registry = registry if registry is not None else FactsRegistry()
        self.test_cases: Dict[str, Callable] = {}
        self.test_results: Dict[str, TestResult] = {}
    
    def register_test(self, test_id: str, test_func: Callable) -> None:
        """
        Register a test case
        
        Args:
            test_id: Unique identifier for the test
            test_func: The test function to execute
        """
        self.test_cases[test_id] = test_func
    
    def run_test(self, test_id: str) -> TestResult:
        """
        Run a specific test case
        
        Args:
            test_id: The test identifier
            
        Returns:
            TestResult with execution details
            
        Raises:
            KeyError: If test_id not found
        """
        if test_id not in self.test_cases:
            raise KeyError(f"Test '{test_id}' not found")
        
        test_func = self.test_cases[test_id]
        start_time = datetime.now()
        
        try:
            test_func()
            status = TestStatus.PASSED
            message = "Test passed successfully"
        except AssertionError as e:
            status = TestStatus.FAILED
            message = f"Assertion failed: {str(e)}" if str(e) else "Assertion failed"
        except Exception as e:
            status = TestStatus.ERROR
            message = f"Error during execution: {str(e)}"
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        result = TestResult(
            test_id=test_id,
            status=status,
            message=message,
            duration=duration
        )
        
        self.test_results[test_id] = result
        return result
    
    def run_all_tests(self) -> List[TestResult]:
        """
        Run all registered test cases
        
        Returns:
            List of test results
        """
        results = []
        for test_id in self.test_cases:
            result = self.run_test(test_id)
            results.append(result)
        return results
    
    def get_test_summary(self) -> Dict[str, Any]:
        """
        Get summary of test execution results
        
        Returns:
            Dictionary containing test statistics
        """
        if not self.test_results:
            return {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0,
                'error': 0,
                'success_rate': 0.0
            }
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results.values() 
                    if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.test_results.values() 
                    if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in self.test_results.values() 
                     if r.status == TestStatus.SKIPPED)
        error = sum(1 for r in self.test_results.values() 
                   if r.status == TestStatus.ERROR)
        
        success_rate = (passed / total * 100) if total > 0 else 0.0
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'error': error,
            'success_rate': round(success_rate, 2)
        }
    
    def verify_fact_coherence(self) -> bool:
        """
        Verify that facts maintain coherence
        
        Returns:
            True if coherence is maintained
        """
        # Check if registry is accessible and has facts
        if self.registry is None:
            return False
        
        # Basic coherence check - registry should be consistent
        facts = self.registry.get_all_facts()
        
        # Verify each fact has required attributes
        for fact in facts:
            if not all([
                hasattr(fact, 'id'),
                hasattr(fact, 'category'),
                hasattr(fact, 'statement'),
                hasattr(fact, 'verified'),
                hasattr(fact, 'timestamp'),
                hasattr(fact, 'tags')
            ]):
                return False
        
        return True
    
    def clear_results(self) -> None:
        """Clear all test results"""
        self.test_results.clear()
    
    def get_test_count(self) -> int:
        """
        Get the number of registered tests
        
        Returns:
            Number of registered tests
        """
        return len(self.test_cases)
