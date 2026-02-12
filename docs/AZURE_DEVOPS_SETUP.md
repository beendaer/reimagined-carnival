# Azure DevOps Setup Guide

**Repository:** beendaer/reimagined-carnival  
**Platform:** Azure DevOps (dev.azure.com)  
**Purpose:** CI/CD pipeline configuration for Testing as a Service platform

---

## Overview

This guide walks you through setting up Azure DevOps for the reimagined-carnival project, enabling CI/CD pipelines complementary to the existing GitHub Actions workflows.

## Prerequisites

- **Azure Subscription:** You need Owner or Contributor role on at least one Azure subscription
- **GitHub Account:** Repository access to beendaer/reimagined-carnival
- **Email:** Valid email for Azure DevOps notifications (e.g., justobeeme@outlook.com)

---

## Step 1: Create Azure DevOps Organization

### 1.1 Navigate to Azure DevOps
Visit: https://dev.azure.com

### 1.2 Setup Organization
1. Click **"Start free"** or **"Sign in"**
2. Sign in with your Microsoft account
3. **Name your organization:**
   - Enter organization name (e.g., `justobeeme`)
   - Organization URL will be: `dev.azure.com/justobeeme`
4. **Select region:** Choose closest to your location
   - Example: West US, East US, Central US

### 1.3 Link Azure Subscription
**IMPORTANT:** To create an Azure DevOps organization, you must link it to an Azure subscription.

If you see this error:
```
We couldn't find any subscriptions you have access to. 
Make sure you have the Owner or Contributor role on at least one Azure subscription.
```

**Solutions:**
1. **Create Azure Free Account:**
   - Visit: https://azure.microsoft.com/free/
   - Get $200 credit for 30 days
   - Free services for 12 months

2. **Request Access:**
   - Ask your Azure subscription administrator to grant you Owner or Contributor role
   - Go to Azure Portal → Subscriptions → Access Control (IAM) → Add role assignment

3. **Use Existing Subscription:**
   - If you already have access, select the subscription from the dropdown
   - Ensure you have Owner or Contributor role

### 1.4 Complete Organization Setup
1. Review and accept:
   - Terms of Service
   - Privacy Statement
   - Code of Conduct
2. Complete CAPTCHA verification
3. Click **"Continue"**

---

## Step 2: Create Project

### 2.1 Project Configuration
After organization creation, create your first project:

1. **Project name:** `justobeeme` (or `reimagined-carnival`)
2. **Description:** "Testing as a Service platform with deception detection"
3. **Visibility:**
   - **Private:** Only organization members can access (recommended for production)
   - **Public:** Anyone can view the project

### 2.2 Version Control Settings
- **Version control:** Git
- **Work item process:** Agile

### 2.3 Create Project
Click **"Create"** to initialize the project.

---

## Step 3: Connect GitHub Repository

### 3.1 Install Azure Pipelines GitHub App
1. Navigate to your project
2. Go to **Pipelines** → **Create Pipeline**
3. Select **"GitHub"**
4. Authenticate with GitHub
5. Select **"beendaer/reimagined-carnival"** repository
6. Authorize Azure Pipelines app

### 3.2 Configure Service Connection
1. In Azure DevOps, go to **Project Settings** → **Service connections**
2. Click **"New service connection"**
3. Select **"GitHub"**
4. Authenticate and authorize
5. Name the connection: `github-reimagined-carnival`

---

## Step 4: Setup Pipeline

### 4.1 Create Pipeline from Repository
1. Go to **Pipelines** → **New Pipeline**
2. Select **"GitHub"**
3. Choose **beendaer/reimagined-carnival**
4. Select **"Existing Azure Pipelines YAML file"**
5. Branch: `main` (or your working branch)
6. Path: `/azure-pipelines.yml`
7. Click **"Continue"**

### 4.2 Review Pipeline Configuration
The `azure-pipelines.yml` file defines:
- **Lint Stage:** Code quality checks (flake8, shellcheck)
- **Security Stage:** Trivy security scanning
- **Test Stage:** Unit tests on Python 3.11 & 3.12
- **Build Stage:** Docker image validation

### 4.3 Run Pipeline
1. Review the pipeline YAML
2. Click **"Run"**
3. Monitor the pipeline execution

---

## Step 5: Configure Pipeline Settings

### 5.1 Branch Policies
Set up branch protection for `main`:
1. Go to **Repos** → **Branches**
2. Click `...` on `main` branch → **Branch policies**
3. Enable:
   - **Require a minimum number of reviewers:** 1
   - **Check for linked work items:** Optional
   - **Build validation:** Add Azure Pipeline
   - **Status checks:** Require successful build

### 5.2 Pipeline Triggers
The pipeline is configured to trigger on:
- **Push to branches:** `main`, `tooling/*`, `feature/*`, `fix/*`
- **Pull requests to:** `main`

Edit `azure-pipelines.yml` to customize triggers.

### 5.3 Variables and Secrets
For sensitive configuration:
1. Go to **Pipelines** → **Library**
2. Create **Variable group:** `reimagined-carnival-secrets`
3. Add variables:
   - `API_KEY`: Your API key
   - `DOCKER_REGISTRY`: Registry URL (if using)
4. Link variable group in pipeline YAML:
   ```yaml
   variables:
     - group: reimagined-carnival-secrets
   ```

---

## Step 6: Enable Notifications

### 6.1 Configure Email Notifications
1. Go to **Project Settings** → **Notifications**
2. Create notification subscription:
   - **Event:** Build completed
   - **Recipient:** Your email
   - **Filter:** All builds or failed builds only

### 6.2 Slack/Teams Integration (Optional)
1. Install Azure Pipelines app in Slack/Teams
2. Configure webhook in **Service connections**
3. Add notification step to pipeline

---

## Step 7: Add Build Status Badge

### 7.1 Get Badge Markdown
1. Navigate to your pipeline in Azure DevOps
2. Click on the pipeline name
3. Click **"..."** (three dots menu) → **"Status badge"**
4. Copy the badge URL or Markdown snippet
5. Note your **pipeline definition ID** from the URL

### 7.2 Add Badge to README
Add the badge to your GitHub repository's README.md:

```markdown
[![Azure DevOps Build Status](https://dev.azure.com/justobeeme/justobeeme/_apis/build/status/reimagined-carnival?branchName=main)](https://dev.azure.com/justobeeme/justobeeme/_build/latest?definitionId=1&branchName=main)
```

**Replace:**
- `justobeeme` (first occurrence): Your Azure DevOps organization name
- `justobeeme` (second occurrence): Your project name
- `definitionId=1`: Your actual pipeline definition ID
- `branchName=main`: Your target branch

### 7.3 Example Badge URL Structure
```
https://dev.azure.com/{organization}/{project}/_apis/build/status/{pipeline-name}?branchName={branch}
```

---

## Pipeline Structure

### Current Pipeline Stages

```yaml
Lint → Security → Test → Build
  ↓       ↓         ↓      ↓
flake8  Trivy    Python  Docker
        scan    3.11/3.12 build
```

### Key Features
- ✅ **Multi-stage pipeline** with clear separation of concerns
- ✅ **Matrix testing** on Python 3.11 and 3.12
- ✅ **Security scanning** with Trivy
- ✅ **Docker build validation**
- ✅ **Parallel job execution** for faster feedback

---

## Troubleshooting

### Issue: "No Azure subscription found"
**Solution:** Create Azure free account or request access to existing subscription.

### Issue: "Pipeline failed to trigger"
**Solution:** 
1. Check branch name matches trigger configuration
2. Verify GitHub service connection is active
3. Review pipeline trigger settings

### Issue: "Tests failing in pipeline but pass locally"
**Solution:**
1. Check Python version matches (3.11 or 3.12)
2. Verify all dependencies in `requirements.txt`
3. Review environment variables needed

### Issue: "Docker build fails"
**Solution:**
1. Ensure Dockerfile is at repository root
2. Check for syntax errors in Dockerfile
3. Verify base image availability

---

## Next Steps

After successful setup:

1. **Configure deployment pipeline:**
   - See `docs/AZURE_DEPLOYMENT.md` for Azure App Service deployment
   - Set up production and staging environments

2. **Enable Advanced Features:**
   - Code coverage reporting
   - Test result publishing
   - Artifact publishing

3. **Integrate with Azure Services:**
   - Application Insights for monitoring
   - Azure Key Vault for secrets
   - Azure Container Registry for images

---

## Comparison: Azure Pipelines vs GitHub Actions

| Feature | Azure Pipelines | GitHub Actions |
|---------|----------------|----------------|
| **Configuration** | `azure-pipelines.yml` | `.github/workflows/ci.yml` |
| **Build Minutes** | 1,800 free/month (parallel jobs) | 2,000 free/month |
| **Matrix Testing** | ✅ Python 3.11, 3.12 | ✅ Python 3.11, 3.12 |
| **Artifacts** | Azure Artifacts | GitHub Packages |
| **Deployment** | Azure DevOps Releases | GitHub Environments |
| **Integration** | Azure services | GitHub ecosystem |

Both platforms run identical tests and validations for this project.

---

## Resources

- **Azure DevOps Documentation:** https://docs.microsoft.com/azure/devops/
- **Azure Pipelines YAML Schema:** https://docs.microsoft.com/azure/devops/pipelines/yaml-schema/
- **GitHub Integration:** https://docs.microsoft.com/azure/devops/pipelines/repos/github
- **Azure Free Account:** https://azure.microsoft.com/free/

---

## Support

For issues with Azure DevOps setup:
1. Check Azure DevOps Status: https://status.dev.azure.com/
2. Review pipeline logs for specific errors
3. Consult Azure DevOps community: https://developercommunity.visualstudio.com/

For project-specific issues:
- See `README.md` for local development
- See `docs/OPERATIONS.md` for operational guidance
