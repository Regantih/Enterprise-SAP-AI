# SAP Joule Agent System - Architecture Specification

## 1. High-Level Architecture

The system follows a **Hub-and-Spoke** architecture where the **Joule Copilot** acts as the central orchestrator (Hub), connecting users to various specialized Agents (Spokes) and underlying business systems.

```mermaid
graph TD
    User[User] -->|Natural Language| Joule[Joule Copilot (Orchestrator)]
    
    subgraph "Agent Layer"
        Joule -->|Delegates| ProcAgent[Procurement Agent]
        Joule -->|Delegates| FinAgent[Finance Agent]
        Joule -->|Delegates| HRAgent[HR Agent]
    end
    
    subgraph "Skill Layer"
        ProcAgent --> Skill1[Supplier Analysis]
        ProcAgent --> Skill2[Market Research]
        FinAgent --> Skill3[Reconciliation]
        HRAgent --> Skill4[Onboarding]
    end
    
    subgraph "Data & Integration Layer"
        Skill1 -->|OData| S4HANA[S/4HANA Cloud]
        Skill2 -->|API| BDC[Business Data Cloud]
        Skill3 -->|OData| S4HANA
        Skill4 -->|OData| SF[SuccessFactors]
        
        KG[SAP Knowledge Graph] -.->|Context| Joule
        KG -.->|Semantics| ProcAgent
    end
```

## 2. Component Specifications

### 2.1 Orchestrator (Joule Copilot)
- **Role**: Intent recognition, routing, and context management.
- **Capabilities**:
  - Maintains conversation history.
  - Disambiguates user requests (e.g., "Create a PO" vs. "Check PO status").
  - Hands off complex tasks to specialized agents.

### 2.2 Specialized Agents
Each agent is a self-contained unit with specific domain knowledge.

| Agent | Domain | Key Responsibilities |
|-------|--------|----------------------|
| **Procurement Agent** | Sourcing & Procurement | Supplier negotiation, spend analysis, contract management. |
| **Finance Agent** | Financial Accounting | GL reconciliation, invoice processing, cash flow forecasting. |
| **HR Agent** | Human Capital Management | Onboarding, leave requests, policy Q&A. |

### 2.3 Skills & Tools
Agents execute tasks using "Skills".

- **Deterministic Skills**: Hard-coded logic or API calls (e.g., "Fetch PO #123").
- **Generative Skills**: LLM-based reasoning (e.g., "Draft a negotiation email").
- **Retrieval Skills**: RAG (Retrieval-Augmented Generation) from documents (e.g., "Summarize the travel policy").

## 3. Integration Architecture

### 3.1 SAP BTP Connectivity
- **Destinations**: Managed in BTP Cockpit, providing secure connectivity to backend systems.
- **Cloud Connector**: Tunnels securely from BTP to on-premise systems (if applicable).

### 3.2 Data Flow
1. **User Request**: "Analyze supplier performance for Acme Corp."
2. **Orchestration**: Joule identifies "Procurement" intent -> Routes to Procurement Agent.
3. **Reasoning**: Procurement Agent plans steps:
   - Step 1: Call `GetSupplierData` skill.
   - Step 2: Call `GetQualityScores` skill.
   - Step 3: Synthesize results using LLM.
4. **Execution**: Skills make OData calls to S/4HANA.
5. **Response**: Agent formats data + insights -> Returns to User.

## 4. Security Architecture

- **Authentication**: OAuth 2.0 via SAP Cloud Identity Services (IAS/XSUAA).
- **Authorization**: Role-based access control (RBAC).
  - Users must have specific role collections (e.g., `Procurement_Manager`) to access sensitive agents.
- **Data Privacy**:
  - PII redaction before sending to LLM.
  - Tenant isolation in BTP.

## 5. Scalability & Performance
- **Caching**: Cache frequent API responses (e.g., Supplier Master Data) in SAP HANA Cloud (Redis/DocStore) to reduce latency.
- **Async Processing**: Long-running tasks (e.g., "Generate monthly report") are handled asynchronously with user notifications upon completion.
