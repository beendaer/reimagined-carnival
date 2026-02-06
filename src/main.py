"""
Main module - Demo application and entry point
Demonstrates TAAS Monolith functionality with coherent facts
"""
from typing import Dict, Any, Optional
from datetime import datetime
from src.core.orchestrator import MonolithOrchestrator
from src.models.fact import Fact
from src.services.validation_service import ValidationStatus
from src.utils.helpers import analyze_repetition_noise

MAX_REPETITION_PENALTY = 0.7
REPETITION_PENALTY_FACTOR = 0.25


def validate_input(text: str, context: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate input text for coherence and quality
    Enhanced with deception detection
    
    This function provides API-level validation for user input,
    detecting noise vs coherent information and identifying deception patterns
    
    Args:
        text: The text to validate
        context: Optional context for validation (e.g., category)
        
    Returns:
        Dictionary with validation results including:
        - coherence_score: Score from 0.0 to 1.0
        - noise_detected: Whether input is considered noise
        - validation_passed: Whether validation passed
        - deception_detected: Whether deception was detected (NEW)
        - deception_type: Type of deception if detected (NEW)
        - deception_probability: Probability of deception (NEW)
        - details: Detailed validation information
    """
    if not isinstance(text, str):
        raise ValueError("Input text must be a string")

    # Calculate coherence score based on text characteristics
    coherence_score = 0.0
    
    # Length check
    text_length = len(text.strip())
    if text_length == 0:
        coherence_score = 0.0
    elif text_length < 5:
        coherence_score = 0.2
    elif text_length < 20:
        coherence_score = 0.5
    elif text_length < 40:
        coherence_score = 0.7
    else:
        coherence_score = 0.9
    
    # Word count bonus
    word_count = len(text.split())
    if word_count >= 5:
        coherence_score = min(1.0, coherence_score + 0.1)
    
    # Context bonus
    if context:
        coherence_score = min(1.0, coherence_score + 0.05)
    
    # Add repetition noise check
    repetition_analysis = analyze_repetition_noise(text)
    if repetition_analysis["repetition_count"] > 0:
        repetition_penalty = min(
            MAX_REPETITION_PENALTY,
            REPETITION_PENALTY_FACTOR * repetition_analysis["repetition_count"]
        )
        coherence_score *= (1.0 - repetition_penalty)

    # Add deception check
    from src.services.deception_detector import detect_user_correction
    deception = detect_user_correction(text, context)
    
    # Adjust coherence score if deception detected
    if deception.detected:
        coherence_score *= (1.0 - deception.probability * 0.3)
    
    # Determine if noise detected
    noise_detected = coherence_score < 0.5
    validation_passed = coherence_score >= 0.5
    
    # Build detailed results
    details = {
        'status': 'coherent' if validation_passed else 'noise',
        'findings': [],
        'matched_correction_phrases': deception.matched_phrases,  # NEW
        'repetition': repetition_analysis,
        'metadata': {
            'text_length': text_length,
            'word_count': word_count,
            'context': context
        }
    }
    
    if text_length < 5:
        details['findings'].append('Text is too short')
    if noise_detected:
        details['findings'].append('Input detected as noise')
    if repetition_analysis["repetition_count"] > 0:
        details['findings'].append('Repetitive token sequences detected')
    if deception.detected:
        details['findings'].append(f'Deception pattern detected: {deception.deception_type}')
    
    return {
        'coherence_score': round(coherence_score, 3),
        'noise_detected': noise_detected,
        'validation_passed': validation_passed,
        'deception_detected': deception.detected,  # NEW
        'deception_type': deception.deception_type if deception.detected else None,  # NEW
        'deception_probability': round(deception.probability, 3),  # NEW
        'details': details
    }


def print_separator():
    """Print a visual separator"""
    print("\n" + "=" * 70)


def print_section(title: str):
    """Print a section header"""
    print_separator()
    print(f"  {title}")
    print_separator()


def demo_monolith():
    """
    Demonstrate the TAAS Monolith functionality
    
    This demo shows:
    1. Monolith initialization with default facts
    2. Third-party validation of fact quality
    3. Fact registration with validation
    4. Test execution and reporting
    5. System status monitoring
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  TAAS Monolith - Testing as a Service with Coherent Facts  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Initialize orchestrator
    print_section("1. Initializing Monolith")
    orchestrator = MonolithOrchestrator()
    orchestrator.initialize()
    print("✓ Monolith initialized with default facts")
    print(f"✓ Loaded {orchestrator.facts_registry.count()} default facts")
    print(f"✓ Registered {orchestrator.test_service.get_test_count()} default tests")
    
    # Show system status
    print_section("2. System Status")
    status = orchestrator.get_system_status()
    print(f"Initialized: {status['initialized']}")
    print(f"Total Facts: {status['facts']['total_facts']}")
    print(f"Verified Facts: {status['facts']['verified_facts']}")
    print(f"Coherence Verified: {status['coherence_verified']}")
    
    # Third-party validation
    print_section("3. Third-Party Validation of Existing Facts")
    validation_results = orchestrator.validate_all_facts()
    print(f"✓ Validated {validation_results['summary']['total_validated']} facts")
    print(f"  - Coherent: {validation_results['summary']['coherent']}")
    print(f"  - Suspicious: {validation_results['summary']['suspicious']}")
    print(f"  - Noise: {validation_results['summary']['noise']}")
    print(f"  - Average Confidence: {validation_results['summary']['average_confidence'] * 100:.2f}%")
    print(f"  - Coherence Rate: {validation_results['summary']['coherence_rate']:.1f}%")
    
    # Register a new high-quality fact with validation
    print_section("4. Registering High-Quality Fact (with validation)")
    good_fact = Fact(
        id="demo_good",
        category="demo",
        statement="This is a high-quality fact with sufficient detail and proper structure",
        verified=True,
        timestamp=datetime.now(),
        tags=["demo", "quality", "coherence"]
    )
    
    result = orchestrator.register_and_validate_fact(good_fact)
    if result['success']:
        print(f"✓ Fact registered successfully: {good_fact.id}")
        print(f"  - Validation Status: {result['validation']['status']}")
        print(f"  - Confidence: {result['validation']['confidence'] * 100:.2f}%")
        print(f"  - Coherence Maintained: {result['coherence_maintained']}")
    else:
        print(f"✗ Fact rejected: {result.get('error')}")
    
    # Try to register a low-quality fact
    print_section("5. Attempting to Register Low-Quality Fact")
    bad_fact = Fact(
        id="demo_bad",
        category="demo",
        statement="Bad",  # Too short - should fail validation
        verified=False,
        timestamp=datetime.now(),
        tags=[]  # No tags
    )
    
    result = orchestrator.register_and_validate_fact(bad_fact)
    if result['success']:
        print(f"✓ Fact registered: {bad_fact.id}")
    else:
        print(f"✗ Fact rejected: {result.get('error')}")
        print(f"  - Validation Status: {result['validation']['status']}")
        print(f"  - Confidence: {result['validation']['confidence'] * 100:.2f}%")
        print(f"  - Findings: {', '.join(result['validation']['findings'])}")
        print("\n  This demonstrates noise detection and quality control!")
    
    # Execute tests
    print_section("6. Executing Tests")
    test_results = orchestrator.execute_tests()
    summary = test_results['summary']
    print(f"✓ Executed {summary['total']} tests")
    print(f"  - Passed: {summary['passed']}")
    print(f"  - Failed: {summary['failed']}")
    print(f"  - Success Rate: {summary['success_rate']:.1f}%")
    
    # Final system status with validation metrics
    print_section("7. Final System Status")
    final_status = orchestrator.get_system_status()
    print(f"Total Facts: {final_status['facts']['total_facts']}")
    print(f"Verified Facts: {final_status['facts']['verified_facts']}")
    print(f"Categories: {final_status['facts']['categories_count']}")
    print(f"\nValidation Summary:")
    print(f"  - Total Validated: {final_status['validation']['total_validated']}")
    print(f"  - Coherent: {final_status['validation']['coherent']}")
    print(f"  - Coherence Rate: {final_status['validation']['coherence_rate']:.1f}%")
    print(f"  - Average Confidence: {final_status['validation']['average_confidence'] * 100:.2f}%")
    print(f"\nTest Summary:")
    print(f"  - Total Tests: {final_status['tests']['total']}")
    print(f"  - Success Rate: {final_status['tests']['success_rate']:.1f}%")
    
    print_separator()
    print("\n✓ Demo completed successfully!")
    print("  The monolith maintains coherence across all services.\n")


if __name__ == "__main__":
    demo_monolith()
