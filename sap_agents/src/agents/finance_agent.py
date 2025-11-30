import os
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from src.tools.finance_tools import get_finance_tools

def create_finance_agent():
    """
    Creates the Finance Agent (Invoice Processing & Reconciliation).
    """
    # 1. Initialize LLM
    llm = None
    if os.getenv("GOOGLE_API_KEY"):
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    elif os.getenv("OPENAI_API_KEY"):
        llm = ChatOpenAI(temperature=0, model="gpt-4")
    
    if not llm:
        print("⚠️  No API Key found for Finance Agent. Returning None.")
        return None

    # 2. Load Tools
    tools = get_finance_tools()

    # 3. Define Prompt
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

    # 4. Create Agent
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True,
        max_iterations=15
    )
    
    return agent_executor
