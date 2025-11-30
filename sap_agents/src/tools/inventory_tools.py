from langchain.tools import Tool
import json

# Expanded Mock Inventory Data (20 Items)
INVENTORY_DB = {
    "AG-2025": {"name": "Antigravity Propulsion Unit", "stock": 5, "supplier": "ACME Corp"},
    "HT-1000": {"name": "Notebook Basic 15", "stock": 25, "supplier": "Globex"},
    "HT-1001": {"name": "Notebook Basic 17", "stock": 8, "supplier": "Soylent Corp"},
    "HT-1002": {"name": "Notebook Pro 15", "stock": 60, "supplier": "ACME Corp"},
    "HT-1003": {"name": "Notebook Pro 17", "stock": 12, "supplier": "Globex"},
    "HT-1004": {"name": "ITelO Vault", "stock": 100, "supplier": "Soylent Corp"},
    "HT-1005": {"name": "ITelO Vault Net", "stock": 4, "supplier": "ACME Corp"},
    "HT-1006": {"name": "Vario Tablet 10", "stock": 30, "supplier": "Globex"},
    "HT-1007": {"name": "Vario Tablet 11", "stock": 9, "supplier": "Soylent Corp"},
    "HT-1008": {"name": "Vario Tablet 8", "stock": 55, "supplier": "ACME Corp"},
    "HT-1009": {"name": "Server Point 1000", "stock": 2, "supplier": "Globex"},
    "HT-1010": {"name": "Server Point 2000", "stock": 15, "supplier": "Soylent Corp"},
    "HT-1011": {"name": "Server Point 3000", "stock": 80, "supplier": "ACME Corp"},
    "HT-1012": {"name": "Mini Server", "stock": 3, "supplier": "Globex"},
    "HT-1013": {"name": "Large Server", "stock": 40, "supplier": "Soylent Corp"},
    "HT-1014": {"name": "Workstation Basic", "stock": 7, "supplier": "ACME Corp"},
    "HT-1015": {"name": "Workstation Pro", "stock": 22, "supplier": "Globex"},
    "HT-1016": {"name": "Monitor 24", "stock": 10, "supplier": "Soylent Corp"},
    "HT-1017": {"name": "Monitor 27", "stock": 5, "supplier": "ACME Corp"},
    "HT-1018": {"name": "Monitor 32", "stock": 50, "supplier": "Globex"}
}

SUPPLIER_DB = {
    "ACME Corp": "A",
    "Globex": "C",
    "Soylent Corp": "B"
}

def get_all_products(dummy: str = "") -> str:
    """Returns a list of all product IDs."""
    print("   [Tool] Fetching all product IDs...")
    return json.dumps(list(INVENTORY_DB.keys()))

def check_inventory(product_id: str) -> str:
    """Checks the inventory level for a given product ID."""
    # print(f"   [Tool] Checking inventory for {product_id}...") # Reduce noise
    product = INVENTORY_DB.get(product_id)
    if product:
        return json.dumps(product)
    else:
        return json.dumps({"error": "Product not found"})

def get_supplier_rating(product_id: str) -> str:
    """Gets the rating of the supplier for a product."""
    product = INVENTORY_DB.get(product_id)
    if not product:
        return "Error: Product not found"
    
    supplier = product.get("supplier")
    rating = SUPPLIER_DB.get(supplier, "Unknown")
    print(f"   [Tool] Supplier for {product_id} is {supplier} (Rating: {rating})")
    return rating

def schedule_restock(product_id: str, quantity: str) -> str:
    """Schedules a restock for a product."""
    print(f"   [Tool] Scheduling restock for {product_id} (Qty: {quantity})...")
    if product_id in INVENTORY_DB:
        INVENTORY_DB[product_id]['stock'] += int(quantity)
        return f"Success: Restocked {quantity} units."
    else:
        return "Error: Product not found."

def flag_for_review(product_id: str) -> str:
    """Flags a product for manual review."""
    print(f"   [Tool] 🚩 FLAGGED {product_id} for review (Supplier Risk).")
    return f"Success: {product_id} flagged."

def get_inventory_tools():
    return [
        Tool(
            name="GetAllProducts",
            func=get_all_products,
            description="Get a list of all available product IDs. Input: empty string."
        ),
        Tool(
            name="CheckInventory",
            func=check_inventory,
            description="Check stock level. Input: Product ID."
        ),
        Tool(
            name="GetSupplierRating",
            func=get_supplier_rating,
            description="Get the rating (A, B, C) of the supplier for a product. Input: Product ID."
        ),
        Tool(
            name="ScheduleRestock",
            func=lambda x: schedule_restock(x.split(',')[0].strip(), x.split(',')[1].strip()) if ',' in x else "Error: Input must be 'product_id, quantity'",
            description="Schedule restock. Input: 'product_id, quantity'."
        ),
        Tool(
            name="FlagForReview",
            func=flag_for_review,
            description="Flag a product for manual review due to supplier risk. Input: Product ID."
        )
    ]
