# Azure Deployment Guide

**Status:** Prepared for migration from Render.com  
**Current Platform:** Render.com (free tier)  
**Target Platform:** Azure App Service + PostgreSQL + Redis

---

## Overview

This guide prepares reimagined-carnival for production deployment on Azure. The current Render.com deployment serves as a prototype, with Azure providing production-grade infrastructure, monitoring, and scalability.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Azure Architecture                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │  Azure App       │      │  Application     │            │
│  │  Service         │─────▶│  Insights        │            │
│  │  (FastAPI)       │      │  (Monitoring)    │            │
│  └────────┬─────────┘      └──────────────────┘            │
│           │                                                  │
│           │                                                  │
│  ┌────────▼─────────┐      ┌──────────────────┐            │
│  │  PostgreSQL      │      │  Redis Cache     │            │
│  │  Flexible Server │      │  (Future)        │            │
│  └──────────────────┘      └──────────────────┘            │
│                                                              │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │  Key Vault       │      │  Log Analytics   │            │
│  │  (Secrets)       │      │  Workspace       │            │
│  └──────────────────┘      └──────────────────┘            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

### Azure CLI Installation
```bash
# Install Azure CLI (macOS)
brew install azure-cli

# Login to Azure
az login

# Verify subscription
az account show
```

### Required Azure Services
- Azure App Service (Linux, Python 3.12)
- Azure Database for PostgreSQL - Flexible Server
- Azure Cache for Redis (optional, future)
- Application Insights
- Azure Key Vault
- Log Analytics Workspace

## Resource Group Setup

```bash
# Set variables
RESOURCE_GROUP="rg-reimagined-carnival-prod"
LOCATION="eastus"
APP_NAME="reimagined-carnival"

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION \
  --tags environment=production project=taas-validation
```

## App Service Deployment

### Create App Service Plan
```bash
# Linux-based App Service Plan (B2 tier for production)
az appservice plan create \
  --name "plan-${APP_NAME}" \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --is-linux \
  --sku B2
```

### Create Web App
```bash
# Create App Service with Python 3.12
az webapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan "plan-${APP_NAME}" \
  --runtime "PYTHON:3.12"
```

### Configure App Settings
```bash
# Set environment variables
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    PYTHON_VERSION="3.12" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
    ENABLE_ORYX_BUILD="true" \
    WEBSITE_HTTPLOGGING_RETENTION_DAYS="7" \
    PORT="8000"
```

### Configure Startup Command
```bash
az webapp config set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --startup-file "uvicorn src.api:app --host 0.0.0.0 --port 8000"
```

## PostgreSQL Setup

### Create PostgreSQL Server
```bash
# Variables
POSTGRES_SERVER="${APP_NAME}-postgres"
POSTGRES_ADMIN="adminuser"
POSTGRES_DB="taas_validation"

# Create Flexible Server
az postgres flexible-server create \
  --name $POSTGRES_SERVER \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --admin-user $POSTGRES_ADMIN \
  --admin-password "<generate-secure-password>" \
  --sku-name Standard_D2s_v3 \
  --tier GeneralPurpose \
  --storage-size 32 \
  --version 16 \
  --public-access 0.0.0.0 \
  --tags environment=production

# Create database
az postgres flexible-server db create \
  --server-name $POSTGRES_SERVER \
  --resource-group $RESOURCE_GROUP \
  --database-name $POSTGRES_DB

# Configure firewall for Azure services
az postgres flexible-server firewall-rule create \
  --name $POSTGRES_SERVER \
  --resource-group $RESOURCE_GROUP \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### Connection String
```bash
# Build connection string
POSTGRES_CONN="postgresql://${POSTGRES_ADMIN}:PASSWORD@${POSTGRES_SERVER}.postgres.database.azure.com:5432/${POSTGRES_DB}?sslmode=require"

# Add to App Service
az webapp config connection-string set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --connection-string-type PostgreSQL \
  --settings DATABASE_URL="$POSTGRES_CONN"
```

## Application Insights

### Create Application Insights
```bash
# Create Log Analytics Workspace first
az monitor log-analytics workspace create \
  --resource-group $RESOURCE_GROUP \
  --workspace-name "log-${APP_NAME}"

# Create Application Insights
az monitor app-insights component create \
  --app "${APP_NAME}-insights" \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP \
  --workspace "log-${APP_NAME}"

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app "${APP_NAME}-insights" \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey -o tsv)

# Configure App Service
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY="$INSTRUMENTATION_KEY"
```

## Key Vault (Secrets Management)

### Create Key Vault
```bash
az keyvault create \
  --name "kv-${APP_NAME}" \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --enable-soft-delete true \
  --enable-purge-protection true

# Store secrets
az keyvault secret set \
  --vault-name "kv-${APP_NAME}" \
  --name "DatabasePassword" \
  --value "<postgres-password>"

az keyvault secret set \
  --vault-name "kv-${APP_NAME}" \
  --name "APIKey" \
  --value "<api-key-value>"
```

### Configure Managed Identity
```bash
# Enable system-assigned managed identity
az webapp identity assign \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP

# Grant Key Vault access
WEBAPP_IDENTITY=$(az webapp identity show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query principalId -o tsv)

az keyvault set-policy \
  --name "kv-${APP_NAME}" \
  --object-id $WEBAPP_IDENTITY \
  --secret-permissions get list
```

## Deployment Methods

### Method 1: GitHub Actions (Recommended)

Create `.github/workflows/deploy-azure.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      
      - uses: actions/setup-python@v6
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: python -m unittest discover tests/ -v
      
      - name: Deploy to Azure
        uses: azure/webapps-deploy@v2
        with:
          app-name: ${{ secrets.AZURE_WEBAPP_NAME }}
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

### Method 2: Azure CLI Direct Deploy
```bash
# Deploy from local directory
az webapp up \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --runtime "PYTHON:3.12"
```

### Method 3: Docker Container
```bash
# Build and push to Azure Container Registry
ACR_NAME="${APP_NAME}acr"
az acr create \
  --name $ACR_NAME \
  --resource-group $RESOURCE_GROUP \
  --sku Basic

# Build and push
az acr build \
  --registry $ACR_NAME \
  --image "${APP_NAME}:latest" \
  --file Dockerfile .

# Configure App Service to use container
az webapp config container set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name "${ACR_NAME}.azurecr.io/${APP_NAME}:latest"
```

## Environment Variables

Required environment variables for Azure deployment:

```bash
# Application
PORT=8000
PYTHON_VERSION=3.12
PYTHONUNBUFFERED=1

# Database (from Key Vault)
DATABASE_URL=<from-keyvault>
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Security
API_KEY=<from-keyvault>
ALLOW_OPEN_ACCESS=false

# Azure Services
APPINSIGHTS_INSTRUMENTATIONKEY=<from-app-insights>
APPLICATIONINSIGHTS_CONNECTION_STRING=<from-app-insights>

# Logging
LOG_LEVEL=INFO
WEBSITE_HTTPLOGGING_RETENTION_DAYS=7
```

## Monitoring & Logging

### Application Insights Queries

```kql
// Request performance
requests
| where timestamp > ago(1h)
| summarize count(), avg(duration), percentile(duration, 95) by name
| order by count_ desc

// Failed requests
requests
| where timestamp > ago(24h) and success == false
| project timestamp, name, resultCode, duration
| order by timestamp desc

// Dependency calls
dependencies
| where timestamp > ago(1h)
| summarize count(), avg(duration) by target, type
| order by count_ desc
```

### Health Check
```bash
# Configure health check endpoint
az webapp config set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --health-check-path "/"
```

## Scaling Configuration

### Auto-scaling Rules
```bash
# Create autoscale setting
az monitor autoscale create \
  --resource-group $RESOURCE_GROUP \
  --resource $APP_NAME \
  --resource-type "Microsoft.Web/serverfarms" \
  --name "autoscale-${APP_NAME}" \
  --min-count 1 \
  --max-count 5 \
  --count 2

# CPU-based scaling
az monitor autoscale rule create \
  --resource-group $RESOURCE_GROUP \
  --autoscale-name "autoscale-${APP_NAME}" \
  --condition "Percentage CPU > 70 avg 5m" \
  --scale out 1

az monitor autoscale rule create \
  --resource-group $RESOURCE_GROUP \
  --autoscale-name "autoscale-${APP_NAME}" \
  --condition "Percentage CPU < 30 avg 5m" \
  --scale in 1
```

## Security Best Practices

1. **Always use SSL/TLS** - Azure App Service provides free SSL certificates
2. **Enable managed identity** - No credentials in code
3. **Use Key Vault** - Store all secrets centrally
4. **Firewall rules** - Restrict database access
5. **Private endpoints** - For production databases
6. **CORS configuration** - Only allow trusted origins
7. **Rate limiting** - Implement at application level

## Cost Optimization

### Current Estimated Monthly Cost (Production)
- App Service (B2): ~$70/month
- PostgreSQL (Standard_D2s_v3): ~$150/month
- Application Insights: ~$2/month (5GB free)
- Key Vault: ~$0.50/month
- **Total: ~$222/month**

### Cost Reduction Options
- Use B1 tier for App Service (~$13/month) for lower traffic
- Use Burstable tier for PostgreSQL (~$30/month)
- Reserved instances for long-term commitments

## Backup & Disaster Recovery

### Database Backups
```bash
# PostgreSQL automatic backups (7-day retention by default)
az postgres flexible-server backup list \
  --server-name $POSTGRES_SERVER \
  --resource-group $RESOURCE_GROUP

# Manual backup
az postgres flexible-server backup create \
  --server-name $POSTGRES_SERVER \
  --resource-group $RESOURCE_GROUP \
  --backup-name "manual-$(date +%Y%m%d)"
```

### App Service Backups
```bash
# Create storage account for backups
az storage account create \
  --name "${APP_NAME}backup" \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS

# Configure backup
az webapp config backup create \
  --resource-group $RESOURCE_GROUP \
  --webapp-name $APP_NAME \
  --backup-name "daily-backup" \
  --container-url "<storage-sas-url>"
```

## Migration from Render.com

### Pre-Migration Checklist
- [ ] Azure resources created and configured
- [ ] Database schema migrated to Azure PostgreSQL
- [ ] Environment variables configured in Azure
- [ ] Secrets stored in Key Vault
- [ ] Application Insights configured
- [ ] DNS records prepared for cutover
- [ ] Rollback plan documented

### Migration Steps
1. Deploy application to Azure (parallel to Render.com)
2. Test Azure deployment thoroughly
3. Migrate data from Render.com to Azure PostgreSQL
4. Update DNS to point to Azure
5. Monitor for 24-48 hours
6. Decommission Render.com deployment

### Rollback Procedure
If issues occur:
1. Update DNS back to Render.com
2. Investigate Azure issues offline
3. Fix and retest in staging
4. Retry migration

## Testing

### Local Testing Against Azure Services
```bash
# Test database connection
export DATABASE_URL="postgresql://..."
python -c "import psycopg2; psycopg2.connect(os.getenv('DATABASE_URL'))"

# Test application
uvicorn src.api:app --reload --port 8000
```

### Staging Environment
Create a staging slot for testing:
```bash
az webapp deployment slot create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --slot staging \
  --configuration-source $APP_NAME
```

## Troubleshooting

### View Application Logs
```bash
# Stream logs
az webapp log tail \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP

# Download logs
az webapp log download \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --log-file logs.zip
```

### SSH into Container
```bash
az webapp ssh \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP
```

### Check Application Health
```bash
curl https://${APP_NAME}.azurewebsites.net/
```

## Next Steps

1. **Set up Azure subscription** - Ensure billing is configured
2. **Create staging environment** - Test deployment process
3. **Implement database migrations** - Per DATABASE_PREPARATION.md
4. **Configure CI/CD** - GitHub Actions deployment workflow
5. **Performance testing** - Load testing with Azure load testing service
6. **Documentation** - Update README with Azure deployment status

---

**Note:** This guide is a preparation document. Follow CLI-centric automation approach for all operations. Ensure all deployment steps are scriptable and repeatable.
