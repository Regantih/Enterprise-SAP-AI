from langchain.tools import Tool
import random
import time

# Mock Database with SAP-like Schema
SALES_ORDERS = {
    "SO-5001": {
        "SalesOrder": "5001",
        "SoldToParty": "100010 (TechCorp)",
        "TotalNetAmount": 15000,
        "TransactionCurrency": "USD",
        "OverallSDProcessStatus": "Shipped",
        "SalesOrderItems": [
            {"SalesOrderItem": "10", "Material": "TG-11 (Laptop)", "OrderQuantity": 10}
        ]
    },
    "SO-5002": {
        "SalesOrder": "5002",
        "SoldToParty": "100020 (LogisticsSol)",
        "TotalNetAmount": 5000,
        "TransactionCurrency": "USD",
        "OverallSDProcessStatus": "Processing",
        "SalesOrderItems": [
            {"SalesOrderItem": "10", "Material": "TG-12 (Monitor)", "OrderQuantity": 20}
        ]
    }
}

CUSTOMERS = {
    "100010": {"Customer": "100010", "CustomerName": "TechCorp", "CreditLimitAmount": 50000},
    "100020": {"Customer": "100020", "CustomerName": "LogisticsSol", "CreditLimitAmount": 20000}
}

def check_order_status(order_id: str) -> str:
    """Checks the status of a Sales Order (A2X)."""
    print(f"   [Sales Tool] 🔍 Checking status for SalesOrder {order_id}...")
    time.sleep(0.5)
    
    # Normalize input (handle "SO-" prefix if present, though SAP uses numeric IDs usually)
    clean_id = order_id.replace("SO-", "")
    
    # Search in mock DB (handling both formats for demo)
    order = SALES_ORDERS.get(order_id) or SALES_ORDERS.get(f"SO-{clean_id}")
    
    if order:
        return f"Order **{order['SalesOrder']}** for {order['SoldToParty']} is currently **{order['OverallSDProcessStatus']}**. Amount: {order['TransactionCurrency']} {order['TotalNetAmount']}."
    return f"Sales Order {order_id} not found."

def check_customer_credit(customer_name_or_id: str) -> str:
    """Checks credit limit for a Customer."""
    print(f"   [Sales Tool] 💳 Checking credit for {customer_name_or_id}...")
    time.sleep(0.5)
    
    # Simple mock lookup
    for cust_id, data in CUSTOMERS.items():
        if customer_name_or_id in data['CustomerName'] or customer_name_or_id == cust_id:
             return f"Customer **{data['CustomerName']}** ({data['Customer']}) has a credit limit of **${data['CreditLimitAmount']}**."
             
    return f"Customer {customer_name_or_id} not found."

def create_sales_order(input_str: str) -> str:
    """Simulates creating a Sales Order. Input: 'SoldToParty, Material'"""
    print(f"   [Sales Tool] 📝 Creating Sales Order from input: {input_str}...")
    time.sleep(1.0)
    
    try:
        if "," not in input_str:
             return "Error: Invalid input. Use 'SoldToParty, Material'."
        
        sold_to, material = input_str.split(",", 1)
        sold_to = sold_to.strip()
        material = material.strip()
    except Exception as e:
        return f"Error parsing input: {e}"
    
    new_id = f"SO-{random.randint(6000, 9999)}"
    SALES_ORDERS[new_id] = {
        "SalesOrder": new_id.replace("SO-", ""),
        "SoldToParty": sold_to,
        "TotalNetAmount": random.randint(1000, 50000),
        "TransactionCurrency": "USD",
        "OverallSDProcessStatus": "Created",
        "SalesOrderItems": [
            {"SalesOrderItem": "10", "Material": material, "OrderQuantity": 1}
        ]
    }
    
    # TRIGGER: Agentic Workflow -> Update Supply Chain
    try:
        from src.agents.supply_chain_agent import update_demand_forecast
        scm_response = update_demand_forecast(material, 1) # Assume 1 unit for demo
        print(f"   [Sales Tool] 🔄 Workflow Triggered: {scm_response}")
    except Exception as e:
        print(f"   [Sales Tool] ⚠️ Workflow Error: {e}")

    return f"✅ Sales Order **{new_id}** created for {sold_to}. Material: {material}. Status: Created. (Supply Chain Notified)"

def get_sales_tools():
    return [
        Tool(
            name="CheckOrderStatus",
            func=check_order_status,
            description="Check the status of a Sales Order. Input: Order ID (e.g., 'SO-5001')."
        ),
        Tool(
            name="CheckCustomerCredit",
            func=check_customer_credit,
            description="Check customer credit limit and rating. Input: Customer Name (e.g., 'TechCorp')."
        ),
        Tool(
            name="CreateSalesOrder",
            func=create_sales_order,
            description="Create a new Sales Order. Input: Customer Name and Items (e.g., 'TechCorp, 5 Laptops')."
        )
    ]
