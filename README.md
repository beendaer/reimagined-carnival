# reimagined-carnival

## TAAS Monolith - Testing as a Service with Coherent Facts

reimagined-carnival is a monolithic architecture implementing Testing as a Service (TAAS) with a coherent facts registry. This project demonstrates industry best practices for maintaining determined facts within a unified system while providing comprehensive testing capabilities.

## Overview

This monolith provides:

- **Facts Registry**: Single source of truth for determined facts
- **Test Service**: Testing as a Service (TAAS) implementation
- **Validation Service**: Third-party validation for fact quality assurance
- **Deception Detection**: AI-powered detection of deceptive patterns in text
- **Monolith Orchestrator**: Centralized coordination of all components
- **Coherence Verification**: Ensures facts maintain integrity across the system

## Key Features

✅ **Coherent Fact Management**: Centralized registry maintaining single source of truth  
✅ **Testing as a Service**: Built-in test execution and verification  
✅ **Third-Party Validation**: Investigate, check records, and evaluate coherence vs noise  
✅ **Deception Detection**: 6-pattern ontology detecting user corrections, facade metrics, hallucinations, and more  
✅ **Industry Best Practices**: Following established patterns and procedures  
✅ **Comprehensive Testing**: 130+ unit and integration tests included  
✅ **Type Safety**: Full type annotations for better development experience  
✅ **Documentation**: Detailed architecture, deception patterns, and user guides  

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

### Process Product Data

Washing machine extraction data is stored in `data/extracted-washing-machines.json`.
The converted RawProductData payload is available in `data/raw-washing-machines.json`
and can be submitted to the API endpoint:

```bash
curl -X POST http://localhost:8000/api/process-products \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d @data/raw-washing-machines.json
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
│   │   ├── deception_detector.py # Deception detection service
│   │   ├── test_service.py       # TAAS implementation
│   │   └── validation_service.py # Third-party validation
│   ├── utils/
│   │   └── helpers.py            # Utility functions
│   └── main.py                   # Demo application
├── tests/
│   ├── unit/                     # Unit tests
│   │   ├── test_deception_detector.py
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
    ├── DECEPTION_PATTERNS.md     # Deception detection guide
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

### Using Deception Detection

```python
from services.deception_detector import (
    detect_user_correction,
    detect_facade_of_competence,
    detect_unverified_claims,
    detect_all_patterns
)

# Detect user corrections
result = detect_user_correction("That's wrong, it's not deployed")
if result.detected:
    print(f"Deception type: {result.deception_type}")
    print(f"Probability: {result.probability}")
    print(f"Matched phrases: {result.matched_phrases}")

# Detect facade of competence
metrics = {'accuracy': 1.0, 'recall': 1.0, 'precision': 1.0}
result = detect_facade_of_competence(metrics, external_validation=None)
if result.detected:
    print(f"Facade detected with {result.probability} probability")

# Detect unverified claims
text = "Deployed at https://example.com"
result = detect_unverified_claims(text)
if result.detected:
    print(f"Unverified claims require validation")

# Detect all patterns at once
results = detect_all_patterns("That's wrong, deployed at https://test.com")
for r in results:
    if r.detected:
        print(f"{r.deception_type}: {r.probability}")
```

### Using Input Validation with Deception Detection

```python
from src.main import validate_input

# Validate input text
result = validate_input("That's incorrect, it shows 404", context="testing")
print(f"Coherence score: {result['coherence_score']}")
print(f"Deception detected: {result['deception_detected']}")
print(f"Deception type: {result['deception_type']}")
print(f"Deception probability: {result['deception_probability']}")
print(f"Matched phrases: {result['details']['matched_correction_phrases']}")
```

## Testing the Protected Validation Endpoint

The `/validate` endpoint requires API key authentication via the `x-api-key` header when the `API_KEY` environment variable is configured. If `API_KEY` is unset, you can enable open mode for local development by setting `ALLOW_OPEN_ACCESS=true`.

### Example Request
```bash
curl -X POST https://taas-validation.onrender.com/validate \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "input_text": "This is a coherent factual statement.",
    "context": "TAAS verification"
  }'
```

### Expected Response
```json
{
  "validation": {
    "coherence_score": 0.85,
    "noise_detected": false,
    "validation_passed": true,
    "deception_detected": false,
    "deception_type": null,
    "deception_probability": 0.0,
    "details": {
      "status": "coherent",
      "findings": [],
      "matched_correction_phrases": [],
      "metadata": {
        "text_length": 39,
        "word_count": 6,
        "context": "TAAS verification"
      }
    }
  }
}
```

### Authentication Error
When `API_KEY` is configured (and open access is not enabled), requests without a valid `x-api-key` header return:
```json
{"detail": "Invalid or missing API key"}
```

### Local Testing
To run the API locally:
```bash
# (Optional) Set API key environment variable to enable authentication
export API_KEY=your_secure_api_key

# (Optional) Allow open access when API_KEY is not configured
export ALLOW_OPEN_ACCESS=true

# Install dependencies
pip install -r requirements.txt

# Run the API server
uvicorn src.api:app --reload --port 8000

# Test the endpoint (include the header if API_KEY is set)
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_secure_api_key" \
  -d '{"input_text": "This is a test.", "context": "local"}'
```

## Documentation

### Project Status & Operations
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)**: Comprehensive project status, features, architecture, and deployment info
- **[MEMORY_UPDATE_GUIDE.md](MEMORY_UPDATE_GUIDE.md)**: Session recap and memory update workflow guide
- **[CHANGELOG.md](CHANGELOG.md)**: Track all project changes and releases

### Technical Documentation
- **[Architecture Guide](docs/ARCHITECTURE.md)**: Detailed system architecture
- **[User Guide](docs/USER_GUIDE.md)**: Comprehensive usage instructions
- **[Deception Patterns Guide](docs/DECEPTION_PATTERNS.md)**: Complete deception detection documentation
- **[Third-Party Validation Guide](docs/THIRD_PARTY_VALIDATION.md)**: Documentation structure for validation

### Deployment & Infrastructure
- **[Azure Deployment Guide](docs/AZURE_DEPLOYMENT.md)**: Complete Azure deployment guide with CLI commands
- **[Database Preparation](docs/DATABASE_PREPARATION.md)**: PostgreSQL migration preparation and strategy

### Incident Reports
- **[CHAOS_ANALYSIS.md](CHAOS_ANALYSIS.md)**: Analysis of Feb 2026 code bloat incident
- **[RECOVERY_PLAN.md](RECOVERY_PLAN.md)**: Recovery plan from code cascade

## Design Patterns

This project implements several industry-standard patterns:

- **Singleton Pattern**: Facts Registry for system-wide coherence
- **Facade Pattern**: Orchestrator for simplified access
- **Data Transfer Object**: Fact model for data encapsulation
- **Service Layer**: Test Service for business logic

## Requirements

- Python 3.11+ (currently supports 3.11 and 3.12)
- Dependencies listed in requirements.txt with version pins for production stability
- PostgreSQL driver included (prepared for future database integration)
- Redis client included (prepared for future caching)

### Key Dependencies
- FastAPI >= 0.115.0
- Uvicorn >= 0.32.0
- Requests >= 2.32.0
- httpx >= 0.27.0 (for API tests)
- psycopg2-binary >= 2.9.9 (PostgreSQL support, not yet used)
- redis >= 5.2.0 (caching support, not yet used)

## Development & Operations

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run local server with auto-reload
uvicorn src.api:app --reload --port 8000

# Run with open access (no API key required)
ALLOW_OPEN_ACCESS=true uvicorn src.api:app --reload --port 8000

# Run tests
python -m unittest discover tests/ -v

# Run specific test module
python3 -m unittest tests.unit.test_deception_detector -v

# Run linting
flake8 src/ tests/ --max-line-length=120

# Run shellcheck on scripts
find scripts -name "*.sh" -exec shellcheck {} +
```

### Docker Operations
```bash
# Build Docker image
docker build -t reimagined-carnival:local .

# Run with Docker
docker run -p 8000:8000 reimagined-carnival:local

# Using docker-compose (development)
docker-compose -f infra/docker/docker-compose.yml up
```

### CI/CD Pipeline
```bash
# CI runs automatically on push to main, tooling/*, feature/* branches
# Local CI simulation:
python -m unittest discover tests/ -v
flake8 src/ tests/ --max-line-length=120
find scripts -name "*.sh" -exec shellcheck {} +
docker build -t reimagined-carnival:test .
```

### Deployment
- **Current:** Render.com (free tier) - `https://taas-validation.onrender.com`
- **Planned:** Azure App Service with PostgreSQL and Redis
- See [Azure Deployment Guide](docs/AZURE_DEPLOYMENT.md) for migration steps

## Testing

The monolith includes comprehensive tests:

- **Unit Tests**: Test individual components (Fact, Registry, Service, Deception Detector)
- **Integration Tests**: Test complete system integration
- **Self-Testing**: TAAS verifies its own functionality
- **Deception Detection Tests**: 65 tests covering all 6 deception patterns and 15 validation dataset cases

```bash
# Run all tests with verbose output (130+ tests)
python -m unittest discover tests -v

# Run deception detector tests specifically
python -m unittest tests.unit.test_deception_detector -v

# Run validation dataset tests
python -m unittest tests.unit.test_deception_detector.TestValidationDatasetCases -v
```

### Test Coverage
- **Total Tests:** 130+
- **Success Rate:** 100%
- **Deception Detector Tests:** 65
- **Validation Dataset Coverage:** 15/15 cases (100%)
- **False Positive Rate:** 0%

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
- ✅ Advanced deception detection with 6-pattern ontology
- ✅ 100% test coverage on validation dataset (15/15 cases)
- ✅ Industry best practices and patterns
- ✅ Comprehensive documentation and testing (130+ tests)
- ✅ Type-safe Python implementation

### Deception Detection Capabilities
- **User Corrections:** Detects explicit contradictions and corrections
- **Facade of Competence:** Identifies ungrounded perfect metrics
- **Hallucination Features:** Flags unverified URLs and deployment claims
- **Ultimate AI Lie:** Catches insistence despite contradictory evidence
- **Apology Trap:** Detects doubling down after corrections
- **Red Herring:** Identifies distraction from core issues

For detailed information, see the [documentation](docs/).
