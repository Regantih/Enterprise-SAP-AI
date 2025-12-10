# SAP BTP Setup Automation Script
# This script automates the setup of SAP Joule and related services on SAP BTP
# Prerequisites: SAP BTP CLI (btp) must be installed and authenticated

param(
    [Parameter(Mandatory=$true)]
    [string]$GlobalAccount,
    
    [Parameter(Mandatory=$true)]
    [string]$Subaccount,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us10"
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message)
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor Cyan
}

function Check-BtpCli {
    try {
        btp --version | Out-Null
        Write-Log "✅ SAP BTP CLI is installed"
    }
    catch {
        Write-Error "❌ SAP BTP CLI is not installed. Please install it first: https://tools.hana.ondemand.com/#cloud"
    }
}

function Enable-Service {
    param([string]$ServiceName, [string]$Plan)
    
    Write-Log "Enabling service: $ServiceName ($Plan)..."
    try {
        # Check entitlement
        btp list accounts/entitlement --subaccount $Subaccount | Select-String $ServiceName | Out-Null
        
        # Create subscription/instance
        btp create services/instance --subaccount $Subaccount --service $ServiceName --plan $Plan --name "$ServiceName-core"
        Write-Log "✅ Service $ServiceName enabled successfully"
    }
    catch {
        Write-Warning "⚠️ Could not enable $ServiceName. Check entitlements or if it's already enabled."
    }
}

# --- Main Execution ---

Write-Log "🚀 Starting SAP Joule Environment Setup..."

# 1. Verify CLI
Check-BtpCli

# 2. Target Subaccount
Write-Log "Targeting Global Account: $GlobalAccount / Subaccount: $Subaccount"
# Note: User must be logged in via 'btp login' beforehand

# 3. Enable Core Joule Services (The "Brain")
# These services are required for the 400+ use cases
Enable-Service -ServiceName "joule" -Plan "standard"
Enable-Service -ServiceName "das-application" -Plan "standard" # Data Attribute Recommendation

# 4. Enable Development Services (Custom Agents)
# These are for building your OWN agents
Enable-Service -ServiceName "sap-build-code" -Plan "standard"
Enable-Service -ServiceName "sap-business-application-studio" -Plan "standard"
Enable-Service -ServiceName "business-data-cloud" -Plan "standard"

# 5. Setup Trust & Security (Placeholder)
Write-Log "ℹ️  Reminder: Configure Trust Configuration in BTP Cockpit for SAP Cloud Identity Services"

Write-Log "🎉 Setup script completed. Please verify services in BTP Cockpit."
