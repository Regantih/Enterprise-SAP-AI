from typing import Dict, List, Any, Callable
from dataclasses import dataclass
from src.core.mock_sap import mock_db

@dataclass
class ToolSchema:
    name: str
    description: str
    inputs: Dict[str, str]  # name: type_description
    outputs: Dict[str, str] # name: type_description
    func: Callable
    category: str

class MetaRegistry:
    def __init__(self):
        self.tools: Dict[str, ToolSchema] = {}
        self._register_tools()

    def _register_tools(self):
        # --- MM (Materials Management) ---
        self.register(ToolSchema(
            name="find_purchase_orders",
            description="Find Purchase Orders based on Vendor, Status, or Plant Location.",
            inputs={
                "vendor_name": "str (Optional) - Name of the vendor (e.g., 'Acme')",
                "status": "str (Optional) - Status of PO (Open, Late, Received, Blocked)",
                "plant_loc": "str (Optional) - Location of the plant (e.g., 'Berlin')"
            },
            outputs={"purchase_orders": "List[Dict] - List of PO objects"},
            func=mock_db.find_pos,
            category="MM"
        ))

        # --- FI (Finance) ---
        self.register(ToolSchema(
            name="find_invoices",
            description="Find Invoices based on Status or PO ID.",
            inputs={
                "status": "str (Optional) - Status of Invoice (Paid, Pending, Blocked)",
                "po_id": "str (Optional) - The Purchase Order ID linked to the invoice"
            },
            outputs={"invoices": "List[Dict] - List of Invoice objects"},
            func=mock_db.find_invoices,
            category="FI"
        ))

        # --- SD (Sales & Distribution) ---
        self.register(ToolSchema(
            name="find_sales_orders",
            description="Find Sales Orders based on Customer Name or Status.",
            inputs={
                "customer": "str (Optional) - Name of the customer",
                "status": "str (Optional) - Status of Order (Open, Shipped, Delayed)"
            },
            outputs={"sales_orders": "List[Dict] - List of Sales Order objects"},
            func=mock_db.find_sales_orders,
            category="SD"
        ))

        # --- UTILS ---
        self.register(ToolSchema(
            name="get_plant_id",
            description="Resolve a Plant Location Name to its SAP ID.",
            inputs={"location": "str - City or Name of the plant (e.g., 'Texas')"},
            outputs={"plant_id": "str - The 4-digit SAP Plant ID"},
            func=mock_db.get_plant_id,
            category="UTILS"
        ))

        # --- PREDICTIVE (SAP RPT-1) ---
        self.register(ToolSchema(
            name="analyze_vendor_risk",
            description="PREDICTIVE: Analyzes vendor delivery history to predict risk of delay.",
            inputs={"vendor_name": "str - Name of the vendor"},
            outputs={"prediction": "Dict - Risk score and reasoning"},
            func=mock_db.analyze_vendor_risk,
            category="PREDICTIVE"
        ))

    def register(self, schema: ToolSchema):
        self.tools[schema.name] = schema

    def get_tool(self, name: str) -> ToolSchema:
        return self.tools.get(name)

    def list_tools(self) -> List[Dict]:
        return [{
            "name": t.name,
            "description": t.description,
            "inputs": t.inputs,
            "category": t.category
        } for t in self.tools.values()]

# Singleton
registry = MetaRegistry()
