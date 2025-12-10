# SAP Joule & Business AI Setup Guide

To access the **400+ AI use cases** and build your own agents, you need to configure two distinct environments: **Consumption** (for pre-built agents) and **Development** (for custom agents).

## 1. Prerequisites for Pre-built Agents (The "400 Use Cases")

To "turn on" the existing agents for Finance, HR, Supply Chain, etc., you need:

### A. System Requirements
- [ ] **SAP S/4HANA Cloud** (Public Edition 2402+ or Private Edition)
- [ ] **SAP Business Technology Platform (BTP)** Global Account
- [ ] **SAP Cloud Identity Services** (IAS) for authentication

### B. Licensing & Entitlements
- [ ] **SAP AI Units**: Most Joule use cases consume "AI Units". Ensure your BTP contract includes a sufficient quota.
- [ ] **Joule License**: Verify your specific SAP solution license includes Joule access (often bundled with "Rise with SAP" or "Grow with SAP").

### C. Configuration Steps
1. **Enable Joule in BTP Cockpit**:
   - Go to *Service Marketplace* -> Search for "Joule".
   - Create a subscription.
2. **Connect to Business Systems**:
   - In BTP Cockpit, configure **Destinations** to your S/4HANA, SuccessFactors, or Ariba instances.
   - Install the **Cloud Connector** if using Private Cloud/On-Premise systems.
3. **Role Assignment**:
   - Assign the `Joule User` and `Joule Administrator` role collections to users in SAP Cloud Identity Services.

---

## 2. Prerequisites for Building Custom Agents (Joule Studio)

To build *new* agents or extend existing ones (what we covered in the Roadmap), you need:

### A. Development Environment
- [ ] **SAP Build Code** entitlement in BTP.
- [ ] **Joule Studio** access (via SAP Build Lobby).
- [ ] **SAP Business Application Studio** (optional, for advanced coding).

### B. Data & Knowledge Setup
- [ ] **SAP Business Data Cloud**: Setup connection to index your business data for the agents to "read".
- [ ] **SAP Knowledge Graph**: Enable this service to give agents semantic understanding of your data relationships.

---

## 3. "Hello World" Checklist

To verify everything is working:

1. **Test Pre-built**: Log into your S/4HANA Fiori Launchpad. Click the diamond "Joule" icon in the header. Ask: *"Show me my open purchase requisitions."*
2. **Test Custom**: Log into SAP Build Lobby. Open Joule Studio. Create a simple "Echo" agent. Test it in the preview panel.

## 🔍 Troubleshooting Common Setup Issues

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| **Joule icon missing** | Missing User Roles | Check SAP Cloud Identity Services group assignments. |
| **"I cannot help with that"** | Missing Data Context | Verify BTP Destinations and Cloud Connector status. |
| **AI Units Error** | Quota Exceeded | Check BTP Entitlements and purchase more AI Units if needed. |
