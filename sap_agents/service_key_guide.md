# How to Get Your SAP Service Key 🔑

Since I cannot access your subaccount directly due to security redirects, please follow these steps manually:

## Step 1: Enter Your Trial Account
1.  Go to the **SAP BTP Cockpit**: [https://cockpit.hanatrial.ondemand.com/trial/#/home/trial](https://cockpit.hanatrial.ondemand.com/trial/#/home/trial)
2.  Click the blue button **"Go To Your Trial Account"**.
    *   *If that doesn't work, look for a tile named "Trial Account" and click it.*

## Step 2: Navigate to Instances
1.  Once inside your subaccount (you should see a left sidebar), click on **"Instances and Subscriptions"**.
2.  Look at the list of instances. Do you see **"SAP AI Core"**?

## Step 3: If "SAP AI Core" Exists...
1.  Click on the row for **SAP AI Core**.
2.  On the right panel that opens, look for **"Service Keys"**.
3.  Click the **( ... )** or **Create** button to make a new key.
4.  Give it a name (e.g., `joule-key`) and click **Create**.
5.  **Copy the entire JSON content** of the key.

## Step 4: If "SAP AI Core" is MISSING...
1.  Click **"Create"** (top right of the list).
2.  Search for **"SAP AI Core"**.
3.  Select the **"free"** or **"standard"** plan.
4.  Click **Create**.
5.  *Wait a moment for it to be created, then follow Step 3.*

---

**Paste the JSON key here when you have it!** 👇
