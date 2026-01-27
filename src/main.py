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
    
    # Register a custom test
    def custom_fact_test():
        """Test that custom facts are properly registered"""
        fact = orchestrator.facts_registry.get_fact("fact_001")
        assert fact is not None
        assert fact.verified == True
    
    orchestrator.test_service.register_test("custom_fact_test", custom_fact_test)
    print("✓ Registered custom test case")
    print()
    
    # Add a new fact
    new_fact = Fact(
        id="fact_demo",
        category="demonstration",
        statement="This monolith demonstrates TAAS with coherent facts",
        verified=True,
        timestamp=datetime.now(),
        tags=["demo", "taas", "monolith"]
    )
    
    result = orchestrator.register_and_test_fact(new_fact)
    print(f"✓ New fact registered: {new_fact.id}")
    print(f"  Coherence maintained: {result['coherence_maintained']}")
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
    print("=" * 60)


if __name__ == "__main__":
    main()
