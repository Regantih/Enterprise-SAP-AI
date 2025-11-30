import argparse
import json
import sys
import re

class OrchestratorAgent:
    def __init__(self):
        self.trace = []
        self.tools = {
            "check_invoice_status": self.tool_check_invoice_status,
            "calculate_risk": self.tool_calculate_risk
        }

    def log(self, step, content):
        self.trace.append({
            "step": step,
            "content": content
        })

    def tool_check_invoice_status(self, invoice_id):
        # Deterministic tool logic
        if invoice_id == "INV-999":
            return {"status": "Blocked", "amount": 50.00, "variance": 10.00}
        return {"status": "Paid", "amount": 100.00, "variance": 0.00}

    def tool_calculate_risk(self, amount, variance):
        # Deterministic math logic
        threshold = 40.00
        if amount > threshold:
            return "High Risk"
        return "Low Risk"

    def tool_get_top_customers(self):
        # Mode A: Factual/Deterministic Data
        return [
            {"name": "TechCorp", "profit": 150000, "region": "NA"},
            {"name": "LogistiX", "profit": 120000, "region": "EU"},
            {"name": "BioHealth", "profit": 95000, "region": "APAC"}
        ]

    def tool_simulate_forecast(self, scenario_type, parameter):
        # Mode B: Predictive/Simulation
        # In a real system, this would run a Monte Carlo simulation or ML inference.
        if scenario_type == "price_increase":
            impact = parameter * 0.8 # Elasticity assumption
            return {
                "scenario": f"Price Increase of {parameter}%",
                "revenue_impact": f"+{impact}%",
                "risk": "Medium - Potential churn in APAC region"
            }
        return {"error": "Unknown scenario"}

    def run(self, prompt, explain=False):
        self.trace = []
        self.log("Input", prompt)

        # ReAct Loop Simulation (Deterministic)
        # In a real system, an LLM (temp=0) would decide these steps.
        # Here we implement the "Chain of Thought" logic in Python for the demo.

        response = {}

        # Step 1: Identify Intent
        if "invoice" in prompt.lower():
            # Extract ID
            match = re.search(r"INV-\d+", prompt)
            inv_id = match.group(0) if match else "INV-000"
            
            self.log("Decision", f"Call tool 'check_invoice_status' for {inv_id}")
            
            # Step 2: Execute Tool
            invoice_data = self.tools["check_invoice_status"](inv_id)
            self.log("Observation", f"Status is '{invoice_data['status']}'")

            # Step 3: Reasoning
            if invoice_data['status'] == "Blocked":
                self.log("Decision", "Invoice is blocked. Call 'calculate_risk'")
                
                # Step 4: Execute Next Tool
                risk = self.tools["calculate_risk"](invoice_data['amount'], invoice_data['variance'])
                self.log("Conclusion", f"Risk Level: {risk}")
                
                response["final_answer"] = f"Invoice {inv_id} is Blocked with {risk}."
            else:
                response["final_answer"] = f"Invoice {inv_id} is {invoice_data['status']}."
        
        # Mode A: Factual Analysis
        elif "profitable" in prompt.lower() and "customer" in prompt.lower():
            self.log("Decision", "Intent: Factual Analysis (Top Customers). Call 'get_top_customers'")
            data = self.tool_get_top_customers()
            self.log("Observation", f"Retrieved {len(data)} records from Data Warehouse.")
            
            # Format the output
            top_names = ", ".join([f"{c['name']} (${c['profit']:,})" for c in data])
            response["final_answer"] = f"The most profitable customers are: {top_names}."

        # Mode B: Predictive/Simulation
        elif "forecast" in prompt.lower() or "simulate" in prompt.lower():
            self.log("Decision", "Intent: Predictive Analysis. Call 'simulate_forecast'")
            
            # Extract parameter (simplified)
            param = 5 # Default to 5% if not found
            if "10%" in prompt: param = 10
            
            self.log("Action", f"Running Simulation: Price Increase {param}%")
            result = self.tool_simulate_forecast("price_increase", param)
            
            self.log("Observation", f"Simulation Complete. Impact: {result['revenue_impact']}")
            response["final_answer"] = f"Simulation Result: A {param}% price increase is projected to increase revenue by {result['revenue_impact']}. Risk: {result['risk']}."

        else:
            self.log("Decision", "Unknown intent")
            response["final_answer"] = "I can help with Invoices, Customer Profitability (Factual), or Forecasting (Simulation)."

        if explain:
            response["reasoning_trace"] = self.trace

        return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deterministic Orchestrator Agent')
    parser.add_argument('--prompt', type=str, required=True, help='User query')
    parser.add_argument('--explain', action='store_true', help='Include reasoning trace')
    
    args = parser.parse_args()
    
    agent = OrchestratorAgent()
    result = agent.run(args.prompt, args.explain)
    
    print(json.dumps(result, indent=2))
