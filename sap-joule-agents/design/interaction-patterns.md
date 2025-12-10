# SAP Joule Agent System - Interaction Patterns

## 1. Conversation Flows

### 1.1 Intent Recognition & Routing

**Pattern:** `User Request -> Orchestrator -> Specific Agent`

1.  **User**: "I need to negotiate a new contract with Acme Corp."
2.  **Joule Orchestrator**:
    *   Analyzes intent: `Negotiation`
    *   Identifies entity: `Acme Corp` (Supplier)
    *   Routes to: `Procurement Agent`
3.  **Procurement Agent**: "I can help with that. I've found Acme Corp (ID: 1000123). Shall I pull their performance data first?"

### 1.2 Slot Filling (Information Gathering)

**Pattern:** `Agent -> User (Clarification) -> Agent`

1.  **User**: "Check the invoice status."
2.  **Finance Agent**: "Which invoice are you referring to? You can give me the Invoice ID or the Supplier Name."
3.  **User**: "The one from TechSolutions."
4.  **Finance Agent**: "I found 3 recent invoices for TechSolutions. Are you looking for the one from yesterday for $5,000?"

### 1.3 Human-in-the-Loop (Escalation)

**Pattern:** `Agent -> Constraint Check -> Human Approval`

1.  **Procurement Agent**: "I've drafted the negotiation email. It proposes a 5% price reduction."
2.  **Constraint Check**: Contract value > $1M requires VP approval.
3.  **Agent**: "Since this contract is valued at $1.2M, I need approval from the VP of Procurement before sending. I've sent an approval request to Sarah Jenkins."

## 2. Multi-Agent Collaboration

### 2.1 Handoff Pattern

**Scenario**: Procurement negotiation leads to budget question.

1.  **Procurement Agent**: "The supplier agrees to the terms, but the total cost is $55,000."
2.  **User**: "Do we have budget for this?"
3.  **Procurement Agent**: "Let me check with the Finance Agent."
    *   *Internal Call*: `Procurement Agent -> Finance Agent (CheckBudget, CostCenter: IT, Amount: 55000)`
4.  **Finance Agent**: *Returns* `{"available": true, "remaining": 120000}`
5.  **Procurement Agent**: "Yes, the IT cost center has sufficient budget."

## 3. Proactive Notifications

**Pattern:** `System Event -> Agent -> User Notification`

1.  **Event**: S/4HANA triggers event `PurchaseOrder.Created`.
2.  **Joule**: Analyzes subscription. User `John` follows this supplier.
3.  **Joule -> User**: "Heads up: A new PO #450001 for Acme Corp was just created by Jane Doe."
