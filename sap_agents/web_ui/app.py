"""
SAP Joule Multi-Agent Web Interface
A simple Streamlit UI for chatting with the Joule Agent system.
"""
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.agents.specialized_agents import (
    SalesAgent, FinanceAgent, HRAgent, 
    ProcurementAgent, InventoryAgent
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'agents' not in st.session_state:
    st.session_state.agents = [
        SalesAgent(),
        FinanceAgent(),
        HRAgent(),
        ProcurementAgent(),
        InventoryAgent()
    ]

# Page config
st.set_page_config(
    page_title="SAP Joule Copilot",
    page_icon="💎",
    layout="wide"
)

# Header
st.title("💎 SAP Joule Multi-Agent System")
st.markdown("**AI-powered business assistant with specialized SAP agents**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🤖 Available Agents")
    st.markdown("The system will automatically route your question to the right expert:")
    
    st.markdown("**📦 Sales Agent**")
    st.caption("Sales orders, invoices, customers")
    
    st.markdown("**💰 Finance Agent**")
    st.caption("Budgets, cost centers, P&L")
    
    st.markdown("**👥 HR Agent**")
    st.caption("Employees, leave, org structure")
    
    st.markdown("**🛒 Procurement Agent**")
    st.caption("Purchase orders, vendors")
    
    st.markdown("**📊 Inventory Agent**")
    st.caption("Stock, warehouses, materials")
    
    st.markdown("---")
    st.caption("⚠️ Mode: Development (Mock Data)")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about sales, finance, HR, procurement, or inventory..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Find appropriate agent
    selected_agent = None
    priority_order = [
        st.session_state.agents[3],  # Procurement
        st.session_state.agents[1],  # Finance
        st.session_state.agents[2],  # HR
        st.session_state.agents[0],  # Sales
        st.session_state.agents[4]   # Inventory
    ]
    
    for agent in priority_order:
        if agent.can_handle(prompt):
            selected_agent = agent
            break
    
    # Generate response
    with st.chat_message("assistant"):
        if selected_agent:
            with st.spinner(f"Routing to {selected_agent.name}..."):
                result = selected_agent.process(prompt)
            
            response = f"**🎯 {result['agent']}**\n\n"
            response += f"Accessed: {selected_agent.module}\n\n"
            
            # Format data as markdown table
            if result['data']:
                data = result['data'][0]
                response += "**Results:**\n\n"
                
                # Create table header
                headers = list(data.keys())
                response += "| " + " | ".join(headers) + " |\n"
                response += "| " + " | ".join(["---"] * len(headers)) + " |\n"
                
                # Add rows
                for item in result['data']:
                    row = [str(item.get(h, "")) for h in headers]
                    response += "| " + " | ".join(row) + " |\n"
            else:
                response += "No data found."
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            response = """❓ I'm not sure which agent can help with that.

**Available expertise areas:**
- 📦 Sales & Orders
- 💰 Finance & Budgeting  
- 👥 HR & Employees
- 🛒 Procurement & Vendors
- 📊 Inventory & Stock

Try asking: *"Show me the budget"* or *"List purchase orders"*"""
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
