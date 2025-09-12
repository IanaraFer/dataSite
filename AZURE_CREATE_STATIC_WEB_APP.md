# 🚀 Create Azure Static Web App - Step by Step

## Current Issue
The Azure deployment is failing because no Static Web App exists yet. You need to create one first.

## Step 1: Create Resource Group (if needed)

1. **In Azure Portal**, click "Create a resource"
2. **Search for "Resource Group"**
3. **Click "Create"**
4. **Fill in:**
   - **Resource Group name**: `rg-analyticacore-prod`
   - **Region**: `East US 2`
5. **Click "Review + Create"** → **"Create"**

## Step 2: Create Static Web App

1. **Click "Create a resource"** (big + button)
2. **Search for "Static Web App"**
3. **Click "Create"**

## Step 3: Fill in Basic Details

**Subscription**: Select your subscription
**Resource Group**: `rg-analyticacore-prod` (or create new)
**Name**: `analyticacore-ai` (must be globally unique - try adding numbers if taken)
**Plan type**: **Free**
**Region**: **East US 2**

## Step 4: Configure Deployment

**Deployment tab:**
- **Source**: **GitHub**
- **GitHub account**: Your GitHub account
- **Organization**: Your GitHub username
- **Repository**: `dataSite`
- **Branch**: `main`

**Build tab:**
- **Build presets**: **Custom**
- **App location**: `/`
- **API location**: (leave empty)
- **Output location**: `/website`

## Step 5: Create and Get Token

1. **Click "Review + Create"**
2. **Click "Create"**
3. **Wait for deployment** (2-3 minutes)
4. **Go to your Static Web App**
5. **Click "Manage deployment token"** in the left menu
6. **Copy the deployment token**

## Step 6: Add Token to GitHub

1. **Go to**: https://github.com/IanaraFer/dataSite/settings/secrets/actions
2. **Click "New repository secret"**
3. **Name**: `AZURE_STATIC_WEB_APPS_API_TOKEN`
4. **Value**: [Your token from Step 5]
5. **Click "Add secret"**

## Step 7: Test Deployment

1. **Go to Actions**: https://github.com/IanaraFer/dataSite/actions
2. **The workflow should run automatically**
3. **Wait for it to complete**
4. **Visit your site**: `https://[your-app-name].azurestaticapps.net`

## ✅ That's it! Your site will be live on Azure.

### 🔧 If You Get Errors:

**"Name not available"**: Try adding numbers: `analyticacore-ai-123`

**"Resource group not found"**: Create it first (Step 1)

**"Token not working"**: Make sure the secret name is exactly: `AZURE_STATIC_WEB_APPS_API_TOKEN`

**"Workflow not running"**: Push a small change to trigger it

### 📞 Need Help?
- Check the Azure Portal for error messages
- Look at the GitHub Actions logs
- The workflow is now configured to skip deployment if token is missing
