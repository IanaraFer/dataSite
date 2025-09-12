# 🚀 Azure Quick Setup - 5 Minutes

## Step 1: Create Azure Static Web App (2 minutes)

1. **Go to Azure Portal**: https://portal.azure.com
2. **Click "Create a resource"** (big + button)
3. **Search for "Static Web App"** and select it
4. **Click "Create"**

## Step 2: Fill in the Details

**Basic Tab:**
- **Subscription**: Select your subscription
- **Resource Group**: Create new → `rg-analyticacore-prod`
- **Name**: `analyticacore-ai` (or any unique name)
- **Plan type**: **Free**
- **Region**: **East US 2**

**Deployment Tab:**
- **Source**: **GitHub**
- **GitHub account**: Your GitHub account
- **Organization**: Your GitHub username
- **Repository**: `dataSite`
- **Branch**: `main`

**Build Tab:**
- **Build presets**: **Custom**
- **App location**: `/`
- **API location**: (leave empty)
- **Output location**: `/website`

## Step 3: Create and Get Token (1 minute)

1. **Click "Review + Create"**
2. **Click "Create"**
3. **Wait for deployment** (1-2 minutes)
4. **Go to your Static Web App**
5. **Click "Manage deployment token"** in the left menu
6. **Copy the deployment token**

## Step 4: Add Token to GitHub (1 minute)

1. **Go to GitHub**: https://github.com/IanaraFer/dataSite/settings/secrets/actions
2. **Click "New repository secret"**
3. **Name**: `AZURE_STATIC_WEB_APPS_API_TOKEN`
4. **Value**: Paste your token from Step 3
5. **Click "Add secret"**

## Step 5: Test Deployment (1 minute)

1. **Go to Actions tab**: https://github.com/IanaraFer/dataSite/actions
2. **You should see "Azure Deployment" workflow running**
3. **Wait for it to complete** (2-3 minutes)
4. **Visit your site**: `https://[your-app-name].azurestaticapps.net`

## ✅ That's it! Your site will be live on Azure.

### 🔧 If Something Goes Wrong:

**Token not working?**
- Make sure the secret name is exactly: `AZURE_STATIC_WEB_APPS_API_TOKEN`
- Check that the token was copied completely

**Workflow not running?**
- Push a small change to trigger it
- Check the Actions tab for any errors

**Site not loading?**
- Wait 2-3 minutes after deployment
- Check the Azure Portal for any errors
- Try refreshing the page

### 📞 Need Help?
- Check the Azure Portal for error messages
- Look at the GitHub Actions logs
- The workflow is already configured and ready to go!
