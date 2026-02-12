# Changelog

All notable changes to reimagined-carnival will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- PostgreSQL preparation documentation (`docs/DATABASE_PREPARATION.md`)
- Azure deployment guide (`docs/AZURE_DEPLOYMENT.md`)
- Python 3.11 and 3.12 support in CI/CD pipeline
- Test job in CI/CD pipeline with matrix testing
- Docker build validation in CI/CD
- Flake8 linting execution in CI pipeline
- Redis client dependency for future caching implementation
- Gunicorn for production-ready WSGI server
- python-dotenv for environment variable management
- psycopg2-binary for PostgreSQL database support
- Local/CI testing notes in workflow comments
- CHANGELOG.md for tracking project changes

### Changed
- Root Dockerfile: Fixed Python 3.14 (non-existent) → Python 3.12-slim
- Root Dockerfile: Changed from multi-stage to single-stage build
- infra/docker/Dockerfile: Updated from alpine to slim, port 3000→8000
- requirements.txt: Added version pins for production stability
- requirements.txt: Updated python-multipart from 0.0.17 to 0.0.22 (security fix)
- CI/CD workflow: Removed duplicate checkout/setup-python steps
- CI/CD workflow: Added proper Python test execution
- CI/CD workflow: Added flake8 execution (was installed but not run)

### Fixed
- CI/CD duplicate actions/checkout@v6 and actions/setup-python@v6 declarations
- Docker Python version mismatch (3.14 doesn't exist)
- Docker multi-stage build path inconsistency (copying from 3.12 to 3.14)
- infra/docker/Dockerfile port mismatch (3000 vs 8000 standard)
- Security vulnerability in python-multipart < 0.0.22 (CVE-2024-XXXXX)
- Missing flake8 execution in CI (was installed but never run)
- Missing test job in CI pipeline

### Security
- Updated python-multipart to 0.0.22+ to fix:
  - Arbitrary File Write via Non-Default Configuration (versions < 0.0.22)
  - Denial of Service via deformation multipart/form-data boundary (versions < 0.0.18)

## [0.1.0] - 2026-02-11

### Initial State
- FastAPI validation endpoint operational
- 6-pattern deception detection system (811 LOC)
- 130+ unit and integration tests passing
- Deployed on Render.com (free tier)
- API key authentication
- In-memory storage only
- Python 3.11+ support

### Known Issues at 2026-02-11
- No database persistence
- No rate limiting
- No monitoring/alerts
- No usage analytics
- CI doesn't run tests
- CI doesn't execute flake8
- Two conflicting Dockerfiles

---

## Version History

### Version Numbering
- **Major.Minor.Patch** (Semantic Versioning)
- Major: Breaking changes
- Minor: New features, backward compatible
- Patch: Bug fixes, backward compatible

### Release Dates
- 2026-02-12: Operational readiness improvements (this release)
- 2026-02-11: Initial stable state documented

---

## Categories

### Added
New features or capabilities

### Changed
Changes to existing functionality

### Deprecated
Soon-to-be-removed features

### Removed
Removed features

### Fixed
Bug fixes

### Security
Security-related changes

---

**Note:** This CHANGELOG follows the CLI-centric, automation-first approach of the project. All changes should be verifiable via git history and scriptable deployment procedures.
