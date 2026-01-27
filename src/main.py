"""
Main entry point for the TAAS Monolith
Demonstrates the complete system in action
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.orchestrator import MonolithOrchestrator
from models.fact import Fact
from utils.helpers import format_report
from datetime import datetime


def main():
    """Main function to demonstrate TAAS monolith functionality"""
    print("=" * 60)
    print("TAAS Monolith - Testing as a Service")
    print("Coherent Facts within Monolithic Architecture")
    print("With Third-Party Validation")
    print("=" * 60)
    print()
    
    # Initialize orchestrator
    orchestrator = MonolithOrchestrator()
    orchestrator.initialize()
    
    print("✓ Monolith initialized successfully")
    print()
    
    # Display initial system status
    status = orchestrator.get_system_status()
    print(format_report(status, "Initial System Status"))
    print()
    
    # Demonstrate third-party validation
    print("=" * 60)
    print("THIRD-PARTY VALIDATION DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Validate existing facts
    print("Validating all existing facts...")
    validation_results = orchestrator.validate_all_facts()
    print(format_report(validation_results['summary'], "Validation Summary"))
    print()
    
    # Show individual validation results
    print("Individual Validation Results:")
    print("-" * 60)
    for result in validation_results['results'][:3]:  # Show first 3
        print(f"\nFact ID: {result['fact_id']}")
        print(f"  Status: {result['status']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Findings: {', '.join(result['findings'])}")
    print()
    
    # Register a custom test
    def custom_fact_test():
        """Test that custom facts are properly registered"""
        fact = orchestrator.facts_registry.get_fact("fact_001")
        assert fact is not None
        assert fact.verified == True
    
    orchestrator.test_service.register_test("custom_fact_test", custom_fact_test)
    print("✓ Registered custom test case")
    print()
    
    # Add a new fact with validation
    new_fact = Fact(
        id="fact_demo",
        category="demonstration",
        statement="This monolith demonstrates TAAS with coherent facts and third-party validation",
        verified=True,
        timestamp=datetime.now(),
        tags=["demo", "taas", "monolith", "validation"]
    )
    
    print("Registering new fact with validation...")
    result = orchestrator.register_and_validate_fact(new_fact)
    print(f"✓ New fact registered: {new_fact.id}")
    print(f"  Coherence maintained: {result['coherence_maintained']}")
    print(f"  Validation status: {result['validation']['status']}")
    print(f"  Validation confidence: {result['validation']['confidence']:.2%}")
    print()
    
    # Try to register a low-quality fact (should fail)
    low_quality_fact = Fact(
        id="fact_bad",
        category="test",
        statement="Bad",
        verified=False,
        timestamp=datetime.now(),
        tags=[]
    )
    
    print("Attempting to register low-quality fact (should fail)...")
    bad_result = orchestrator.register_and_validate_fact(low_quality_fact)
    print(f"✗ Registration result: {bad_result['success']}")
    if not bad_result['success']:
        print(f"  Error: {bad_result['error']}")
        print(f"  Validation status: {bad_result['validation']['status']}")
        print(f"  Validation confidence: {bad_result['validation']['confidence']:.2%}")
    print()
    
    # Execute all tests
    print("Running all tests...")
    test_results = orchestrator.execute_tests()
    print(format_report(test_results['summary'], "Test Execution Summary"))
    print()
    
    # Display final system status
    final_status = orchestrator.get_system_status()
    print(format_report(final_status, "Final System Status"))
    print()
    
    # Display facts by category
    print("Facts by Category:")
    print("-" * 60)
    for category in ["architecture", "testing", "coherence", "best_practices", "demonstration"]:
        facts = orchestrator.facts_registry.get_facts_by_category(category)
        if facts:
            print(f"\n{category.upper()}:")
            for fact in facts:
                print(f"  • {fact.statement}")
    print()
    
    print("=" * 60)
    print("TAAS Monolith demonstration completed successfully!")
    print("Third-party validation ensures data quality!")
    print("=" * 60)


if __name__ == "__main__":
    main()
