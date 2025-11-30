# SAP Agents Infrastructure

This project provides a framework for building AI Agents that interact with SAP systems using Python and LangChain.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration**:
    *   Copy `.env.template` to `.env`
    *   Fill in your SAP credentials (URL, Username, Password/API Key)
    *   If using SAP AI Core, fill in the `AICORE_*` variables.

## Components

*   **`src/tools/sap_odata.py`**: A generic LangChain tool for querying any SAP OData service.
*   **`src/agents/sap_agent.py`**: A sample "Sales Agent" that can query Sales Orders and Products.
*   **`src/utils/auth.py`**: Handles authentication with SAP systems.

## Usage

To run the sample agent:

```bash
python -m src.agents.sap_agent
```

## Customization

To add new tools, edit `src/agents/sap_agent.py` and add more `create_sap_tool()` calls for different Entity Sets (e.g., `BusinessPartnerSet`, `PurchaseOrderSet`).
