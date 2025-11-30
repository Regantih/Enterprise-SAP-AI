from langchain.tools import Tool
import json

class MockSAPTool:
    def __init__(self, entity_set):
        self.entity_set = entity_set

    def query(self, query_params: str) -> str:
        """Returns mock data for testing"""
        if "SalesOrder" in self.entity_set:
            return json.dumps([
                {"SalesOrder": "5000001", "Customer": "TechCorp", "NetAmount": "1500.00", "Currency": "EUR"},
                {"SalesOrder": "5000002", "Customer": "SoftServe", "NetAmount": "2300.00", "Currency": "USD"}
            ], indent=2)
        elif "Product" in self.entity_set:
            return json.dumps([
                {"ProductID": "HT-1000", "Name": "Notebook Basic 15", "Price": "956.00"},
                {"ProductID": "HT-1001", "Name": "Notebook Basic 17", "Price": "1249.00"},
                {"ProductID": "AG-2025", "Name": "Antigravity Propulsion Unit", "Price": "5000.00", "StockLevel": 5}
            ], indent=2)
        else:
            return json.dumps({"error": "Entity not found in mock data"})

def create_mock_sap_tool(entity_set: str, description: str) -> Tool:
    return Tool(
        name=f"query_{entity_set}",
        func=MockSAPTool(entity_set).query,
        description=f"Mock tool for {entity_set}. Returns sample data."
    )
