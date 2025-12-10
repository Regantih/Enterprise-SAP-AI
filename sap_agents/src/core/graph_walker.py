"""
Graph Walker: Executes multi-hop queries by traversing the Knowledge Graph.
"""
from typing import Dict, Any, List, Optional
from src.core.knowledge_graph import knowledge_graph, GraphEdge
from src.core.meta_registry import registry
from src.core.mock_sap import mock_db

class GraphWalker:
    """
    Executes a path of tool calls discovered by the Knowledge Graph.
    Supports multi-hop reasoning like: "Find risk for vendor of Invoice #999"
    """
    
    def __init__(self):
        self.graph = knowledge_graph
        self.registry = registry
        self.db = mock_db
        
    def detect_entities(self, prompt: str) -> Dict[str, Any]:
        """
        Extract entity types and instance values from the prompt.
        Returns: {"start_entity": "Invoice", "start_value": "999", "end_entity": "RiskAssessment"}
        """
        prompt_lower = prompt.lower()
        result = {"start_entity": None, "start_value": None, "end_entity": None}
        
        # Detect target entity (what we want to find)
        if any(kw in prompt_lower for kw in ["risk", "prediction", "forecast"]):
            result["end_entity"] = "RiskAssessment"
        elif "invoice" in prompt_lower and ("find" in prompt_lower or "get" in prompt_lower):
            result["end_entity"] = "Invoice"
        elif "order" in prompt_lower or "po" in prompt_lower:
            result["end_entity"] = "PurchaseOrder"
        elif "vendor" in prompt_lower:
            result["end_entity"] = "Vendor"
            
        # Detect source entity (what we're starting from)
        if "invoice" in prompt_lower:
            result["start_entity"] = "Invoice"
            # Try to extract ID
            import re
            match = re.search(r'invoice\s*#?\s*(\d+)', prompt_lower)
            if match:
                result["start_value"] = match.group(1)
                
        elif "po" in prompt_lower or "purchase order" in prompt_lower:
            result["start_entity"] = "PurchaseOrder"
            import re
            match = re.search(r'po\s*#?\s*(\d+)', prompt_lower)
            if match:
                result["start_value"] = match.group(1)
                
        elif "vendor" in prompt_lower:
            result["start_entity"] = "Vendor"
            # Try to extract vendor name (check against DB)
            for vendor in self.db.vendors:
                if vendor['name'].lower() in prompt_lower:
                    result["start_value"] = vendor['name']
                    break
                    
        return result

    def execute_path(self, path: List[GraphEdge], start_data: Any) -> Dict[str, Any]:
        """
        Execute a chain of tool calls along the graph path.
        
        Args:
            path: List of edges to traverse
            start_data: Initial data (e.g., an Invoice object)
            
        Returns:
            Final result after all traversals
        """
        current_data = start_data
        trace = []
        
        for edge in path:
            tool_schema = self.registry.get_tool(edge.tool_name)
            
            if not tool_schema:
                # Handle virtual tools (data extraction without API call)
                
                if edge.tool_name == "get_vendor_from_po":
                    # Extract vendor from PO data
                    if isinstance(current_data, dict):
                        current_data = {"name": current_data.get("vendor_name")}
                    elif isinstance(current_data, list) and current_data:
                        current_data = {"name": current_data[0].get("vendor_name")}
                    trace.append({
                        "step": f"{edge.source} -> {edge.target}",
                        "tool": edge.tool_name,
                        "result": f"Extracted vendor: {current_data.get('name', 'N/A')}"
                    })
                    continue
                    
                elif edge.tool_name == "get_po_from_invoice":
                    # Extract PO ID from Invoice data and fetch PO
                    po_id = None
                    if isinstance(current_data, dict):
                        po_id = current_data.get("po_id")
                    elif isinstance(current_data, list) and current_data:
                        po_id = current_data[0].get("po_id")
                    
                    if po_id:
                        pos = [p for p in self.db.purchase_orders if p['id'] == po_id]
                        current_data = pos[0] if pos else {}
                    trace.append({
                        "step": f"{edge.source} -> {edge.target}",
                        "tool": edge.tool_name,
                        "result": f"Fetched PO #{po_id}"
                    })
                    continue
                    
                elif edge.tool_name == "get_customer_from_so":
                    # Extract customer from Sales Order
                    if isinstance(current_data, dict):
                        current_data = {"name": current_data.get("customer")}
                    elif isinstance(current_data, list) and current_data:
                        current_data = {"name": current_data[0].get("customer")}
                    trace.append({
                        "step": f"{edge.source} -> {edge.target}",
                        "tool": edge.tool_name,
                        "result": f"Extracted customer: {current_data.get('name', 'N/A')}"
                    })
                    continue
                    
                else:
                    trace.append({"step": edge.relation, "error": f"Tool {edge.tool_name} not found"})
                    continue
            
            # Build parameters from current data
            params = {}
            for source_attr, tool_param in edge.param_map.items():
                if isinstance(current_data, dict):
                    if source_attr in current_data:
                        params[tool_param] = current_data[source_attr]
                    elif source_attr == "name" and "vendor_name" in current_data:
                        params[tool_param] = current_data["vendor_name"]
                elif isinstance(current_data, list) and current_data:
                    first = current_data[0]
                    if isinstance(first, dict) and source_attr in first:
                        params[tool_param] = first[source_attr]
            
            # Execute tool
            try:
                result = tool_schema.func(**params)
                trace.append({
                    "step": f"{edge.source} --({edge.relation})--> {edge.target}",
                    "tool": edge.tool_name,
                    "params": params,
                    "result_count": len(result) if isinstance(result, list) else 1
                })
                current_data = result
            except Exception as e:
                trace.append({"step": edge.relation, "error": str(e)})
                break
                
        return {
            "final_result": current_data,
            "traversal_trace": trace
        }

    def solve(self, prompt: str) -> Dict[str, Any]:
        """
        Main entry point: Solve a multi-hop query.
        
        Example: "Find the risk for the vendor of PO #4500123"
        """
        # 1. Detect entities
        entities = self.detect_entities(prompt)
        
        if not entities["start_entity"] or not entities["end_entity"]:
            return {
                "status": "error",
                "message": "Could not identify source and target entities.",
                "entities_detected": entities
            }
            
        # 2. Find path in graph
        path = self.graph.find_path(entities["start_entity"], entities["end_entity"])
        
        if not path and entities["start_entity"] != entities["end_entity"]:
            return {
                "status": "error", 
                "message": f"No path from {entities['start_entity']} to {entities['end_entity']}.",
                "entities_detected": entities
            }
            
        # 3. Get starting data
        start_data = self._get_start_data(entities)
        
        if not start_data:
            return {
                "status": "error",
                "message": f"Could not find {entities['start_entity']} with value {entities['start_value']}.",
                "entities_detected": entities
            }
            
        # 4. Execute the path
        result = self.execute_path(path, start_data)
        
        return {
            "status": "success",
            "data": result["final_result"],
            "path": self.graph.explain_path(path),
            "trace": result["traversal_trace"],
            "tool_used": "GraphWalker",
            "confidence": 0.95
        }
        
    def _get_start_data(self, entities: Dict) -> Optional[Any]:
        """Fetch the starting entity data."""
        entity_type = entities["start_entity"]
        value = entities["start_value"]
        
        if entity_type == "Invoice" and value:
            invoices = [i for i in self.db.invoices if value in i['id']]
            return invoices[0] if invoices else None
            
        elif entity_type == "PurchaseOrder" and value:
            pos = [p for p in self.db.purchase_orders if value in p['id']]
            return pos[0] if pos else None
            
        elif entity_type == "Vendor" and value:
            return {"name": value}
            
        return None

# Singleton
graph_walker = GraphWalker()
