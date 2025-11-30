import argparse
import sys
import os
import json
from dotenv import load_dotenv

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Load environment variables
load_dotenv()

# Mock Data for Offline Mode
MOCK_SUPPLIERS = {
    "ACME Corp": {"rating": "A", "on_time_delivery": 98, "risk_score": "Low"},
    "Globex": {"rating": "C", "on_time_delivery": 75, "risk_score": "High"},
    "Soylent Corp": {"rating": "B", "on_time_delivery": 88, "risk_score": "Medium"}
}

def run_offline_agent(prompt):
    """
    Runs a simple rule-based agent when no LLM is available.
    """
    print("⚠️  OPENAI_API_KEY not found. Running in OFFLINE MOCK MODE.")
    
    # Simple keyword extraction
    supplier_found = None
    for name in MOCK_SUPPLIERS.keys():
        if name.lower() in prompt.lower():
            supplier_found = name
            break
            
    if supplier_found:
        data = MOCK_SUPPLIERS[supplier_found]
        recommendation = "Maintain relationship."
        if data['rating'] == 'A': recommendation = "Negotiate 2% discount."
        if data['rating'] == 'C': recommendation = "Audit required."
        
        return {
            "output": f"Analysis for {supplier_found}:\n- Rating: {data['rating']}\n- Delivery: {data['on_time_delivery']}%\n- Recommendation: {recommendation}"
        }
    else:
        return {
            "output": f"I couldn't find that supplier in the mock database. Available: {list(MOCK_SUPPLIERS.keys())}"
        }

def create_procurement_agent():
    """
    Creates a Procurement Agent capable of negotiating with suppliers.
    """
    # Check for OpenAI or Google Key
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        return None

    from langchain.agents import AgentExecutor, create_react_agent
    from langchain_community.chat_models import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.tools import Tool
    from langchain.prompts import PromptTemplate
    from src.tools.sap_odata import create_sap_tool
    from src.tools.mock_sap import create_mock_sap_tool
    from src.tools.inventory_tools import get_inventory_tools
    from src.tools.document_tools import get_document_tools

    # Define Tools
    tools = []
    
    # Add Inventory & Document Tools
    tools.extend(get_inventory_tools())
    tools.extend(get_document_tools())
    
    # SAP Tools (Real or Mock)
    if os.getenv("SAP_ODATA_URL"):
        print("🔌 Connecting to SAP System via OData...")
        tools.extend([
            create_sap_tool("SupplierSet", "Query Supplier details and performance."),
            create_sap_tool("PurchaseOrderSet", "Query Purchase Orders and history.")
        ])
    else:
        print("⚠️  No SAP_ODATA_URL found. Using MOCK SAP System.")
        tools.extend([
            create_mock_sap_tool("SupplierSet", "Query Supplier details"),
            create_mock_sap_tool("PurchaseOrderSet", "Query Purchase Orders")
        ])

    def get_market_pricing(query: str) -> str:
        return "Current market price for 'High-Performance Chips' is $450/unit. Trend: Stable."

    def negotiate_supplier(query: str) -> str:
        return "Generated Negotiation Strategy:\n1. Target Price: $420/unit\n2. Leverage: High volume commitment\n3. BATNA: Switch to Globex\n4. Strategy: Aggressive"

    tools.append(Tool(
        name="GetMarketPricing",
        func=get_market_pricing,
        description="Get current market pricing for commodities. Input: Commodity name."
    ))

    tools.append(Tool(
        name="NegotiateSupplier",
        func=negotiate_supplier,
        description="Generate a negotiation strategy for a supplier. Input: Supplier Name or Topic."
    ))

    try:
        if os.getenv("OPENAI_API_KEY"):
            llm = ChatOpenAI(temperature=0, model="gpt-4")
        elif os.getenv("GOOGLE_API_KEY"):
            print("🧠 Using Google Gemini...")
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    except Exception as e:
        print(f"⚠️  Could not initialize LLM: {e}")
        return None

    template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

    prompt = PromptTemplate.from_template(template)
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=50)

    return agent_executor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SAP Procurement Agent')
    parser.add_argument('--prompt', type=str, required=True, help='The user request')
    args = parser.parse_args()

    agent_executor = create_procurement_agent()
    
    if agent_executor:
        try:
            response = agent_executor.invoke({"input": args.prompt})
            print(f"OUTPUT:{response['output']}")
        except Exception as e:
            print(f"ERROR:{str(e)}")
    else:
        # Fallback to offline mode
        result = run_offline_agent(args.prompt)
        print(f"OUTPUT:{result['output']}")
