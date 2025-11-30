"""
Advanced Orchestrator with Reasoning Layer
Handles complex queries that require multiple agents working together.
"""
import json
from .specialized_agents import (
    SalesAgent, FinanceAgent, HRAgent, 
    ProcurementAgent, InventoryAgent
)

class ReasoningOrchestrator:
    def __init__(self):
        print("🧠 SAP Joule Advanced Multi-Agent System")
        print("=" * 50)
        print("⚠️  Mode: Development (Mock Data)")
        print("✨ Feature: Multi-Agent Reasoning")
        print("=" * 50)
        
        # Initialize specialized agents
        self.agents = {
            'sales': SalesAgent(),
            'finance': FinanceAgent(),
            'hr': HRAgent(),
            'procurement': ProcurementAgent(),
            'inventory': InventoryAgent()
        }
        
        print(f"\n✅ Loaded {len(self.agents)} specialized agents with reasoning capabilities")
    
    def run(self):
        print("\n\nJoule Reasoning System: I can answer complex questions by consulting")
        print("multiple experts and connecting the dots for you.\n")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\nJoule: Goodbye! Have a productive day.")
                    break
                
                self.process_complex_request(user_input)
            except KeyboardInterrupt:
                print("\n\nJoule: Goodbye!")
                break
    
    def process_complex_request(self, query):
        print("\n🧠 Analyzing query complexity...")
        
        # Determine which agents are needed
        needed_agents = self.identify_required_agents(query)
        
        if len(needed_agents) == 0:
            print("\n❓ I'm not sure how to help with that. Try asking about:")
            print("  - Budget and procurement issues")
            print("  - Sales order problems")  
            print("  - Employee availability")
            print("  - Inventory and stock issues")
            return
        
        if len(needed_agents) == 1:
            # Simple query - route to single agent
            agent_name = needed_agents[0]
            agent = self.agents[agent_name]
            print(f"\n🎯 Routing to: {agent.name}")
            result = agent.process(query)
            print(f"\n📊 Results from {result['agent']}:")
            print(json.dumps(result['data'], indent=2))
        else:
            # Complex query - multi-agent reasoning
            print(f"\n🔍 Complex query detected - consulting {len(needed_agents)} agents")
            self.multi_agent_reasoning(query, needed_agents)
    
    def identify_required_agents(self, query):
        """Identify which agents are needed for the query"""
        lower = query.lower()
        needed = []
        
        # Check each agent
        if any(word in lower for word in ['budget', 'finance', 'cost', 'approved', 'spending']):
            needed.append('finance')
        if any(word in lower for word in ['procurement', 'purchase', 'vendor', 'equipment', 'procure']):
            needed.append('procurement')
        if any(word in lower for word in ['sales', 'order', 'customer', 'shipped', 'ship']):
            needed.append('sales')
        if any(word in lower for word in ['inventory', 'stock', 'warehouse', 'material']):
            needed.append('inventory')
        if any(word in lower for word in ['employee', 'hr', 'staff', 'personnel']):
            needed.append('hr')
        
        return needed
    
    def multi_agent_reasoning(self, query, agent_names):
        """Consult multiple agents and synthesize an answer"""
        print("\n" + "=" * 50)
        print("🤝 MULTI-AGENT COLLABORATION")
        print("=" * 50)
        
        # Gather data from each agent
        agent_results = {}
        for agent_name in agent_names:
            agent = self.agents[agent_name]
            print(f"\n📞 Consulting {agent.name}...")
            result = agent.process(query)
            agent_results[agent_name] = result
            print(f"   ✓ Data received from {agent.module}")
        
        # Synthesize the answer
        print("\n" + "=" * 50)
        print("💡 REASONING & SYNTHESIS")
        print("=" * 50)
        
        self.synthesize_answer(query, agent_results)
    
    def synthesize_answer(self, query, results):
        """Generate a reasoning-based answer from multiple data sources"""
        
        print("\n🧠 Analyzing data from all agents...\n")
        
        # Show data from each agent
        for agent_name, result in results.items():
            print(f"\n📊 {result['agent']} Data:")
            print(json.dumps(result['data'][:2], indent=2))  # Show first 2 items
            if len(result['data']) > 2:
                print(f"   ... and {len(result['data']) - 2} more items")
        
        # Generate reasoning based on the query type
        print("\n" + "-" * 50)
        print("🎯 ANSWER & INSIGHTS:")
        print("-" * 50)
        
        if 'finance' in results and 'procurement' in results and 'sales' in results:
            print("\n💡 Analyzing budget → procurement → sales flow:\n")
            
            finance_data = results['finance']['data']
            proc_data = results['procurement']['data']
            sales_data = results['sales']['data']
            
            # Find blocked orders
            blocked_orders = [s for s in sales_data if 'Blocked' in s.get('Status', '')]
            pending_pos = [p for p in proc_data if 'Pending' in p.get('Status', '')]
            
            if blocked_orders:
                print(f"⚠️  Found {len(blocked_orders)} blocked sales order(s):")
                for order in blocked_orders:
                    print(f"   - Order {order['SalesOrder']} to {order['Customer']} (€{order['Amount']})")
            
            if pending_pos:
                print(f"\n⏳ Found {len(pending_pos)} pending procurement order(s):")
                for po in pending_pos:
                    print(f"   - PO {po['PurchaseOrder']} from {po['Vendor']} (€{po['Amount']})")
            
            print("\n📋 LIKELY CAUSE:")
            if pending_pos and blocked_orders:
                print("   → Budget was approved (Finance ✓)")
                print("   → Purchase order created but NOT YET approved (Procurement ⏳)")
                print("   → Equipment not ordered, so can't fulfill customer order")
                print("   → Sales order is BLOCKED waiting for inventory")
            else:
                print("   → All procurement is approved")
                print("   → Blocked order may be due to other reasons (credit check, pricing, etc.)")
        
        elif 'inventory' in results and 'sales' in results:
            print("\n💡 Checking inventory vs sales orders:")
            sales_data = results['sales']['data']
            inv_data = results['inventory']['data']
            
            print(f"   → {len(inv_data)} products in stock")
            print(f"   → {len(sales_data)} sales orders")
            
            # Find low stock items
            low_stock = [i for i in inv_data if isinstance(i.get('Stock'), (int, str)) and int(str(i['Stock'])) < 10]
            if low_stock:
                print(f"\n⚠️  Low stock alert on {len(low_stock)} items:")
                for item in low_stock:
                    print(f"   - {item['Name']}: {item['Stock']} units")
        
        else:
            print("\n   → Data gathered from multiple systems")
            print("   → Review the information above for insights")

if __name__ == "__main__":
    orchestrator = ReasoningOrchestrator()
    orchestrator.run()
