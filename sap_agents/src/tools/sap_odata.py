from langchain.tools import Tool
from ..utils.auth import get_sap_session
import json

class SAPODataTool:
    def __init__(self, entity_set):
        self.entity_set = entity_set
        self.session, self.base_url = get_sap_session()

    def query(self, query_params: str) -> str:
        """
        Executes an OData query against the configured entity set.
        Args:
            query_params: OData query string (e.g., "$top=5&$select=SalesOrder,NetAmount")
        """
        if not self.base_url:
            return "Error: SAP_ODATA_URL not configured."

        # Ensure trailing slash
        url = f"{self.base_url.rstrip('/')}/{self.entity_set}"
        
        if query_params:
            url += f"?{query_params}"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Simplify response for LLM (remove metadata)
            results = data.get('d', {}).get('results', []) or data.get('value', [])
            return json.dumps(results, indent=2)
            
        except Exception as e:
            return f"Error querying SAP: {str(e)}"

def create_sap_tool(entity_set: str, description: str) -> Tool:
    """Factory function to create a LangChain Tool for a specific SAP Entity"""
    odata_tool = SAPODataTool(entity_set)
    
    return Tool(
        name=f"query_{entity_set}",
        func=odata_tool.query,
        description=f"Useful for querying {entity_set} from SAP. Input should be OData query parameters like '$top=5' or '$filter=ID eq 123'."
    )
