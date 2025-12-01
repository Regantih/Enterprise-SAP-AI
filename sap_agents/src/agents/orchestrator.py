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
        self.services = service_manager
        self.registry = capability_index.index
        self.audit_service = create_audit_service()
        self.trace_log = []
        self.current_plan = None

    def _log(self, stage, message):
        entry = f"[{datetime.now().isoformat()}] [{stage}]: {message}"
        print(entry)
        self.trace_log.append(entry)

    def plan(self, user_request, user_id="admin"):
        self.trace_log = [] # Reset trace
        transaction_id = str(uuid.uuid4())
        self._log("Planning Started", f"User: {user_id}, Request: {user_request}")
        
        try:
            # 1. Context Enrichment
            enriched_ctx = context_enricher.enrich(user_request, user_id)
            self._log("Context Enriched", str(enriched_ctx))
            
            # 2. Intent/Strategy
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
            fallback_plan = {
                "goal": user_request,
                "steps": [{"id": 1, "action": "error", "message": f"Planning failed: {str(e)}"}],
                "transaction_id": transaction_id
            }
            self.current_plan = fallback_plan
            return fallback_plan

    def _fallback_planning(self, user_request, plan):
        req = user_request.lower()
        
        # 1. System Health
        if "system status" in req or "health" in req:
             plan["steps"].append({"id": 1, "action": "system_check", "task": "Check Health"})
        
        # 2. Supply Chain Impact Analysis (Complex Scenario)
        elif any(x in req for x in ["impact", "delayed", "delay", "quality", "late"]):
            # Step 1: Procurement - Identify the Vendor/PO
            plan["steps"].append({
                "id": 1, 
                "action": "delegate", 
                "agent_criteria": "Procurement", 
                "task": f"Identify Purchase Orders related to: {user_request}"
            })
            # Step 2: Supply Chain - Check Inventory Buffer
            plan["steps"].append({
                "id": 2, 
                "action": "delegate", 
                "agent_criteria": "Supply Chain", 
                "task": "Check Safety Stock and Inventory Levels for impacted materials"
            })
            # Step 3: Sales - Identify Customer Impact
            plan["steps"].append({
                "id": 3, 
                "action": "delegate", 
                "agent_criteria": "Sales", 
                "task": "Identify Customer Orders allocated to these materials"
            })
            # Step 4: Finance - Assess Risk
            plan["steps"].append({
                "id": 4, 
                "action": "delegate", 
                "agent_criteria": "Finance", 
                "task": "Calculate financial risk and SLA penalties"
            })
            
        # 3. Order Status
        elif "status" in req or "order" in req:
             plan["steps"].append({
                 "id": 1, 
                 "action": "delegate", 
                 "agent_criteria": "Sales", 
                 "task": f"Check status of order: {user_request}"
             })
             
        # 4. Fallback
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
                        if a['agent'] == agent_name or a.get('category') == agent_name:
                            agent = a
                            break
                    
                    if agent:
                        agent_name = agent['agent'] # Update for audit
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
                        
                        output = f"[{agent['agent']}]: {secured_output}"
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
            self._log("Execution Error", str(e))
            return f"System Error during execution: {str(e)}"

    def _run_agent(self, agent, prompt):
        executor = None
        if agent['id'] == 'travel_agent' or agent.get('category') == 'Travel':
            executor = create_travel_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Travel Agent."

        elif agent['id'] == 'pl_planning' or agent.get('category') == 'Planning':
            executor = create_planning_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Planning Agent."

        elif agent['id'] == 'sus_sustainability' or agent.get('category') == 'Sustainability':
            executor = create_sustainability_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Sustainability Agent."

        elif agent['id'] == 'rag_knowledge' or agent.get('category') == 'Knowledge Base':
            executor = create_knowledge_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Knowledge Agent."

        elif agent['id'] == 'strat_market' or agent.get('category') == 'Market Intelligence':
            executor = create_market_intelligence_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Market Intelligence Agent."

        elif agent['id'] == 'pp_manufacturing' or agent.get('category') == 'Manufacturing':
            executor = create_manufacturing_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Manufacturing Agent."

        elif agent['id'] == 'eam_assets' or agent.get('category') == 'Asset Management':
            executor = create_eam_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Asset Management Agent."

        elif agent['id'] == 'cs_service' or agent.get('category') == 'Customer Service':
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

        elif agent['id'] == 'salesorderassistant' or agent.get('category') == 'Sales':
            executor = create_sales_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Sales Agent."

        elif agent['id'] == 'financereconciliationagent' or agent.get('category') == 'Finance':
            executor = create_finance_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Finance Agent."

        elif agent['id'] == 'hremployeeassistant' or agent.get('category') == 'HR':
            executor = create_hr_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize HR Agent."

        elif agent['id'] == 'scm_ibp' or agent.get('category') == 'Supply Chain':
            executor = create_supply_chain_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Supply Chain Agent."

        elif agent['id'] == 'ppm_projects' or agent.get('category') == 'Project Management':
            executor = create_project_agent()
            if executor:
                try:
                    res = executor.invoke({"input": prompt})
                    return res['output']
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: Could not initialize Project Agent."
            
        else:
            return f"I have analyzed '{prompt}' based on my expertise in {agent.get('category')}. [Simulated Result]"

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
