from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Mock Data for Asset Management (EAM)
EQUIPMENT = {
    "EQ-5001": {"name": "Hydraulic Press", "location": "Building A", "status": "Operational", "last_maintenance": "2025-10-01"},
    "EQ-5002": {"name": "Conveyor Belt", "location": "Building B", "status": "Down", "last_maintenance": "2025-09-15"},
    "EQ-5003": {"name": "Forklift 04", "location": "Warehouse", "status": "Operational", "last_maintenance": "2025-11-10"}
}

WORK_ORDERS = {
    "WO-9001": {"equipment": "EQ-5002", "type": "Repair", "status": "Assigned", "priority": "High"},
    "WO-9002": {"equipment": "EQ-5001", "type": "Inspection", "status": "Completed", "priority": "Medium"}
}

class MockEAMLLM:
    def invoke(self, input_dict):
        prompt = input_dict["input"]
        
        # Equipment Lookup
        if "EQ-" in prompt:
            for eq_id, data in EQUIPMENT.items():
                if eq_id in prompt:
                    return {"output": f"**Equipment {eq_id} ({data['name']})**:\n- Location: {data['location']}\n- Status: **{data['status']}**\n- Last Maint: {data['last_maintenance']}"}
            return {"output": "Equipment not found."}
            
        # Work Order Lookup
        if "WO-" in prompt:
            for wo_id, data in WORK_ORDERS.items():
                if wo_id in prompt:
                    return {"output": f"**Work Order {wo_id}**:\n- Equipment: {data['equipment']}\n- Type: {data['type']}\n- Status: **{data['status']}**\n- Priority: {data['priority']}"}
            return {"output": "Work Order not found."}

        return {"output": "I can help with Equipment (EQ-) and Work Orders (WO-)."}

def create_eam_agent():
    """
    Creates the Asset Management Agent (EAM).
    """
    return MockEAMLLM()
