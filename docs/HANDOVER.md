# Handover Guide
## Repository: reimagined-carnival
## Owner: @beendaer
## Quick Start
1. Clone repo
2. Run bash scripts/bootstrap.sh
3. Push to tooling/* or feature/* to trigger CI
## Infrastructure
- Docker: infra/docker/
- Terraform: infra/terraform/
- Monitoring: monitoring/
## Deployment
- Manual via GitHub Actions workflow_dispatch
- Targets: staging, production
