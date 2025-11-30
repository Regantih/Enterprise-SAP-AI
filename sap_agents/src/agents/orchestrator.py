import json
import os
import sys
import random
from datetime import datetime
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agents.procurement_agent import create_procurement_agent, run_offline_agent
from src.agents.sales_agent import create_sales_agent
from src.agents.finance_agent import create_finance_agent
from src.agents.hr_agent import create_hr_agent
from src.agents.analytics_agent import create_analytics_agent
from src.agents.manufacturing_agent import create_manufacturing_agent
from src.agents.eam_agent import create_eam_agent
from src.agents.cs_agent import create_cs_agent
from src.agents.supply_chain_agent import create_supply_chain_agent
from src.agents.project_agent import create_project_agent
from src.agents.treasury_agent import create_treasury_agent
from src.agents.integration_agent import create_integration_agent
from src.agents.experience_agent import create_experience_agent
from src.agents.network_agent import create_network_agent
from src.agents.travel_agent import create_travel_agent
from src.agents.planning_agent import create_planning_agent
from src.agents.process_agent import create_process_agent
from src.agents.sustainability_agent import create_sustainability_agent
from src.agents.knowledge_agent import create_knowledge_agent
from src.agents.market_intelligence_agent import create_market_intelligence_agent

REGISTRY_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'registry.json')

from src.services.service_manager import service_manager
from src.services.capability_index import capability_index
from src.services.quality_guardrail import quality_guardrail
from src.services.context_enricher import context_enricher
from src.services.solution_architect import solution_architect
from src.services.data_privacy import data_privacy
from src.services.human_handoff import confidence_engine
from src.services.audit_service import create_audit_service

class OrchestratorAgent:
    def __init__(self):
        self.registry = self._load_registry()
        self.trace_log = []
        self.current_plan = None
        self.services = service_manager # Subscribe to services
        self.audit_service = create_audit_service()

    def _load_registry(self):
        try:
            with open(REGISTRY_PATH, 'r') as f:
                return json.load(f)['agents']
        except Exception as e:
            print(f"CRITICAL ERROR: Could not load registry: {e}")
            return []

    def _log(self, step, details):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "details": details
        }
        self.trace_log.append(entry)

    def plan(self, user_request, user_id="admin"):
        """
        Advanced Planning: Enrich -> Evaluate -> Plan
        """
        self.trace_log = [] # Reset trace
        self._log("Planning Start", f"Received request: {user_request}")
        
        # Generate Transaction ID
        transaction_id = str(uuid.uuid4())
        self.audit_service.log_event(transaction_id, "TRANSACTION", f"New Request: {user_request}")

        try:
            # 1. Context Enrichment
            enriched_ctx = context_enricher.enrich(user_request, user_id)
            self._log("Context Enrichment", f"Role: {enriched_ctx['user_role']}, Location: {enriched_ctx['user_location']}")
            
            # 2. Input Guardrail
            validation = quality_guardrail.validate_input(user_request)
            if not validation["valid"]:
                self._log("Guardrail Blocked", validation["reason"])
                self.audit_service.log_event(transaction_id, "BLOCKED", validation["reason"], "FAIL")
                plan = {
                    "goal": user_request,
                    "context": enriched_ctx,
                    "steps": [{"id": 1, "action": "block", "reason": validation["reason"]}],
                    "transaction_id": transaction_id
                }
                self.current_plan = plan
                return plan

            # 3. Solution Architect (Build vs. Buy)
            strategy = solution_architect.evaluate(enriched_ctx['enriched_prompt'])
            self._log("Solution Strategy", f"{strategy['strategy']} via {strategy['source']}")

            plan = {
                "goal": user_request,
                "context": enriched_ctx,
                "strategy": strategy,
                "transaction_id": transaction_id,
                "steps": []
            }

            # 4. Plan Generation based on Strategy
            if strategy['strategy'] == "OOTB":
                # Delegate to Standard Agent
                plan["steps"].append({
                    "id": 1,
                    "action": "delegate",
                    "agent_criteria": strategy['details']['agent'],
                    "task": user_request # Pass original request, agent handles specifics
                })
                self.audit_service.log_event(transaction_id, "DECISION", f"Routed to {strategy['details']['agent']}", "SUCCESS")
            elif strategy['strategy'] == "CUSTOM_ASSET":
                # Retrieve Custom Asset
                plan["steps"].append({
                    "id": 1,
                    "action": "custom_asset",
                    "asset_id": strategy['details']['id'],
                    "asset_name": strategy['details']['name']
                })
                self.audit_service.log_event(transaction_id, "DECISION", f"Selected Custom Asset: {strategy['details']['name']}", "SUCCESS")
            elif strategy['strategy'] == "NEW_BUILD":
                # Flag for Development
                plan["steps"].append({
                    "id": 1,
                    "action": "new_build",
                    "details": strategy['details']
                })
                self.audit_service.log_event(transaction_id, "DECISION", "Flagged for New Build", "SUCCESS")
            else:
                # Fallback to Heuristics (Legacy)
                self._fallback_planning(user_request, plan)
                self.audit_service.log_event(transaction_id, "DECISION", "Fallback to Heuristics", "WARNING")

            self.current_plan = plan
            self._log("Plan Generated", plan)
            return plan
            
        except Exception as e:
            self._log("Planning Error", str(e))
            self.audit_service.log_event(transaction_id, "ERROR", str(e), "CRITICAL")
            # Fallback Plan
            return {
                "goal": user_request,
                "steps": [{"id": 1, "action": "error", "message": f"Planning failed: {str(e)}"}],
                "transaction_id": transaction_id
            }

    def _fallback_planning(self, user_request, plan):
        # ... (Existing Heuristics Logic) ...
        if "system status" in user_request.lower() or "health" in user_request.lower():
             plan["steps"].append({"id": 1, "action": "system_check", "task": "Check Health"})
        elif "status" in user_request.lower():
             plan["steps"].append({"id": 1, "action": "clarify", "question": "Clarify: Order Status or Supplier Status?"})
        else:
             plan["steps"].append({"id": 1, "action": "clarify", "question": "I am not sure. Please clarify."})

    def execute(self):
        """
        Advanced Execution: Execute -> Secure -> Validate -> Audit
        """
        if not self.current_plan:
            return {"error": "No plan to execute"}
            
        results = []
        ctx = self.current_plan.get('context', {})
        user_role = ctx.get('user_role', 'Unknown')
        clearance = ctx.get('security_clearance', 'L1')
        transaction_id = self.current_plan.get('transaction_id', 'unknown')
        
        try:
            for step in self.current_plan['steps']:
                self._log("Execution Step", f"Executing Step {step['id']}: {step['action']}")
                self.audit_service.log_event(transaction_id, "ACTION", f"Executing {step['action']}")
                
                output = ""
                agent_name = "System"
                
                if step['action'] == 'error':
                    output = f"❌ **System Error**: {step['message']}"
                
                elif step['action'] == 'block':
                    output = f"[System]: 🛡️ Query blocked: {step['reason']}"

                elif step['action'] == 'system_check':
                    health = self.services.health_check()
                    status_msg = "\n".join([f"- {k}: {v}" for k, v in health.items()])
                    output = f"[System]: **Enterprise Services Status:**\n{status_msg}"

                elif step['action'] == 'custom_asset':
                    output = f"[System]: 🏗️ Executing Custom Asset: **{step['asset_name']}**... [Simulated Output]"

                elif step['action'] == 'new_build':
                    output = f"[System]: 🚧 Request flagged for **New Custom Build**. Ticket #CB-{random.randint(1000,9999)} created."

                elif step['action'] == 'delegate':
                    # Find Agent
                    agent_name = step['agent_criteria']
                    agent = None
                    for a in self.registry:
                        if a['name'] == agent_name or a['category'] == agent_name:
                            agent = a
                            break
                    
                    if agent:
                        agent_name = agent['name'] # Update for audit
                        # Execute Agent Logic
                        raw_output = self._run_agent(agent, step['task'])
                        
                        # 5. Data Privacy (Masking)
                        secured_output = data_privacy.secure_data(raw_output, user_role, clearance)
                        if secured_output != raw_output:
                            self._log("Data Privacy", "Sensitive data masked.")
                        
                        # 6. Output Guardrail
                        validation = quality_guardrail.validate_output(secured_output)
                        if not validation["valid"]:
                            self._log("Guardrail Warning", validation["reason"])
                            secured_output += f"\n\n*(System Note: Quality Flag: {validation['reason']})*"
                        
                        output = f"[{agent['name']}]: {secured_output}"
                    else:
                        output = f"[System]: Agent '{agent_name}' not found."
                
                elif step['action'] == 'clarify':
                    output = f"[Agent Manager]: {step['question']}"
                
                # 7. Confidence Engine & Audit
                audit = confidence_engine.evaluate(output, agent_name)
                self._log("Confidence Audit", f"Score: {audit['confidence_score']}, Status: {audit['review_status'] if 'review_status' in audit else 'Checked'}")
                self.audit_service.log_event(transaction_id, "OUTCOME", "Response generated", "SUCCESS")
                
                # Append Audit Trail
                output = confidence_engine.append_audit_info(output, audit)
                
                results.append(output)
                        
            final_response = "\n\n".join(results)
            self._log("Execution Complete", "Success")
            return final_response
            
        except Exception as e:
            error_msg = f"❌ **Critical Execution Error**: {str(e)}\n\n*Please contact IT Support.*"
            self._log("Execution Crash", str(e))
            return error_msg

    def _run_agent(self, agent, prompt):
        """
        Runs the specific agent logic.
        """
        if agent['id'] == 'analytics_strategy' or agent['category'] == 'Analytics':
            executor = create_analytics_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Analytics Agent."

        elif agent['id'] == 'xm_experience' or agent['category'] == 'Experience Management':
            executor = create_experience_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Experience Agent."

        elif agent['id'] == 'bn_network' or agent['category'] == 'Business Network':
            executor = create_network_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Network Agent."

        elif agent['id'] == 'tv_travel' or agent['category'] == 'Travel':
            executor = create_travel_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Travel Agent."

        elif agent['id'] == 'pl_planning' or agent['category'] == 'Planning':
            executor = create_planning_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Planning Agent."

        elif agent['id'] == 'sus_sustainability' or agent['category'] == 'Sustainability':
            executor = create_sustainability_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Sustainability Agent."

        elif agent['id'] == 'rag_knowledge' or agent['category'] == 'Knowledge Base':
            executor = create_knowledge_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Knowledge Agent."

        elif agent['id'] == 'strat_market' or agent['category'] == 'Market Intelligence':
            executor = create_market_intelligence_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Market Intelligence Agent."

        elif agent['id'] == 'pp_manufacturing' or agent['category'] == 'Manufacturing':
            executor = create_manufacturing_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Manufacturing Agent."

        elif agent['id'] == 'eam_assets' or agent['category'] == 'Asset Management':
            executor = create_eam_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Asset Management Agent."

        elif agent['id'] == 'cs_service' or agent['category'] == 'Customer Service':
            executor = create_cs_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Customer Service Agent."

        elif agent['id'] == 'procurementnegotiationassistant':
            # Run the real/mock procurement logic
            executor = create_procurement_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return run_offline_agent(prompt)['output']

        elif agent['id'] == 'salesorderassistant' or agent['category'] == 'Sales':
            executor = create_sales_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Sales Agent."

        elif agent['id'] == 'financereconciliationagent' or agent['category'] == 'Finance':
            executor = create_finance_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Finance Agent."

        elif agent['id'] == 'hremployeeassistant' or agent['category'] == 'HR':
            executor = create_hr_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize HR Agent."

        elif agent['id'] == 'scm_ibp' or agent['category'] == 'Supply Chain':
            executor = create_supply_chain_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Supply Chain Agent."

        elif agent['id'] == 'ppm_projects' or agent['category'] == 'Project Management':
            executor = create_project_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Project Agent."
            
        else:
            return f"I have analyzed '{prompt}' based on my expertise in {agent['category']}. [Simulated Result]"

    def get_trace(self):
        return self.trace_log

    def run(self, prompt, user_id="admin"):
        """
        Convenience method for one-shot execution (Plan + Execute).
        """
        plan = self.plan(prompt, user_id)
        if "error" in plan and "steps" not in plan:
             return plan["error"], "N/A"
             
        response = self.execute()
        transaction_id = plan.get('transaction_id', 'unknown')
        return response, transaction_id

# Global Instance
orchestrator = OrchestratorAgent()

def handle_request(prompt, user_id="admin"):
    orchestrator.plan(prompt, user_id)
    response = orchestrator.execute()
    return {
        "response": response,
        "trace": orchestrator.get_trace()
    }
