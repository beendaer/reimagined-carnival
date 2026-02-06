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

Open [http://localhost:8000/gui](http://localhost:8000/gui) in your browser. The GUI lets you submit text feed content, supply the API key, and view the validation output plus action results.

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

## Case Studies in Organisational Values and Ethical Systems

Based on 12 sources.

| Organisation or Entity | Core Values or Principles | Operational Strategy | Ethical Framework | Social or Industrial Impact | Outcome of Value Alignment | Source |
| --- | --- | --- | --- | --- | --- | --- |
| BBFB Master Project | Zero-AI Project Governance, structural logic, and methodology persistence. | Implementing 'Zero-AI' maintenance rules: 00-99 numbering, ISO Date file naming, and 'Source vs. Build' folder isolation. | Human-Centric / Systemic Logic (Strict distinction between human logic and machine execution). | System remains self-sorting, easy to audit, and independent of specific software languages; ensures project history transparency. | Successful (Guaranteed longevity, manual auditability, and project control without AI assistants). | `[Source_Number]`, `[1]` |
| CVS Health (CVS Pharmacy) | Public Health, Corporate Integrity, Innovation, Collaboration, and Accountability. | Stopped selling all tobacco products in stores as of October 2014. | Traditional / Moral (Leadership Values). | Enhanced consumer trust and alignment with the purpose of "helping people on their path to better health". | Successful (Brand elevation through authentic behaviour). | `[Source_Number]`, `[2]` |
| Environmental Managers (under Environment Act 1986) | Intrinsic values of ecosystems vs. placed (assigned) quality values. | Creating content inventories and a 'full and balanced account' of both inherent worth and human preferences in resource management. | Mixed (Biocentric/Ecocentric vs. Anthropocentric). | Legal requirement to balance biophysical foundations with monetary metrics and economic utility. | Conflict (Systemic subordination of nature to monetary metrics; inherent tension regarding mathematical incommensurability). | `[Source_Number]`, `[3]` |
| Athleta | Sustainability and social empowerment ("Sisterhood elevates"). | Uses sustainable fibres for 60% of materials; diverts 70% of waste from landfills; invests in Gap’s P.A.C.E. program for women's advancement. | Intrinsic (Environmental Sustainability and Social Empowerment). | Reduced environmental waste, certified B Corp status, and improved life skills for female employees. | Successful (Alignment of business practices with sustainability and community impact values). | `[2]` |
| Black Lives Matter (BLM) | Solidarity with Palestinians; commitment to ending settler-colonialism in all forms. | Standing in solidarity with Palestinians; advocating for Palestinian liberation; anti-Israel activism. | Marxist-Adjacent | Disenfranchisement of Jews from their historic homeland; spread of BDS (Boycott, Divestment, Sanctions) movement. | Leads to conflict; accused of anti-Semitism and anti-American sentiment. | `[4]` |
| New York Police Department (NYPD) | Public safety; proactive policing to reduce crime. | Implementation of 'Stop and Frisk' (Terry stops); disbanding specific units in response to public pressure. | Traditional (Inferred) | Racial disparities in stops (59% Black vs 9% White in 2019); loss of community trust. | Conflict; led to class action (Floyd v. City of New York) and disbandment of units. | `[4]` |
| Kleros | Decentralised justice; Thomas Schelling’s 'focal points' theory. | Jury selection of anonymous jurors based on industry specialisation to vote on smart contract disputes. | Technological / Decentralised Justice | Facilitation of online dispute resolution for e-commerce and insurance. | Successful within smart contract platforms; questionable enforceability in national courts. | `[4]` |
| Didi Global Inc. | Information security; domestic compliance; personal information protection. | Listing in the US followed by a 'low-profile' IPO; subsequent delisting and consideration of Hong Kong listing. | National Security / Regulatory Compliance | Sanctions by the Cyberspace Administration of China (CAC); removal of apps; stock price slump. | Conflict; led to massive financial loss and investor class actions in the US. | `[4]` |
| Red Guards (Cultural Revolution) | Mao Zedong Thought; anti-revisionism; anti-bourgeois. | Writing 'Dazibao' (big-character posters); public rituals of humiliation; 'xuexi ban' (study groups). | Marxist-Leninist | Destruction of social fabric; widespread suicides; silencing of dissent. | Successful in political purging; led to historic tragedy and eventual banning of posters. | `[4]` |
| Chinese Judiciary (Network Defamation) | Personal dignity; protection of reputation; social order. | Quantifying 'serious circumstances' (e.g., 5,000 views or 500 reposts) for criminal prosecution of online slander. | Continental Civil Law | Criminal sentencing for cyber-offenders; deterrence of language violence. | Successful; ensured judicial protection of reputation in the digital age. | `[4]` |
| Thomas M. Cooley Law School | Objective reasonable reliance (Legal doctrine). | Publishing misleading employment statistics (80% employment rate) including part-time and non-legal work. | Instrumental (Market-based outcomes over moral duty). | Legal precedent allowing fraudsters to escape liability if a 'reasonable person' would not have fallen for the fraud. | Successful for the entity (Dismissed on pleadings), but led to industrial conflict (Class action lawsuits). | `[Source_Number]` |
| Personalised Recommendation Platforms (Xiaohongshu/Douyin) | User Autonomy and Algorithmic Relevance. | Users employing 'Intentional Implicit Feedback' (fast-skipping, intentional clicks) to disrupt echo chambers. | Instrumental (User agency vs. Algorithmic 'spying'). | Increased content diversity and consumer control over the 'information cocoon'. | Mixed (Increased user sense of agency but potential for inaccurate user profiling). | `[Source_Number]` |
| Spiritualist Church (Reverend Lillian Lee) | Intended Reliance (Old Common Law Rule). | Purposefully exploiting a victim's unreasonable beliefs (spiritualism) to induce financial actions. | Traditional Moral (Culpable intent). | Protection of gullible victims under the law of deceit. | Conflict (Led to litigation and initial reversal of dismissal). | `[Source_Number]` |
| Everlane | Exceptional quality, ethical factories, and radical transparency. | Encouraged employees not to unionise despite complaints of low pay and unpredictable scheduling. | Instrumental (Market-Driven Transparency). | Erosion of employee and consumer trust. | Conflict; led to unionisation efforts and public misalignment. | `[2]` |
| Beehive | Sustainability and supporting local vendors. | Began serving Well Rooted Teas from local farms using sustainable practices. | Instrumental (Local Economic Support). | Support for regional sustainable farming and internal value embrace. | Successful (Integration of values into daily office operations). | `[2]` |

Sources:

- `[1]` [ROOT] 📁 BBFB_Master_Project.md.pdf
- `[2]` 4 Ways Organizational Values Can Fuel Decision-Making - Beehive
- `[3]` allchachatt
- `[4]` vol 2 no 2 summer 2022 - International Journal of Law, Ethics, and Technology

## Summary

The TAAS Monolith provides:
- ✅ Coherent fact management
- ✅ Testing as a Service capabilities
- ✅ Centralized orchestration
- ✅ Comprehensive testing
- ✅ Industry best practices

For more details, see [ARCHITECTURE.md](ARCHITECTURE.md).
