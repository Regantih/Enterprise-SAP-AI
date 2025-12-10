# Activation Checklist: 400+ Pre-built Use Cases

To "turn on" the 400+ use cases, you don't build them from scratch. You activate them in your specific SAP systems.

## 1. Finance (S/4HANA)
- [ ] **Activate Scope Items**: In S/4HANA Cloud, activate scope items for "Intelligent Finance" (e.g., 4AI, 4AF).
- [ ] **Cash App**: Enable "SAP Cash Application" integration for automated bank reconciliation.
- [ ] **Joule Integration**: Ensure the `Joule` communication scenario is active in S/4HANA Communication Arrangements.

## 2. Human Resources (SuccessFactors)
- [ ] **Upgrade Center**: Go to Admin Center > Upgrade Center.
- [ ] **Enable Joule**: Search for "Joule" and click "Upgrade Now".
- [ ] **Permissions**: Grant "Access Joule" permission to "All Employees" role.
- [ ] **Sync**: Run the "Joule HR Data Sync" job to index employee data.

## 3. Supply Chain (IBP / S/4HANA)
- [ ] **Copilot Configuration**: In IBP Fiori Launchpad, enable "Digital Assistant".
- [ ] **Data Sharing**: Allow data sharing between IBP and Joule service in BTP.

## 4. Procurement (Ariba / S/4HANA)
- [ ] **Guided Buying**: Enable "GenAI Features" in Ariba Administration.
- [ ] **Category Management**: Activate "Intelligent Category Management" services.

## 5. Verification
- [ ] Log into **Fiori Launchpad**.
- [ ] Click the **Joule Icon** (Diamond shape).
- [ ] Ask: *"What can you do?"* -> It should list capabilities from Finance, HR, etc. based on your active integrations.
