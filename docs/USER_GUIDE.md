# TAAS Monolith - User Guide

## Introduction

Welcome to the TAAS (Testing as a Service) Monolith! This system provides a coherent framework for managing determined facts within a monolithic architecture while offering comprehensive testing capabilities.

## Quick Start

### Running the Demo

```bash
cd /path/to/reimagined-carnival
python src/main.py
```

This will:
1. Initialize the monolith with default facts
2. Register and execute tests
3. Display system status and coherence reports
4. Demonstrate fact management capabilities

### Running the Text Feed Testing GUI

Start the API server, then open the GUI to submit text and see action results:

```bash
uvicorn src.api:app --reload
```

Open [http://localhost:8000/gui](http://localhost:8000/gui) in your browser. The GUI lets you submit text feed content, supply the API key when configured (or enable `ALLOW_OPEN_ACCESS=true` for local testing), and view the validation output plus action results.

## Core Concepts

### Facts

A **Fact** is a determined statement that maintains coherence within the monolith. Each fact has:

- **ID**: Unique identifier
- **Category**: Organizational grouping
- **Statement**: The factual statement
- **Verified**: Whether the fact has been verified
- **Timestamp**: When the fact was created/updated
- **Tags**: Searchable metadata tags

### Facts Registry

The **Facts Registry** is the single source of truth for all facts in the system. It ensures:
- No duplicate facts
- Category-based organization
- Query capabilities
- Data coherence

### Test Service (TAAS)

The **Test Service** provides Testing as a Service capabilities:
- Register and execute test cases
- Verify fact coherence
- Generate test reports
- Track test results

## Usage Examples

### Creating and Registering Facts

```python
from datetime import datetime
from src.models.fact import Fact
from src.core.facts_registry import FactsRegistry

# Create a fact
fact = Fact(
    id="my_fact_001",
    category="business_logic",
    statement="User authentication requires valid credentials",
    verified=True,
    timestamp=datetime.now(),
    tags=["auth", "security"]
)

# Register the fact
registry = FactsRegistry()
registry.register_fact(fact)
```

### Querying Facts

```python
from src.core.facts_registry import FactsRegistry

registry = FactsRegistry()

# Get a specific fact
fact = registry.get_fact("my_fact_001")

# Get all facts in a category
auth_facts = registry.get_facts_by_category("business_logic")

# Get all verified facts
verified = registry.get_verified_facts()

# Get coherence report
report = registry.get_coherence_report()
print(f"Total facts: {report['total_facts']}")
print(f"Verified facts: {report['verified_facts']}")
```

### Using the Test Service

```python
from src.services.test_service import TestService
from src.core.facts_registry import FactsRegistry

# Initialize test service
registry = FactsRegistry()
test_service = TestService(registry)

# Register a test
def test_user_authentication():
    fact = registry.get_fact("my_fact_001")
    assert fact is not None
    assert fact.verified == True

test_service.register_test("test_auth", test_user_authentication)

# Run the test
result = test_service.run_test("test_auth")
print(f"Test status: {result.status}")

# Run all tests
all_results = test_service.run_all_tests()

# Get summary
summary = test_service.get_test_summary()
print(f"Success rate: {summary['success_rate']}%")
```

### Using the Orchestrator

```python
from src.core.orchestrator import MonolithOrchestrator
from src.models.fact import Fact
from datetime import datetime

# Initialize orchestrator
orchestrator = MonolithOrchestrator()
orchestrator.initialize()

# Get system status
status = orchestrator.get_system_status()
print(status)

# Register and test a fact
new_fact = Fact(
    id="new_fact",
    category="test",
    statement="Orchestrator manages all components",
    verified=True,
    timestamp=datetime.now(),
    tags=["orchestrator"]
)

result = orchestrator.register_and_test_fact(new_fact)
print(f"Success: {result['success']}")
print(f"Coherence maintained: {result['coherence_maintained']}")

# Execute all tests
test_results = orchestrator.execute_tests()
print(test_results['summary'])
```

## Running Tests

### Unit Tests

Run individual unit tests:

```bash
# Test Fact model
python -m unittest tests/unit/test_fact.py

# Test Facts Registry
python -m unittest tests/unit/test_facts_registry.py

# Test Test Service
python -m unittest tests/unit/test_test_service.py
```

### Integration Tests

Run integration tests:

```bash
python -m unittest tests/integration/test_monolith.py
```

### All Tests

Run all tests:

```bash
python -m unittest discover tests
```

## Configuration

Configuration is managed in `config/settings.py`:

```python
MONOLITH_CONFIG = {
    'name': 'TAAS Monolith',
    'version': '1.0.0',
    'facts_registry': {
        'enable_persistence': True,
        'auto_verify': True,
        'max_facts': 10000
    },
    'test_service': {
        'parallel_execution': False,
        'timeout_seconds': 30,
        'retry_failed_tests': False
    }
}
```

## Best Practices

1. **Always verify facts**: Set `verified=True` only for confirmed facts
2. **Use descriptive categories**: Organize facts logically
3. **Add meaningful tags**: Facilitate searching and filtering
4. **Test regularly**: Use the Test Service to verify coherence
5. **Check coherence reports**: Monitor system health

## Troubleshooting

### Fact Registration Fails

**Problem**: ValueError when registering a fact

**Solution**: Ensure the fact has a unique ID and all required fields

### Test Failures

**Problem**: Tests failing unexpectedly

**Solution**: Check coherence report and verify all facts are properly registered

### Singleton Issues

**Problem**: Registry not maintaining state

**Solution**: Use `FactsRegistry()` to get the singleton instance, don't create new instances manually

## Advanced Usage

### Exporting Facts

```python
from pathlib import Path
from src.core.facts_registry import FactsRegistry

registry = FactsRegistry()
registry.export_facts(Path("facts_backup.json"))
```

### Importing Facts

```python
from pathlib import Path
from src.core.facts_registry import FactsRegistry

registry = FactsRegistry()
registry.import_facts(Path("facts_backup.json"))
```

## Summary

The TAAS Monolith provides:
- ✅ Coherent fact management
- ✅ Testing as a Service capabilities
- ✅ Centralized orchestration
- ✅ Comprehensive testing
- ✅ Industry best practices

For more details, see [ARCHITECTURE.md](ARCHITECTURE.md).
