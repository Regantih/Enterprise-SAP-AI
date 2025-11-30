from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
# In a real SAP BTP scenario, you would use:
# from generative_ai_hub.sdk.langchain.llm import ChatOpenAI as SAPChatOpenAI

from ..tools.sap_odata import create_sap_tool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_sales_agent():
    """
    Creates a Sales Agent capable of querying Sales Orders.
    """
    # Define Tools
    # Check if we have credentials, otherwise use Mock
    if os.getenv("SAP_ODATA_URL"):
        tools = [
            create_sap_tool("SalesOrderSet", "Query Sales Orders. Use standard OData params."),
            create_sap_tool("ProductSet", "Query Products and Inventory.")
        ]
        print("🔌 Connected to SAP System")
    else:
        from ..tools.mock_sap import create_mock_sap_tool
        tools = [
            create_mock_sap_tool("SalesOrderSet", "Query Sales Orders"),
            create_mock_sap_tool("ProductSet", "Query Products")
        ]
        print("⚠️  No Credentials found. Using MOCK SAP System.")

    # Initialize LLM
    # For local testing, we use standard OpenAI. 
    # On BTP, switch to SAP's proxy.
    llm = ChatOpenAI(temperature=0, model="gpt-4")

    # Initialize Agent
    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True,
        handle_parsing_errors=True
    )

    return agent

if __name__ == "__main__":
    print("🤖 SAP Sales Agent Initialized")
    agent = create_sales_agent()
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        try:
            response = agent.run(user_input)
            print(f"Agent: {response}")
        except Exception as e:
            print(f"Error: {e}")
