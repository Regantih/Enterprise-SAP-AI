import sys
import json
import time
import random

class JouleAgent:
    def __init__(self):
        print("💎 SAP Joule Copilot (Custom Agent) Initialized")
        print("--------------------------------------------")
        print("⚠️  Mode: Development (Mock Data)")
        print("--------------------------------------------")
        self.context = {}

    def run(self):
        print("\nJoule: Hello! I'm your SAP Joule Copilot. How can I help you with your business today?")
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("Joule: Goodbye! Have a productive day.")
                    break
                
                self.process_request(user_input)
            except KeyboardInterrupt:
                print("\nJoule: Goodbye!")
                break

    def process_request(self, query):
        # Simulate "Thinking" animation
        print("Joule: ", end="", flush=True)
        for _ in range(3):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print(" ", end="", flush=True)
        
        query_lower = query.lower()

        if "sales" in query_lower or "order" in query_lower:
            self.handle_sales_skill(query)
        elif "product" in query_lower or "inventory" in query_lower or "stock" in query_lower:
            self.handle_inventory_skill(query)
        elif "finance" in query_lower or "budget" in query_lower or "cost" in query_lower or "p&l" in query_lower:
            self.handle_finance_skill(query)
        elif "hr" in query_lower or "employee" in query_lower or "leave" in query_lower or "org" in query_lower:
            self.handle_hr_skill(query)
        elif "procurement" in query_lower or "purchase" in query_lower or "vendor" in query_lower or "po" in query_lower:
            self.handle_procurement_skill(query)
        elif "help" in query_lower:
            print("\nI can assist you with:")
            print("  • 📦 Sales Order Management")
            print("  • 📊 Product Inventory & Stock")
            print("  • 💰 Finance & Budgeting")
            print("  • 👥 HR & Employee Management")
            print("  • 🛒 Procurement & Vendors")
            print("  • 🔍 General Business Inquiries")
        else:
            print(f"\nI understand you're asking about '{query}'.")
            print("However, I'm currently trained on: Sales, Inventory, Finance, HR, and Procurement.")
            print("Try asking: 'Show me the budget report' or 'List employees in IT department'.")

    def handle_sales_skill(self, query):
        print("\nAccessing S/4HANA Sales Module...")
        time.sleep(0.5)
        data = [
            {"SalesOrder": "5000001", "Customer": "TechCorp Inc.", "Amount": "15,000.00 EUR", "Status": "🟢 Open", "Date": "2023-11-15"},
            {"SalesOrder": "5000002", "Customer": "SoftServe Ltd.", "Amount": "8,250.00 USD", "Status": "🚚 Shipped", "Date": "2023-11-18"},
            {"SalesOrder": "5000003", "Customer": "Global Automotives", "Amount": "125,000.00 EUR", "Status": "🔴 Blocked", "Date": "2023-11-19"}
        ]
        print("Here are the recent Sales Orders I found:")
        print(json.dumps(data, indent=2))

    def handle_inventory_skill(self, query):
        print("\nQuerying Material Management (MM)...")
        time.sleep(0.5)
        data = [
            {"ProductID": "HT-1000", "Name": "Notebook Basic 15", "Stock": 15, "Location": "Warehouse A"},
            {"ProductID": "HT-1001", "Name": "Notebook Basic 17", "Stock": 8, "Location": "Warehouse B"},
            {"ProductID": "HT-1002", "Name": "Ergo Screen E-I", "Stock": 120, "Location": "Warehouse A"}
        ]
        print("Current Inventory Status:")
        print(json.dumps(data, indent=2))

    def handle_finance_skill(self, query):
        print("\nAccessing SAP FI/CO (Finance & Controlling)...")
        time.sleep(0.5)
        data = [
            {"CostCenter": "CC-1000", "Department": "IT", "Budget": "250,000 EUR", "Spent": "187,500 EUR", "Remaining": "62,500 EUR"},
            {"CostCenter": "CC-2000", "Department": "Marketing", "Budget": "150,000 EUR", "Spent": "142,000 EUR", "Remaining": "8,000 EUR"},
            {"CostCenter": "CC-3000", "Department": "Operations", "Budget": "500,000 EUR", "Spent": "325,000 EUR", "Remaining": "175,000 EUR"}
        ]
        print("Budget Overview:")
        print(json.dumps(data, indent=2))

    def handle_hr_skill(self, query):
        print("\nAccessing SAP HCM (Human Capital Management)...")
        time.sleep(0.5)
        data = [
            {"EmployeeID": "EMP-1001", "Name": "Sarah Johnson", "Department": "IT", "Position": "Senior Developer", "LeaveBalance": "15 days"},
            {"EmployeeID": "EMP-1002", "Name": "Michael Chen", "Department": "Marketing", "Position": "Marketing Manager", "LeaveBalance": "10 days"},
            {"EmployeeID": "EMP-1003", "Name": "Emma Rodriguez", "Department": "Operations", "Position": "Operations Lead", "LeaveBalance": "22 days"}
        ]
        print("Employee Information:")
        print(json.dumps(data, indent=2))

    def handle_procurement_skill(self, query):
        print("\nAccessing SAP MM (Materials Management - Procurement)...")
        time.sleep(0.5)
        data = [
            {"PurchaseOrder": "PO-4500001", "Vendor": "Office Supplies Co.", "Amount": "5,000 USD", "Status": "🟢 Approved", "DeliveryDate": "2023-12-01"},
            {"PurchaseOrder": "PO-4500002", "Vendor": "Tech Equipment Ltd.", "Amount": "25,000 EUR", "Status": "⏳ Pending Approval", "DeliveryDate": "2023-12-15"},
            {"PurchaseOrder": "PO-4500003", "Vendor": "Cleaning Services Inc.", "Amount": "2,500 USD", "Status": "🚚 In Transit", "DeliveryDate": "2023-11-25"}
        ]
        print("Purchase Orders:")
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    agent = JouleAgent()
    agent.run()
