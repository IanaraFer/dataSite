@description('Irish business deployment for AnalyticaCore AI')
param environment string = 'prod'
param location string = 'West Europe' // EU region for GDPR compliance
param companyRegistrationNumber string // Irish CRO number
param vatNumber string // Irish VAT number

// Variables for Irish business
var resourcePrefix = 'analyticacore-ie-${environment}'
var domainName = 'analyticacore.ie'

// Resource Group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: 'rg-${resourcePrefix}'
  location: location
  tags: {
    environment: environment
    country: 'Ireland'
    companyType: 'Irish SME'
    gdprCompliant: 'true'
    croNumber: companyRegistrationNumber
    vatNumber: vatNumber
  }
}

// Key Vault for secure configuration (Required for Irish business)
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-${resourcePrefix}'
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: true
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    purgeProtectionEnabled: false
  }
  tags: {
    purpose: 'Secure configuration storage'
    gdprCompliant: 'true'
  }
}

// Application Insights for monitoring (Required for business operations)
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'ai-${resourcePrefix}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    DisableIpMasking: false // GDPR compliance
    DisableLocalAuth: false
  }
  tags: {
    purpose: 'Application monitoring'
    gdprCompliant: 'true'
  }
}

// Container Registry for Docker images
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: '${replace(resourcePrefix, '-', '')}registry'
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
  tags: {
    purpose: 'Container image storage'
  }
}

// Static Web App for frontend
resource staticWebApp 'Microsoft.Web/staticSites@2023-01-01' = {
  name: 'swa-${resourcePrefix}'
  location: location
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
  properties: {
    buildProperties: {
      appLocation: '/website'
      apiLocation: ''
      outputLocation: ''
    }
    stagingEnvironmentPolicy: 'Enabled'
  }
  tags: {
    purpose: 'Frontend hosting'
    gdprCompliant: 'true'
  }
}

// Container Apps Environment
resource containerEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: 'cae-${resourcePrefix}'
  location: location
  properties: {
    zoneRedundant: true
  }
  tags: {
    purpose: 'Container hosting environment'
  }
}

// Container App for Streamlit backend
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: 'ca-${resourcePrefix}'
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
            'https://${domainName}'
            'https://www.${domainName}'
          ]
        }
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          username: containerRegistry.name
          passwordSecretRef: 'registry-password'
        }
      ]
      secrets: [
        {
          name: 'registry-password'
          value: containerRegistry.listCredentials().passwords[0].value
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'analyticacore-api'
          image: '${containerRegistry.properties.loginServer}/analyticacore-ai:latest'
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
              name: 'GDPR_COMPLIANCE'
              value: 'true'
            }
            {
              name: 'DATA_RESIDENCY'
              value: 'EU'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
      }
    }
  }
  tags: {
    purpose: 'AI analysis backend'
    gdprCompliant: 'true'
  }
}

// DNS Zone for custom domain
resource dnsZone 'Microsoft.Network/dnsZones@2023-07-01' = {
  name: domainName
  location: 'global'
  properties: {}
  tags: {
    purpose: 'Domain management'
  }
}

// Custom domain configuration
resource customDomain 'Microsoft.Web/staticSites/customDomains@2023-01-01' = {
  parent: staticWebApp
  name: domainName
  properties: {
    validationMethod: 'cname-delegation'
  }
}