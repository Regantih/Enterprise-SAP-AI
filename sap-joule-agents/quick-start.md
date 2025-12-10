# SAP Joule AI Agent - Quick Start Guide

## 🚀 Get Started in 30 Minutes

This guide helps you create your first SAP Joule AI agent quickly.

---

## Prerequisites Checklist

- [ ] SAP BTP account (trial or production)
- [ ] Joule Studio access
- [ ] Basic understanding of your use case
- [ ] Web browser (Chrome/Edge recommended)

---

## Step 1: Access Joule Studio (5 minutes)

1. **Login to SAP BTP Cockpit**
   - Navigate to https://account.hanatrial.ondemand.com (trial) or your production URL
   - Enter your credentials

2. **Open SAP Build**
   - Click on "SAP Build" from the main menu
   - Select "Joule Studio" from the lobby

3. **Verify Access**
   - You should see the Agent Builder interface
   - If not, check your entitlements and user roles

---

## Step 2: Create Your First Agent (10 minutes)

### Agent Template: Simple Data Retrieval Agent

**Use Case**: Help users retrieve supplier information

1. **Click "Create New Agent"**

2. **Define Agent Purpose**
   ```
   Agent Name: Supplier Information Assistant
   
   Description: This agent helps users quickly find supplier 
   information including contact details, performance metrics, 
   and contract status.
   
   Role: You are a helpful assistant with access to supplier 
   data. Provide clear, concise information when users ask 
   about suppliers.
   ```

3. **Connect Data Source**
   - Click "Add Data Source"
   - Select "SAP S/4HANA" (or your available system)
   - Choose "Supplier Master Data" entity
   - Test connection

4. **Select LLM Model**
   - Choose from available models (GPT-4, Claude, Gemini)
   - Start with default settings
   - You can optimize later

5. **Save Agent**
   - Click "Save"
   - Your agent is now created!

---

## Step 3: Create a Simple Skill (10 minutes)

### Skill: Get Supplier Details

1. **Navigate to Skills Section**
   - Click "Skills" in the left menu
   - Click "Create New Skill"

2. **Configure Skill**
   ```json
   {
     "name": "GetSupplierDetails",
     "description": "Retrieves detailed supplier information",
     "type": "API",
     "inputs": [
       {
         "name": "supplierId",
         "type": "string",
         "required": true,
         "description": "Unique supplier identifier"
       }
     ],
     "outputs": [
       {
         "name": "supplierName",
         "type": "string"
       },
       {
         "name": "contactEmail",
         "type": "string"
       },
       {
         "name": "status",
         "type": "string"
       }
     ]
   }
   ```

3. **Connect to API**
   - Endpoint: `/API_BUSINESS_PARTNER/A_Supplier('{supplierId}')`
   - Method: GET
   - Authentication: Use configured connection

4. **Test Skill**
   - Enter test supplier ID
   - Click "Test"
   - Verify output

5. **Attach to Agent**
   - Go back to your agent
   - Click "Add Skills"
   - Select "GetSupplierDetails"
   - Save

---

## Step 4: Test Your Agent (5 minutes)

### Test Prompts

1. **Basic Query**
   ```
   User: "Show me information for supplier SUP-001"
   Expected: Agent uses GetSupplierDetails skill and returns data
   ```

2. **Natural Language**
   ```
   User: "What's the contact email for supplier ABC Corp?"
   Expected: Agent finds supplier and returns email
   ```

3. **Error Handling**
   ```
   User: "Show me supplier XYZ-999"
   Expected: Agent handles "not found" gracefully
   ```

### Testing Panel

- Use the built-in test panel in Joule Studio
- Review execution trace for each test
- Check response time and accuracy
- Iterate on prompts and configuration

---

## Step 5: Deploy (Optional)

### For Production Deployment

1. **Review Agent**
   - Verify all tests pass
   - Check security settings
   - Review data access permissions

2. **Deploy**
   - Click "Deploy to Production"
   - Select target environment
   - Confirm deployment

3. **Share with Users**
   - Generate access link
   - Send to pilot users
   - Provide basic instructions

---

## 🎉 Congratulations!

You've created your first SAP Joule AI agent! 

### Next Steps

- [ ] Add more skills to your agent
- [ ] Connect additional data sources
- [ ] Create more complex agents
- [ ] Explore multi-agent collaboration
- [ ] Review the full roadmap for advanced features

---

## Common Issues & Solutions

### Issue: Can't access Joule Studio
**Solution**: Check BTP entitlements and user role assignments

### Issue: Data connection fails
**Solution**: Verify API credentials and network connectivity

### Issue: Agent doesn't understand prompts
**Solution**: Refine agent instructions and add more context

### Issue: Slow response times
**Solution**: Optimize skills, check API performance, consider caching

---

## Resources

- 📖 [Full Roadmap](./roadmap.md)
- 🎓 [SAP Learning Hub](https://learning.sap.com)
- 💬 [SAP Community](https://community.sap.com)
- 🆘 [Support Portal](https://support.sap.com)

---

**Need Help?** Refer to the comprehensive roadmap or reach out to SAP support!
