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
        
        # Production Order Lookup
        if "PO-" in prompt:
            for po_id, data in PRODUCTION_ORDERS.items():
                if po_id in prompt:
                    return {"output": f"**Production Order {po_id}**:\n- Material: {data['material']}\n- Quantity: {data['qty']}\n- Status: **{data['status']}**\n- Work Center: {data['work_center']}"}
            return {"output": "Production Order not found."}
            
        # Work Center Status
        if "WC-" in prompt or "work center" in prompt.lower():
            for wc_id, data in WORK_CENTERS.items():
                if wc_id in prompt:
                    return {"output": f"**Work Center {wc_id} ({data['name']})**:\n- Status: **{data['status']}**\n- Efficiency: {data['efficiency']}"}
            return {"output": "Work Center not found."}

        return {"output": "I can help with Production Orders (PO-) and Work Centers (WC-)."}

def create_manufacturing_agent():
    """
    Creates the Manufacturing Agent (PP).
    """
    return MockManufacturingLLM()
