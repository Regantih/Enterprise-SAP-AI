# SAP Joule Agent System - Skills & Tools Specification

## 1. Procurement Agent Skills

### 1.1 Deterministic Skills (API-Based)

| Skill Name | Endpoint / Function | Inputs | Outputs |
|------------|---------------------|--------|---------|
| `GetSupplierData` | `GET /A_Supplier` | `supplierId` | `name`, `status`, `rating` |
| `GetPurchaseOrders` | `GET /A_PurchaseOrder` | `supplierId`, `dateRange` | `List[PO]` |
| `CreateRequisition` | `POST /A_PurchaseReq` | `material`, `qty`, `plant` | `reqId` |

### 1.2 AI Capabilities (LLM-Based)

| Skill Name | Description | Model | Prompt Strategy |
|------------|-------------|-------|-----------------|
| `AnalyzeSpend` | Summarizes spend patterns and identifies anomalies. | GPT-4 | Chain-of-Thought |
| `DraftNegotiation` | Generates email drafts for supplier negotiation. | GPT-4 | Role-Playing |
| `ExtractContractTerms` | Extracts key dates and clauses from PDF contracts. | GPT-4-Vision | Zero-Shot |

## 2. Finance Agent Skills

### 2.1 Deterministic Skills

| Skill Name | Endpoint / Function | Inputs | Outputs |
|------------|---------------------|--------|---------|
| `CheckInvoiceStatus` | `GET /A_SupplierInvoice` | `invoiceId` | `status`, `paymentDate` |
| `GetBudgetStatus` | `GET /A_BudgetPeriod` | `costCenter` | `allocated`, `consumed` |

### 2.2 AI Capabilities

| Skill Name | Description | Model | Prompt Strategy |
|------------|-------------|-------|-----------------|
| `ExplainVariance` | Explains why actuals differ from budget. | GPT-4 | Data-to-Text |
| `ClassifyExpense` | Suggests GL account for unstructured expense items. | GPT-3.5 | Few-Shot |

## 3. Tool Integrations

### 3.1 SAP S/4HANA Cloud
- **Protocol**: OData V2/V4
- **Auth**: OAuth 2.0 (Principal Propagation)
- **Throttling**: 100 req/min per user

### 3.2 SAP Business Data Cloud
- **Protocol**: REST API
- **Use Case**: Historical data analysis, market benchmarks.

### 3.3 Microsoft 365 (via Graph API)
- **Use Case**: Sending emails, scheduling meetings.
- **Skill**: `SendEmail`, `FindMeetingSlot`.
