# Operational Quick Reference

**reimagined-carnival** - CLI-Centric Operations Guide

---

## Daily Operations

### Start Development Server
```bash
# With API key authentication
export API_KEY=your_secure_key
uvicorn src.api:app --reload --port 8000

# Open access mode (development only)
ALLOW_OPEN_ACCESS=true uvicorn src.api:app --reload --port 8000
```

### Run Tests
```bash
# All tests (200 tests, ~0.07s)
python -m unittest discover tests/ -v

# Deception detector only (96 tests)
python3 -m unittest tests.unit.test_deception_detector -v

# API tests
python -m unittest tests.unit.test_api -v

# Integration tests
python -m unittest discover tests/integration -v
```

### Code Quality
```bash
# Lint Python code
flake8 src/ tests/ --max-line-length=120 --extend-ignore=E501,W503

# Check shell scripts
find scripts -name "*.sh" -exec shellcheck {} +

# Check syntax
python -m py_compile src/services/deception_detector.py
```

---

## Docker Operations

### Build
```bash
# Production build (root Dockerfile - Python 3.12-slim)
docker build -t reimagined-carnival:latest .

# Development build (infra/docker/Dockerfile)
docker build -f infra/docker/Dockerfile -t reimagined-carnival:dev .
```

### Run
```bash
# Run container
docker run -p 8000:8000 -e API_KEY=test reimagined-carnival:latest

# With environment file
docker run -p 8000:8000 --env-file .env reimagined-carnival:latest

# Using docker-compose
docker-compose -f infra/docker/docker-compose.yml up
```

### Troubleshooting
```bash
# View logs
docker logs <container_id>

# Shell into container
docker exec -it <container_id> /bin/bash

# Inspect image
docker inspect reimagined-carnival:latest
```

---

## CI/CD

### GitHub Actions Workflows
- **Lint Job:** Runs flake8 and shellcheck
- **Security Job:** Runs Trivy security scanner
- **Test Job:** Matrix testing on Python 3.11 and 3.12
- **Build Job:** Docker image build validation

### Local CI Simulation
```bash
# Run all CI checks locally
flake8 src/ tests/ --max-line-length=120 --extend-ignore=E501,W503
find scripts -name "*.sh" -exec shellcheck {} + 2>/dev/null || true
python -m unittest discover tests/ -v
docker build -t reimagined-carnival:test .
```

### Trigger CI
```bash
# Push to trigger CI
git push origin feature/your-feature

# Create PR to trigger full pipeline
gh pr create --base main --head feature/your-feature
```

---

## API Testing

### Validation Endpoint
```bash
# Test locally
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_api_key" \
  -d '{
    "input_text": "This is a test input.",
    "context": "local_testing"
  }'

# Test production (Render.com)
curl -X POST https://taas-validation.onrender.com/validate \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{
    "input_text": "Test text",
    "context": "production"
  }'
```

### Health Check
```bash
# Root endpoint
curl http://localhost:8000/

# Expected response
# {"message":"TAAS Validation Service","status":"operational"}
```

---

## Database Operations (Prepared - Not Yet Implemented)

### PostgreSQL Setup (Future)
```bash
# Local PostgreSQL with Docker
docker run --name postgres-local \
  -e POSTGRES_PASSWORD=local_dev_password \
  -e POSTGRES_DB=taas_validation \
  -p 5432:5432 \
  -d postgres:16-alpine

# Connect
psql -h localhost -U postgres -d taas_validation

# Environment variable
export DATABASE_URL="postgresql://postgres:password@localhost:5432/taas_validation"
```

### Redis Setup (Future)
```bash
# Local Redis with Docker
docker run --name redis-local \
  -p 6379:6379 \
  -d redis:7-alpine

# Test connection
redis-cli ping
```

---

## Deployment

### Render.com (Current)
```bash
# Deployment happens automatically via GitHub integration
# Configuration: render.yaml
# URL: https://taas-validation.onrender.com
```

### Azure (Planned)
```bash
# See docs/AZURE_DEPLOYMENT.md for complete guide

# Quick deploy
az webapp up \
  --name reimagined-carnival \
  --resource-group rg-reimagined-carnival-prod \
  --runtime "PYTHON:3.12"
```

---

## Monitoring & Logging

### Local Logs
```bash
# Run with debug logging
LOG_LEVEL=DEBUG uvicorn src.api:app --reload --port 8000

# View application logs
tail -f logs/app.log  # (if configured)
```

### Production Logs (Render.com)
```bash
# Via Render CLI
render logs -a taas-validation

# Via web dashboard
# https://dashboard.render.com/
```

### Future: Azure Logs
```bash
# Stream logs
az webapp log tail --name reimagined-carnival --resource-group rg-reimagined-carnival-prod

# Download logs
az webapp log download --name reimagined-carnival --resource-group rg-reimagined-carnival-prod
```

---

## Environment Variables

### Required
```bash
# API Security
API_KEY=your_secure_api_key_here

# Optional: Open access mode (development only)
ALLOW_OPEN_ACCESS=true
```

### Optional (Future PostgreSQL)
```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

### Optional (Future Redis)
```bash
REDIS_URL=redis://localhost:6379/0
```

### Optional (Logging)
```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## Troubleshooting

### Tests Failing
```bash
# Check dependencies
pip install -r requirements.txt

# Run specific failing test
python -m unittest tests.unit.test_api.TestAPIEndpoints.test_root_endpoint -v

# Check Python version
python --version  # Should be 3.11+
```

### Docker Build Failing
```bash
# Clear cache
docker builder prune -a

# Build with no cache
docker build --no-cache -t reimagined-carnival:latest .

# Check Dockerfile syntax
docker build --dry-run -t reimagined-carnival:latest .
```

### API Not Responding
```bash
# Check port availability
lsof -i :8000

# Kill process on port 8000
kill $(lsof -t -i:8000)

# Restart server
uvicorn src.api:app --reload --port 8000
```

### Import Errors
```bash
# Ensure src is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or use module syntax
python -m src.api
```

---

## Quick Commands Cheat Sheet

```bash
# Development
uvicorn src.api:app --reload                    # Start dev server
python -m unittest discover tests/ -v           # Run tests
flake8 src/ tests/ --max-line-length=120        # Lint

# Docker
docker build -t reimagined-carnival .           # Build
docker run -p 8000:8000 reimagined-carnival     # Run

# Git
git status                                       # Check status
git add .                                        # Stage all
git commit -m "message"                          # Commit
git push origin <branch>                         # Push

# API
curl http://localhost:8000/                      # Health check
curl -X POST http://localhost:8000/validate ... # Test endpoint

# Database (future)
docker run --name postgres -p 5432:5432 ...      # PostgreSQL
docker run --name redis -p 6379:6379 ...         # Redis
```

---

## Best Practices

### Before Committing
1. Run all tests: `python -m unittest discover tests/ -v`
2. Run linters: `flake8 src/ tests/`
3. Check Docker builds: `docker build -t test .`
4. Review changes: `git diff`

### Before Deploying
1. All tests pass
2. Docker image builds successfully
3. Environment variables configured
4. Database migrations ready (when applicable)
5. Monitoring configured

### Security Checklist
- [ ] API_KEY set and secure
- [ ] No secrets in code
- [ ] Dependencies up to date
- [ ] Security scan passed (Trivy)
- [ ] Database SSL enabled (future)

---

**Last Updated:** 2026-02-12  
**Maintained By:** beendaer  
**Repository:** beendaer/reimagined-carnival
