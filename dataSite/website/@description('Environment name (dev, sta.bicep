@description('Environment name (dev, staging, prod)')
param environment string = 'prod'

@description('Location for all resources')
param location string = 'East US 2'

@description('Custom domain name')
param customDomain string = 'analyticacoreai.com'

@description('GitHub repository URL')
param repositoryUrl string = 'https://github.com/yourusername/analyticacoreai-platform'

// Variables following Azure naming conventions
var resourcePrefix = 'analyticacore-${environment}'
var staticWebAppName = '${resourcePrefix}-webapp'
var containerAppName = '${resourcePrefix}-api'
var containerEnvironmentName = '${resourcePrefix}-env'
var logAnalyticsName = '${resourcePrefix}-logs'
var appInsightsName = '${resourcePrefix}-insights'

// Resource group (create separately)
// az group create --name rg-analyticacore-prod --location "East US 2"

// Log Analytics Workspace for monitoring
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
  tags: {
    environment: environment
    project: 'AnalyticaCore AI'
    purpose: 'SME Data Analysis Platform'
  }
}

// Application Insights for telemetry
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
  tags: {
    environment: environment
    project: 'AnalyticaCore AI'
  }
}

// Container Apps Environment
resource containerEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: containerEnvironmentName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
  tags: {
    environment: environment
    project: 'AnalyticaCore AI'
  }
}

// Container App for Streamlit backend
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: containerAppName
  location: location
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8501
        transport: 'http'
        corsPolicy: {
          allowedOrigins: [
            'https://${staticWebAppName}.azurestaticapps.net'
            'https://${customDomain}'
            'https://www.${customDomain}'
          ]
          allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
          allowedHeaders: ['*']
          allowCredentials: true
        }
      }
      secrets: [
        {
          name: 'container-registry-password'
          value: 'placeholder' // Will be updated during deployment
        }
      ]
      registries: [
        {
          server: '${resourcePrefix}registry.azurecr.io'
          username: '${resourcePrefix}registry'
          passwordSecretRef: 'container-registry-password'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'analyticacore-api'
          image: '${resourcePrefix}registry.azurecr.io/analyticacore-api:latest'
          resources: {
            cpu: json('1.0')
            memory: '2.0Gi'
          }
          env: [
            {
              name: 'ENVIRONMENT'
              value: environment
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: appInsights.properties.ConnectionString
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
        rules: [
          {
            name: 'http-scale'
            http: {
              metadata: {
                concurrentRequests: '10'
              }
            }
          }
        ]
      }
    }
  }
  tags: {
    environment: environment
    project: 'AnalyticaCore AI'
  }
}

// Static Web App for frontend
resource staticWebApp 'Microsoft.Web/staticSites@2023-01-01' = {
  name: staticWebAppName
  location: location
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
  properties: {
    repositoryUrl: repositoryUrl
    branch: 'main'
    buildProperties: {
      appLocation: '/website'
      apiLocation: ''
      outputLocation: ''
    }
    stagingEnvironmentPolicy: 'Enabled'
  }
  tags: {
    environment: environment
    project: 'AnalyticaCore AI'
    purpose: 'Frontend Hosting'
  }
}

// Custom domain for Static Web App
resource customDomainResource 'Microsoft.Web/staticSites/customDomains@2023-01-01' = {
  parent: staticWebApp
  name: customDomain
  properties: {
    validationMethod: 'cname-delegation'
  }
}

// Outputs for configuration
output staticWebAppUrl string = 'https://${staticWebApp.properties.defaultHostname}'
output staticWebAppName string = staticWebApp.name
output customDomainUrl string = 'https://${customDomain}'
output containerAppUrl string = 'https://${containerApp.properties.configuration.ingress.fqdn}'
output resourceGroupName string = resourceGroup().name
output deploymentToken string = staticWebApp.listSecrets().properties.apiKey