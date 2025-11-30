"""
Customer Demo Orchestrator
Simulates the specific multi-agent workflow for the "Budget vs Shipment" scenario.
Workflow:
1. Create Case
2. Refine Prompt
3. Identify Agents
4. Create Group Chat
5. Trigger Sub-agents
6. Synthesize Solution
"""
import time
import uuid
import json
from datetime import datetime

class DemoOrchestrator:
    def __init__(self):
        self.case_id = None
        self.agents = ['Finance', 'Procurement', 'Inventory', 'Sales']
        
    def run_demo(self):
        print("\n" + "="*80)
        print("🚀 SAP JOULE AGENT - CUSTOMER DEMO SCENARIO")
        print("="*80)
        
        user_query = "Even after the finance manager approves the budget to procure new equipment why is the customer order not shipped?"
        print(f"\n👤 CLIENT MANAGER: {user_query}")
        
        self.step_1_create_case(user_query)
        self.step_2_refine_prompt(user_query)
        self.step_3_identify_agents()
        self.step_4_group_chat_and_subagents()
        self.step_5_synthesis()

    def print_step(self, title):
        print(f"\n\n{'='*30} {title} {'='*30}")
        time.sleep(1)

    def step_1_create_case(self, query):
        self.print_step("STEP 1: CASE CREATION")
        self.case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
        print(f"🤖 SYSTEM: Analyzing incoming query severity...")
        time.sleep(0.5)
        print(f"✅ ACTION: Created Support Case {self.case_id}")
        print(f"📝 STATUS: Open - High Priority")
        print(f"🔗 CONTEXT: Cross-functional delay detected")

    def step_2_refine_prompt(self, query):
        self.print_step("STEP 2: PROMPT REFINEMENT")
        print("🤖 AGENT MANAGER: Refining user intent for technical execution...")
        time.sleep(1)
        refined = {
            "intent": "analyze_fulfillment_block",
            "entities": ["budget_approval", "procurement_process", "shipment_status"],
            "root_cause_hypothesis": "dependency_breakage"
        }
        print(f"✨ REFINED PROMPT: {json.dumps(refined, indent=2)}")

    def step_3_identify_agents(self):
        self.print_step("STEP 3: AGENT IDENTIFICATION")
        print("🤖 AGENT MANAGER: Identifying required domain experts...")
        time.sleep(0.5)
        for agent in self.agents:
            print(f"   👉 Identified: {agent} Agent")
            time.sleep(0.2)
        print(f"✅ DECISION: Initiating Multi-Agent Group Chat with {len(self.agents)} agents.")

    def step_4_group_chat_and_subagents(self):
        self.print_step("STEP 4: GROUP CHAT & SUB-AGENT EXECUTION")
        print(f"📢 CHANNEL: Group Chat {self.case_id} initialized.\n")
        
        # Finance
        self.simulate_agent_turn("Finance", "Checking budget approval status for equipment procurement.")
        self.simulate_subagent("Finance", "BudgetMonitor", "Verifying Cost Center CC-1000 approval logs...")
        print(f"   ✅ Finance Agent: Budget was APPROVED on 2023-11-10. Amount: €25,000. Status: RELEASED.")
        
        # Procurement
        self.simulate_agent_turn("Procurement", "Checking if Purchase Order was created against the budget.")
        self.simulate_subagent("Procurement", "PO_Tracker", "Scanning POs for Vendor 'Tech Equipment Ltd'...")
        print(f"   ⚠️  Procurement Agent: PO-4500002 found. Status: PENDING APPROVAL. Created: 2023-11-12.")
        print(f"   ⚠️  Procurement Agent: ISSUE DETECTED - PO is stuck in 'Manager Review' workflow step.")
        
        # Inventory
        self.simulate_agent_turn("Inventory", "Checking if equipment stock exists.")
        self.simulate_subagent("Inventory", "WarehouseBot", "Scanning bin locations for 'Notebook Basic 15'...")
        print(f"   ❌ Inventory Agent: Stock Level: 0. Equipment not received yet.")
        
        # Sales
        self.simulate_agent_turn("Sales", "Checking impact on Customer Order.")
        self.simulate_subagent("Sales", "OrderStatusBot", "Checking Sales Order 5000003...")
        print(f"   🚫 Sales Agent: Sales Order 5000003 is BLOCKED. Reason: 'Awaiting Stock Allocation'.")

    def simulate_agent_turn(self, agent, action):
        print(f"\n🔵 {agent.upper()} AGENT: {action}")
        time.sleep(0.5)

    def simulate_subagent(self, parent, name, action):
        print(f"   ↳ 🤖 Sub-agent '{name}' triggered: {action}")
        time.sleep(0.5)

    def step_5_synthesis(self):
        self.print_step("STEP 6: FINAL SYNTHESIS & RESOLUTION")
        print("🧠 AGENT MANAGER: Connecting the dots...")
        time.sleep(1)
        
        print("\n🎯 ROOT CAUSE IDENTIFIED:")
        print("1. Finance approved the budget. (✅)")
        print("2. Procurement created the PO, but it is STUCK in approval. (⚠️ THE BLOCKER)")
        print("3. Because PO is stuck, Vendor hasn't shipped equipment. (❌)")
        print("4. Because equipment hasn't arrived, Inventory is 0. (❌)")
        print("5. Because Inventory is 0, Sales Order cannot ship. (🚫)")
        
        print(f"\n✅ RECOMMENDED ACTION for Case {self.case_id}:")
        print("   👉 Nudge Procurement Manager to approve PO-4500002.")
        print("   👉 Notify Client Manager that shipment will proceed 24h after PO approval.")

if __name__ == "__main__":
    demo = DemoOrchestrator()
    demo.run_demo()
