"""
Specialized SAP Agents
Each agent focuses on a specific business domain and has deep knowledge of that area.
"""
import json
import time

class BaseSpecializedAgent:
    """Base class for specialized agents"""
    def __init__(self, name, module):
        self.name = name
        self.module = module
    
    def can_handle(self, query):
        """Determine if this agent can handle the query"""
        raise NotImplementedError
    
    def process(self, query):
        """Process the query and return results"""
        raise NotImplementedError

class SalesAgent(BaseSpecializedAgent):
    def __init__(self):
        super().__init__("Sales Agent", "S/4HANA Sales")
        self.keywords = ["sales", "order", "customer", "invoice"]
    
    def can_handle(self, query):
        return any(keyword in query.lower() for keyword in self.keywords)
    
    def process(self, query):
        print(f"\n🤖 {self.name}: Accessing {self.module}...")
        time.sleep(0.5)
        data = [
            {"SalesOrder": "5000001", "Customer": "TechCorp Inc.", "Amount": "15,000.00 EUR", "Status": "🟢 Open", "Date": "2023-11-15"},
            {"SalesOrder": "5000002", "Customer": "SoftServe Ltd.", "Amount": "8,250.00 USD", "Status": "🚚 Shipped", "Date": "2023-11-18"},
            {"SalesOrder": "5000003", "Customer": "Global Automotives", "Amount": "125,000.00 EUR", "Status": "🔴 Blocked", "Date": "2023-11-19"}
        ]
        return {"agent": self.name, "data": data}

class FinanceAgent(BaseSpecializedAgent):
    def __init__(self):
        super().__init__("Finance Agent", "SAP FI/CO")
        self.keywords = ["finance", "budget", "cost", "p&l", "financial"]
    
    def can_handle(self, query):
        return any(keyword in query.lower() for keyword in self.keywords)
    
    def process(self, query):
        print(f"\n🤖 {self.name}: Accessing {self.module}...")
        time.sleep(0.5)
        data = [
            {"CostCenter": "CC-1000", "Department": "IT", "Budget": "250,000 EUR", "Spent": "187,500 EUR", "Remaining": "62,500 EUR"},
            {"CostCenter": "CC-2000", "Department": "Marketing", "Budget": "150,000 EUR", "Spent": "142,000 EUR", "Remaining": "8,000 EUR"},
            {"CostCenter": "CC-3000", "Department": "Operations", "Budget": "500,000 EUR", "Spent": "325,000 EUR", "Remaining": "175,000 EUR"}
        ]
        return {"agent": self.name, "data": data}

class HRAgent(BaseSpecializedAgent):
    def __init__(self):
        super().__init__("HR Agent", "SAP HCM")
        self.keywords = ["hr", "employee", "leave", "org", "staff", "personnel"]
    
    def can_handle(self, query):
        return any(keyword in query.lower() for keyword in self.keywords)
    
    def process(self, query):
        print(f"\n🤖 {self.name}: Accessing {self.module}...")
        time.sleep(0.5)
        data = [
            {"EmployeeID": "EMP-1001", "Name": "Sarah Johnson", "Department": "IT", "Position": "Senior Developer", "LeaveBalance": "15 days"},
            {"EmployeeID": "EMP-1002", "Name": "Michael Chen", "Department": "Marketing", "Position": "Marketing Manager", "LeaveBalance": "10 days"},
            {"EmployeeID": "EMP-1003", "Name": "Emma Rodriguez", "Department": "Operations", "Position": "Operations Lead", "LeaveBalance": "22 days"}
        ]
        return {"agent": self.name, "data": data}

class ProcurementAgent(BaseSpecializedAgent):
    def __init__(self):
        super().__init__("Procurement Agent", "SAP MM (Procurement)")
        self.keywords = ["procurement", "purchase", "vendor", "po", "requisition"]
    
    def can_handle(self, query):
        return any(keyword in query.lower() for keyword in self.keywords)
    
    def process(self, query):
        print(f"\n🤖 {self.name}: Accessing {self.module}...")
        time.sleep(0.5)
        data = [
            {"PurchaseOrder": "PO-4500001", "Vendor": "Office Supplies Co.", "Amount": "5,000 USD", "Status": "🟢 Approved", "DeliveryDate": "2023-12-01"},
            {"PurchaseOrder": "PO-4500002", "Vendor": "Tech Equipment Ltd.", "Amount": "25,000 EUR", "Status": "⏳ Pending Approval", "DeliveryDate": "2023-12-15"},
            {"PurchaseOrder": "PO-4500003", "Vendor": "Cleaning Services Inc.", "Amount": "2,500 USD", "Status": "🚚 In Transit", "DeliveryDate": "2023-11-25"}
        ]
        return {"agent": self.name, "data": data}

class InventoryAgent(BaseSpecializedAgent):
    def __init__(self):
        super().__init__("Inventory Agent", "SAP MM (Materials)")
        self.keywords = ["inventory", "stock", "product", "warehouse", "material"]
    
    def can_handle(self, query):
        return any(keyword in query.lower() for keyword in self.keywords)
    
    def process(self, query):
        print(f"\n🤖 {self.name}: Accessing {self.module}...")
        time.sleep(0.5)
        data = [
            {"ProductID": "HT-1000", "Name": "Notebook Basic 15", "Stock": 15, "Location": "Warehouse A"},
            {"ProductID": "HT-1001", "Name": "Notebook Basic 17", "Stock": 8, "Location": "Warehouse B"},
            {"ProductID": "HT-1002", "Name": "Ergo Screen E-I", "Stock": 120, "Location": "Warehouse A"}
        ]
        return {"agent": self.name, "data": data}
