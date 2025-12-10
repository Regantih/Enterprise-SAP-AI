import re
from typing import Dict, List, Any
from difflib import get_close_matches
from src.core.meta_registry import registry
from src.core.mock_sap import mock_db
from src.core.graph_walker import graph_walker

class ReasoningEngine:
    def __init__(self):
        self.registry = registry
        self.db = mock_db
        self.graph_walker = graph_walker

    def is_multihop_query(self, prompt: str) -> bool:
        """
        Detect if the query requires multi-hop reasoning.
        Patterns: "X of Y", "X for the Y of Z", "X linked to Y"
        """
        multihop_patterns = [
            r'(risk|invoice|vendor|order).*(of|for).*(po|invoice|order|vendor)',
            r'find.*(for|of).*#?\d+',
            r'(linked|related|associated|connected)\s+to',
        ]
        prompt_lower = prompt.lower()
        return any(re.search(pattern, prompt_lower) for pattern in multihop_patterns)

    def analyze_intent(self, prompt: str) -> Dict[str, Any]:
        """
        Analyzes the prompt to determine the likely tool and parameters.
        Uses fuzzy matching against the database and registry.
        """
        prompt_lower = prompt.lower()
        plan = {"tool": None, "params": {}, "confidence": 0.0, "reasoning": []}

        # 1. Identify Entities (Fuzzy Match against DB)
        # Plants
        for plant in self.db.plants:
            if plant['location'].lower() in prompt_lower or plant['name'].lower() in prompt_lower:
                plan["params"]["plant_loc"] = plant['location']
                plan["reasoning"].append(f"Identified Plant Location: {plant['location']}")
                break
        
        # Vendors
        for vendor in self.db.vendors:
            if vendor['name'].lower() in prompt_lower:
                plan["params"]["vendor_name"] = vendor['name']
                plan["reasoning"].append(f"Identified Vendor: {vendor['name']}")
                break

        # Customers
        for so in self.db.sales_orders:
             if so['customer'].lower() in prompt_lower:
                plan["params"]["customer"] = so['customer']
                plan["reasoning"].append(f"Identified Customer: {so['customer']}")
                break

        # Status Keywords
        status_keywords = {
            "late": "Late", "delayed": "Late",
            "blocked": "Blocked", "hold": "Blocked",
            "open": "Open", "pending": "Pending",
            "paid": "Paid", "shipped": "Shipped"
        }
        for kw, status in status_keywords.items():
            if kw in prompt_lower:
                plan["params"]["status"] = status
                plan["reasoning"].append(f"Identified Status: {status} (from '{kw}')")
                break

        # Predictive Keywords (SAP RPT-1)
        predictive_keywords = ["risk", "likely", "prediction", "forecast", "chance"]
        is_predictive = any(kw in prompt_lower for kw in predictive_keywords)
        if is_predictive:
             plan["reasoning"].append("Detected Predictive Intent (SAP RPT-1 Logic)")

        # 3. Ambiguity Detection (The Enrichment Loop)
        # If the user explicitly mentions a generic entity ("vendor", "customer", "plant") 
        # but we failed to extract a specific name, we must ASK for it.
        
        if "vendor" in prompt_lower and "vendor_name" not in plan["params"]:
            return {
                "tool": "clarification",
                "message": "You mentioned a 'vendor', but I couldn't identify which one. Could you specify the Vendor Name? (e.g., 'Acme Corp', 'Globex')",
                "confidence": 1.0,
                "reasoning": plan["reasoning"] + ["Detected ambiguity: 'vendor' mentioned but no specific name found."]
            }
            
        if "customer" in prompt_lower and "customer" not in plan["params"]:
            return {
                "tool": "clarification",
                "message": "You mentioned a 'customer', but I missed the name. Which Customer are you referring to?",
                "confidence": 1.0,
                "reasoning": plan["reasoning"] + ["Detected ambiguity: 'customer' mentioned but no specific name found."]
            }

        if "plant" in prompt_lower and "plant_loc" not in plan["params"]:
             return {
                "tool": "clarification",
                "message": "Which Plant location are you interested in? (e.g., 'Berlin', 'Texas')",
                "confidence": 1.0,
                "reasoning": plan["reasoning"] + ["Detected ambiguity: 'plant' mentioned but no specific location found."]
            }

        # 4. Select Tool based on Entities (if no ambiguity)
        
        # Predictive Route (RPT-1)
        if is_predictive and "vendor_name" in plan["params"]:
             plan["tool"] = "analyze_vendor_risk"
             plan["confidence"] = 0.95
             
        # If Vendor found -> MM (PO)
        elif "vendor_name" in plan["params"]:
            plan["tool"] = "find_purchase_orders"
            plan["confidence"] = 0.9
        # If Customer found -> SD (Sales Order)
        elif "customer" in plan["params"]:
            plan["tool"] = "find_sales_orders"
            plan["confidence"] = 0.9
        # If "Invoice" mentioned -> FI
        elif "invoice" in prompt_lower:
            plan["tool"] = "find_invoices"
            plan["confidence"] = 0.8
        # If "Order" mentioned but no vendor/customer -> Ambiguous, default to PO if plant present
        elif "order" in prompt_lower:
            if "plant_loc" in plan["params"]:
                 plan["tool"] = "find_purchase_orders" # Default assumption
                 plan["confidence"] = 0.7
            else:
                 plan["tool"] = "find_purchase_orders" # Fallback
                 plan["confidence"] = 0.5

        if not plan["tool"]:
             plan["reasoning"].append("Could not determine specific tool. Defaulting to general search.")

        return plan

    def execute(self, prompt: str) -> Dict[str, Any]:
        """
        Executes the reasoning loop: Analyze -> Plan -> Execute -> Verify.
        Supports multi-hop queries via Knowledge Graph traversal.
        """
        
        # 1. Check for multi-hop query (Knowledge Graph route)
        if self.is_multihop_query(prompt):
            result = self.graph_walker.solve(prompt)
            if result["status"] == "success":
                return {
                    "status": "success",
                    "data": [result["data"]] if not isinstance(result["data"], list) else result["data"],
                    "tool_used": "GraphWalker",
                    "params_used": {},
                    "trace": {
                        "reasoning": [
                            "Detected multi-hop query pattern.",
                            f"Graph traversal path: {result.get('path', 'N/A')}",
                        ] + [f"Step: {t.get('step', 'N/A')}" for t in result.get("trace", [])],
                        "confidence": result.get("confidence", 0.9)
                    },
                    "graph_path": result.get("path")
                }
            # Fall through to simple reasoning if graph fails
        
        # 2. Simple query path (single tool)
        analysis = self.analyze_intent(prompt)
        
        if not analysis["tool"]:
            return {
                "status": "error",
                "message": "I could not understand the intent. Please specify Vendor, Customer, or Document type.",
                "trace": analysis
            }

        if analysis["tool"] == "clarification":
            return {
                "status": "success",
                "data": [],
                "tool_used": "EnrichmentLoop",
                "params_used": {},
                "trace": analysis,
                "message": analysis["message"] # Pass the question to the UI
            }

        tool_name = analysis["tool"]
        tool_schema = self.registry.get_tool(tool_name)
        
        if not tool_schema:
             return {"status": "error", "message": f"Tool {tool_name} not found."}

        # Execute Tool
        try:
            # Filter params to only those accepted by the tool
            valid_params = {k: v for k, v in analysis["params"].items() if k in tool_schema.inputs}
            
            result = tool_schema.func(**valid_params)
            
            return {
                "status": "success",
                "data": result,
                "tool_used": tool_name,
                "params_used": valid_params,
                "trace": analysis
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "trace": analysis
            }

# Singleton
engine = ReasoningEngine()
