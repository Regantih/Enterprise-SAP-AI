from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Mock Data for Manufacturing (PP)
PRODUCTION_ORDERS = {
    "PO-1001": {"material": "Turbine Blade", "qty": 50, "status": "In Progress", "start_date": "2025-11-01", "work_center": "WC-01"},
    "PO-1002": {"material": "Pump Housing", "qty": 20, "status": "Scheduled", "start_date": "2025-12-01", "work_center": "WC-02"},
    "PO-1003": {"material": "Control Valve", "qty": 100, "status": "Completed", "start_date": "2025-10-15", "work_center": "WC-03"}
}

WORK_CENTERS = {
    "WC-01": {"name": "CNC Milling", "status": "Running", "efficiency": "92%"},
    "WC-02": {"name": "Assembly Line A", "status": "Maintenance", "efficiency": "0%"},
    "WC-03": {"name": "Quality Inspection", "status": "Running", "efficiency": "98%"}
}

class MockManufacturingLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"]
        
        # 1. BOM Explosion (Bill of Materials)
        if "bom" in prompt.lower() or "bill of materials" in prompt.lower():
            if "turbine" in prompt.lower():
                return {
                    "output": """
**Bill of Materials for Turbine-X (BOM-1001)**:
- **TB-Blade-01**: Turbine Blade (Titanium) - Qty: 48
- **TB-Shaft-02**: Main Shaft (Steel Alloy) - Qty: 1
- **TB-House-03**: Housing Unit (Composite) - Qty: 1
- **TB-Bear-04**: High-Speed Bearings - Qty: 2 sets

*Inventory Status: All components available for 50 units.*
"""
                }
            elif "pump" in prompt.lower():
                return {
                    "output": """
**Bill of Materials for Pump-P1 (BOM-2002)**:
- **P-Case-01**: Pump Casing (Cast Iron) - Qty: 1
- **P-Imp-02**: Impeller (Bronze) - Qty: 1
- **P-Seal-03**: Mechanical Seal - Qty: 1

*Inventory Status: Seals are low stock (reorder advised).*
"""
                }
            return {"output": "I can show BOMs for 'Turbine-X' and 'Pump-P1'."}

        # 2. Work Center Status
        if "work center" in prompt.lower() or "capacity" in prompt.lower():
            if "wc-01" in prompt.lower() or "milling" in prompt.lower():
                return {"output": "**Work Center WC-01 (CNC Milling)**:\n- Status: 🟢 **Running**\n- Efficiency: 92%\n- Current Job: PO-1001 (Turbine Blades)\n- Queue: 4 Orders"}
            if "wc-02" in prompt.lower() or "assembly" in prompt.lower():
                return {"output": "**Work Center WC-02 (Assembly Line A)**:\n- Status: 🔴 **Maintenance**\n- Efficiency: 0%\n- ETA: 4 hours\n- Reason: Hydraulic Failure"}
            return {"output": "Available Work Centers: WC-01 (Milling), WC-02 (Assembly), WC-03 (Quality)."}

        # 3. Production Scheduling
        if "schedule" in prompt.lower() or "plan" in prompt.lower():
            return {
                "output": """
**Production Schedule Created (Simulated)**:
- **Order**: PO-NEW-001
- **Product**: Turbine-X
- **Quantity**: 500 Units
- **Start Date**: 2025-12-10
- **End Date**: 2025-12-25
- **Assigned Line**: WC-01 -> WC-02 -> WC-03

*Note: Schedule conflicts with WC-02 maintenance. Rerouting to Line B advised.*
"""
            }

        # 4. Production Order Lookup (Existing)
        if "PO-" in prompt:
            for po_id, data in PRODUCTION_ORDERS.items():
                if po_id in prompt:
                    return {"output": f"**Production Order {po_id}**:\n- Material: {data['material']}\n- Quantity: {data['qty']}\n- Status: **{data['status']}**\n- Work Center: {data['work_center']}"}
            return {"output": "Production Order not found."}

def create_manufacturing_agent():
    """
    Creates the Manufacturing Agent (PP).
    """
    return MockManufacturingLLM()
