# Third-Party Validation

## Overview

The monolith includes a third-party validation capability to ensure facts remain coherent and trustworthy. This document outlines the structure for documenting that capability.

## Documentation Structure

1. **Purpose and Scope**  
   - Describe why third-party validation exists and which components participate.
2. **Validation Workflow**  
   - Investigation → Record Check → Rule Evaluation → Coherence Classification → Confidence Scoring.
3. **Interfaces**  
   - Public APIs exposed by `ValidationService` and how other components (e.g., Orchestrator) call them.
4. **Data Requirements**  
   - Required fact fields, expected tag quality, and timestamp validity.
5. **Quality Rules**  
   - Statement length bounds, category presence, tag coherence expectations.
6. **Outcomes**  
   - Possible statuses (COHERENT, SUSPICIOUS, NOISE) and how to interpret confidence values.
7. **Operational Guidance**  
   - How to run validation across all facts, view summaries, and respond to low-quality findings.

## Next Steps

- Fill each section with project-specific details and examples.
- Keep this structure aligned with `docs/ARCHITECTURE.md` and `docs/USER_GUIDE.md`.
