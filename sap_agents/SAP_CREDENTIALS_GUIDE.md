# How to Get SAP AI Core Credentials

To connect your agent to SAP AI Core, you need a **Service Key**. Follow these steps in the SAP BTP Cockpit.

## Prerequisites
*   You must have an SAP BTP Global Account and Subaccount.
*   **SAP AI Core** service must be subscribed/entitled in your subaccount.
*   **SAP AI Launchpad** is recommended for managing deployments.

### 🛑 Can't find "Create Account"?
If you are stuck on a login screen without a "Register" button:
1.  **Create SAP Universal ID directly**: [https://account.sap.com/core/create/landing](https://account.sap.com/core/create/landing)
2.  Once created, go back to the **BTP Sign Up**: [https://account.hanatrial.ondemand.com/](https://account.hanatrial.ondemand.com/)
3.  Select **"Pay-As-You-Go"** (required for AI Core Free Tier).

## Step-by-Step Guide

### 1. Log in to SAP BTP Cockpit
Go to your SAP BTP Cockpit URL (usually `https://cockpit.btp.cloud.sap/`).

### 2. Navigate to Your Subaccount
Select the **Global Account** and then the **Subaccount** where SAP AI Core is enabled.

### 3. Go to Instances and Subscriptions
In the left navigation menu, click on **Services** > **Instances and Subscriptions**.

### 4. Find SAP AI Core Instance
*   Look for **SAP AI Core** in the list of instances.
*   If you don't see it, click **Create** in the top right, select **SAP AI Core**, choose the **standard** plan, and give it a name (e.g., `ai-core-instance`).

### 5. Create a Service Key
1.  Click on the **SAP AI Core** instance name (or the three dots `...` > **Create Service Key**).
2.  In the Service Keys tab/section, click **Create**.
3.  Give it a name (e.g., `agent-key`).
4.  Click **Create**.

### 6. Get the Credentials
1.  Once created, click on the Service Key name or "View".
2.  You will see a JSON object. Copy the following values to your `.env` file:

```json
{
  "serviceurls": {
    "AI_API_URL": "https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com" 
  },
  "clientid": "sb-...",
  "clientsecret": "...",
  "url": "https://<subdomain>.authentication.eu10.hana.ondemand.com"
}
```

## Mapping to `.env`

Update your `sap_agents/.env` file with these values:

| `.env` Variable | Service Key JSON Field |
| :--- | :--- |
| `AICORE_AUTH_URL` | `url` (from the root level, NOT serviceurls) |
| `AICORE_CLIENT_ID` | `clientid` |
| `AICORE_CLIENT_SECRET` | `clientsecret` |
| `AICORE_BASE_URL` | `serviceurls.AI_API_URL` |
| `AICORE_RESOURCE_GROUP` | `default` (or your specific resource group ID) |

> **Note**: The `AICORE_RESOURCE_GROUP` is usually `default` unless you have created specific resource groups in SAP AI Launchpad.
