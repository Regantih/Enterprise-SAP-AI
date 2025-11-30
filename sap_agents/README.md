# 🚀 Enterprise AI Platform (v2.0)

**An Autonomous Multi-Agent System for SAP Enterprise Environments.**

This platform leverages a **Hub-and-Spoke Architecture** to orchestrate over **80+ Specialized Agents** across Finance, Supply Chain, HR, and IT. It features advanced reasoning, real-time RAG (Retrieval Augmented Generation), and strict enterprise guardrails.

![Status](https://img.shields.io/badge/Status-Live-green) ![Version](https://img.shields.io/badge/Version-2.0-blue) ![Agents](https://img.shields.io/badge/Agents-80%2B-purple)

---

## 🏗️ Architecture

The system uses a central **Orchestrator Agent** that intelligently routes queries to specialized sub-agents based on a **Capability Index**.

```mermaid
graph TD
    User[User / Executive] -->|Query| WebUI[Web Dashboard]
    WebUI -->|API| Orch[Orchestrator Agent]
    
    subgraph "Brain / Core Services"
        Orch -->|Plan| CapIndex[Capability Index]
        Orch -->|Verify| Guard[Quality Guardrails]
        Orch -->|Secure| Privacy[Data Privacy Layer]
    end
    
    subgraph "Specialized Agents"
        Orch -->|Route| Fin[Finance Agent]
        Orch -->|Route| SCM[Supply Chain Agent]
        Orch -->|Route| HR[HR Agent]
        Orch -->|Route| IT[IT / Helpdesk Agent]
    end
    
    Fin -->|OData| SAP_S4[SAP S/4HANA]
    SCM -->|API| SAP_IBP[SAP IBP]
    HR -->|API| SuccessFactors[SAP SuccessFactors]
```

## ✨ Key Features

*   **🧠 Intelligent Orchestration**: Dynamically breaks down complex requests (e.g., "Check budget AND schedule meeting") into sub-tasks.
*   **🛡️ Enterprise Guardrails**:
    *   **Input**: Blocks irrelevant or malicious queries ("Hi", "Ignore instructions").
    *   **Output**: Validates formatting and tone.
    *   **Privacy**: Masks sensitive PII/Financial data based on user role.
*   **📚 RAG Knowledge Base**: Answers policy questions using vector search on PDF documents.
*   **🤝 Human Handoff**: Automatically flags low-confidence responses for human review.
*   **📊 Executive Dashboard**: Real-time widgets for System Health, Revenue, and ESG Scores.

---

## 🚀 Demo Script (The "VP of Sales" Flow)

Use these prompts to demonstrate the system's capabilities:

| Persona | Focus Area | **Prompt to Type** | **Expected Result** |
| :--- | :--- | :--- | :--- |
| **VP Sales** | Revenue | `Check the status of Sales Order SO-5001` | "Shipped", $15,000 |
| **VP Sales** | Efficiency | `Create a new sales order for TechCorp for 50 Laptops` | Instant Creation |
| **VP Sales** | Risk | `Check credit limit for TechCorp` | Credit Limit & Rating |
| **VP Sales** | Planning | `Check demand forecast for product IBP-4001` | **1500 units**, 95% Accuracy |

---

## 🛠️ Setup & Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Regantih/Enterprise-SAP-AI.git
    cd Enterprise-SAP-AI
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Platform**:
    ```bash
    # Starts the Backend Server & Web UI
    python web_ui/server.py
    ```

4.  **Access the Dashboard**:
    *   Open `http://localhost:8000` in your browser.

---

## 🤝 Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

**Powered by Antigravity** 🌌
