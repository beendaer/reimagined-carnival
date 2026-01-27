# reimagined-carnival

## TAAS Monolith - Testing as a Service with Coherent Facts

reimagined-carnival is a monolithic architecture implementing Testing as a Service (TAAS) with a coherent facts registry. This project demonstrates industry best practices for maintaining determined facts within a unified system while providing comprehensive testing capabilities.

## Overview

This monolith provides:

- **Facts Registry**: Single source of truth for determined facts
- **Test Service**: Testing as a Service (TAAS) implementation
- **Validation Service**: Third-party validation for fact quality assurance
- **Monolith Orchestrator**: Centralized coordination of all components
- **Coherence Verification**: Ensures facts maintain integrity across the system

## Key Features

✅ **Coherent Fact Management**: Centralized registry maintaining single source of truth  
✅ **Testing as a Service**: Built-in test execution and verification  
✅ **Third-Party Validation**: Investigate, check records, and evaluate coherence vs noise  
✅ **Industry Best Practices**: Following established patterns and procedures  
✅ **Comprehensive Testing**: Unit and integration tests included  
✅ **Type Safety**: Full type annotations for better development experience  
✅ **Documentation**: Detailed architecture and user guides  

## Quick Start

### Run the Demo

```bash
python src/main.py
```

This demonstrates:
1. Monolith initialization with default facts
2. Third-party validation of fact quality
3. Fact registration with validation (coherent vs noise detection)
4. Test execution and reporting
5. System status monitoring

### Run Tests

```bash
# Run all tests
python -m unittest discover tests

# Run unit tests only
python -m unittest discover tests/unit

# Run integration tests
python -m unittest discover tests/integration
```

## Project Structure

```
reimagined-carnival/
├── src/
│   ├── core/
│   │   ├── facts_registry.py    # Central facts repository
│   │   └── orchestrator.py      # System orchestrator
│   ├── models/
│   │   └── fact.py               # Fact data model
│   ├── services/
│   │   ├── test_service.py       # TAAS implementation
│   │   └── validation_service.py # Third-party validation
│   ├── utils/
│   │   └── helpers.py            # Utility functions
│   └── main.py                   # Demo application
├── tests/
│   ├── unit/                     # Unit tests
│   │   ├── test_fact.py
│   │   ├── test_facts_registry.py
│   │   ├── test_test_service.py
│   │   └── test_validation_service.py
│   └── integration/              # Integration tests
│       └── test_monolith.py
├── config/
│   └── settings.py               # Configuration
└── docs/
    ├── ARCHITECTURE.md           # Architecture documentation
    └── USER_GUIDE.md             # User guide

```

## Architecture

The TAAS monolith follows a layered architecture:

```
┌─────────────────────────────────────┐
│     Monolith Orchestrator           │  (Facade Pattern)
│         (Coordination)              │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┬───────────┐
       ▼                ▼           ▼
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│   Facts     │  │    Test     │  │  Validation  │
│  Registry   │  │   Service   │  │   Service    │
│  (Singleton)│  │   (TAAS)    │  │ (3rd-party)  │
└─────────────┘  └─────────────┘  └──────────────┘
       │                │                 │
       └────────────────┴─────────────────┘
                        ▼
                 ┌────────────┐
         │    Fact    │
         │   Model    │
         └────────────┘
```

### Core Principles

1. **Monolithic Coherence**: All components work together in a unified system
2. **Single Source of Truth**: Facts Registry maintains coherence
3. **Service-Oriented**: Clear separation of concerns
4. **Test-Driven**: Built-in testing capabilities (TAAS)
5. **Quality Assurance**: Third-party validation ensures data integrity

## Usage Examples

### Managing Facts

```python
from datetime import datetime
from src.models.fact import Fact
from src.core.facts_registry import FactsRegistry

# Create and register a fact
fact = Fact(
    id="fact_001",
    category="business",
    statement="User authentication requires valid credentials",
    verified=True,
    timestamp=datetime.now(),
    tags=["auth", "security"]
)

registry = FactsRegistry()
registry.register_fact(fact)

# Query facts
fact = registry.get_fact("fact_001")
business_facts = registry.get_facts_by_category("business")
verified_facts = registry.get_verified_facts()
```

### Using Test Service

```python
from src.services.test_service import TestService

test_service = TestService()

# Register and run a test
def test_authentication():
    assert True  # Your test logic

test_service.register_test("auth_test", test_authentication)
result = test_service.run_test("auth_test")

# Get test summary
summary = test_service.get_test_summary()
print(f"Success rate: {summary['success_rate']}%")
```

### Using Validation Service

```python
from src.services.validation_service import ValidationService
from src.models.fact import Fact

validation_service = ValidationService()

# Investigate a fact
investigation = validation_service.investigate_fact(my_fact)
print(f"Statement length: {investigation['statement_length']}")
print(f"Tag coherence: {investigation['tag_coherence']}")

# Check records
records = validation_service.check_records("fact_001")
print(f"Record found: {records['found']}")

# Evaluate coherence (detect noise vs coherent information)
result = validation_service.evaluate_coherence(my_fact)
print(f"Status: {result.status.value}")
print(f"Confidence: {result.confidence}")
print(f"Findings: {result.findings}")

# Validate all facts
results = validation_service.validate_all_facts()
summary = validation_service.get_validation_summary()
print(f"Coherence rate: {summary['coherence_rate']}%")
```

### Using the Orchestrator

```python
from src.core.orchestrator import MonolithOrchestrator

orchestrator = MonolithOrchestrator()
orchestrator.initialize()

# Get system status (includes validation metrics)
status = orchestrator.get_system_status()
print(f"Total facts: {status['facts']['total_facts']}")
print(f"Coherence verified: {status['coherence_verified']}")
print(f"Validation summary: {status['validation']}")

# Validate a specific fact
validation_result = orchestrator.validate_fact("fact_001")
print(f"Validation status: {validation_result['validation']['status']}")

# Register with validation (rejects low-quality facts)
new_fact = Fact(...)
result = orchestrator.register_and_validate_fact(new_fact)
if result['success']:
    print("Fact passed validation and was registered")
else:
    print(f"Fact rejected: {result['error']}")

# Execute all tests
results = orchestrator.execute_tests()
```

## Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)**: Detailed system architecture
- **[User Guide](docs/USER_GUIDE.md)**: Comprehensive usage instructions
- **[Third-Party Validation Guide](docs/THIRD_PARTY_VALIDATION.md)**: Documentation structure for validation

## Design Patterns

This project implements several industry-standard patterns:

- **Singleton Pattern**: Facts Registry for system-wide coherence
- **Facade Pattern**: Orchestrator for simplified access
- **Data Transfer Object**: Fact model for data encapsulation
- **Service Layer**: Test Service for business logic

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)

## Testing

The monolith includes comprehensive tests:

- **Unit Tests**: Test individual components (Fact, Registry, Service)
- **Integration Tests**: Test complete system integration
- **Self-Testing**: TAAS verifies its own functionality

```bash
# Run all tests with verbose output
python -m unittest discover tests -v
```

## Contributing

This project follows industry best practices:

1. Type hints for all functions
2. Comprehensive docstrings
3. Unit and integration tests
4. Clean code principles
5. SOLID design principles

## License

This project is part of the reimagined-carnival repository.

## Summary

The TAAS Monolith demonstrates:
- ✅ Coherent fact management within a monolith
- ✅ Testing as a Service implementation
- ✅ Industry best practices and patterns
- ✅ Comprehensive documentation and testing
- ✅ Type-safe Python implementation

For detailed information, see the [documentation](docs/).
