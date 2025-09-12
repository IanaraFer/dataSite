# 🚀 Complete Azure Setup Guide

## Step 1: Create Azure Static Web App

### Option A: Using Azure Portal (Recommended)
1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Static Web App"
4. Click "Create"
5. Fill in the details:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: `rg-analyticacore-prod` (or create new)
   - **Name**: `analyticacore-ai` (must be globally unique)
   - **Plan type**: Free
   - **Region**: East US 2
   - **Source**: GitHub
   - **GitHub account**: Your GitHub account
   - **Organization**: Your GitHub username
   - **Repository**: `dataSite`
   - **Branch**: `main`
   - **Build presets**: Custom
   - **App location**: `/`
   - **API location**: (leave empty)
   - **Output location**: `/website`

### Option B: Using Azure CLI
```bash
# Install Azure CLI first
az login
az group create --name rg-analyticacore-prod --location eastus2
az staticwebapp create \
  --name analyticacore-ai \
  --resource-group rg-analyticacore-prod \
  --source https://github.com/IanaraFer/dataSite \
  --location eastus2 \
  --branch main \
  --app-location "/" \
  --output-location "/website"
```

## Step 2: Get the Deployment Token

### From Azure Portal:
1. Go to your Static Web App in Azure Portal
2. Click on "Manage deployment token" in the left menu
3. Copy the deployment token

### From Azure CLI:
```bash
az staticwebapp secrets list --name analyticacore-ai --resource-group rg-analyticacore-prod
```

## Step 3: Configure GitHub Secrets

1. Go to your GitHub repository: `https://github.com/IanaraFer/dataSite`
2. Click "Settings" tab
3. Click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Add these secrets:

### Required Secrets:
- **Name**: `AZURE_STATIC_WEB_APPS_API_TOKEN`
- **Value**: [Your deployment token from Step 2]

### Optional Secrets (for infrastructure deployment):
- **Name**: `AZURE_CREDENTIALS`
- **Value**: [Service principal credentials in JSON format]
- **Name**: `AZURE_SUBSCRIPTION_ID`
- **Value**: [Your Azure subscription ID]

## Step 4: Enable the Azure Workflow

Once you have the token configured, I'll enable the workflow.

## Step 5: Test Deployment

After configuration, the workflow will automatically deploy on every push to main branch.

## 🔧 Troubleshooting

### Common Issues:
1. **Token not found**: Make sure the secret name is exactly `AZURE_STATIC_WEB_APPS_API_TOKEN`
2. **Resource group not found**: Create the resource group first
3. **Name not unique**: Choose a different name for your Static Web App
4. **Branch not found**: Make sure you're pushing to the `main` branch

### Verification:
- Check GitHub Actions tab for deployment status
- Visit your Static Web App URL in Azure Portal
- Test the website functionality
