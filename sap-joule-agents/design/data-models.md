# SAP Joule Agent System - Data Model Specification

## 1. Core Data Entities

This document defines the data structures used by the agents to interact with SAP systems and internal logic.

### 1.1 Procurement Domain

#### Entity: Supplier
Maps to S/4HANA Business Partner (Supplier role).

```json
{
  "supplierId": "String (10)",
  "name": "String",
  "status": "Enum [Active, Blocked, Inactive]",
  "rating": {
    "quality": "Float (0-100)",
    "delivery": "Float (0-100)",
    "overall": "Float (0-100)"
  },
  "riskProfile": "Enum [Low, Medium, High]",
  "paymentTerms": "String"
}
```

#### Entity: PurchaseOrder
Maps to S/4HANA Purchase Order.

```json
{
  "poNumber": "String (10)",
  "supplierId": "String (10)",
  "items": [
    {
      "lineId": "Integer",
      "material": "String",
      "quantity": "Decimal",
      "price": "Decimal",
      "currency": "String (3)"
    }
  ],
  "totalValue": "Decimal",
  "status": "Enum [Created, Approved, Sent, Received]",
  "deliveryDate": "Date"
}
```

### 1.2 Finance Domain

#### Entity: Invoice
Maps to S/4HANA Supplier Invoice.

```json
{
  "invoiceId": "String",
  "supplierId": "String",
  "poReference": "String",
  "amount": "Decimal",
  "dueDate": "Date",
  "isDisputed": "Boolean",
  "disputeReason": "String (Optional)"
}
```

### 1.3 HR Domain

#### Entity: Employee
Maps to SuccessFactors User/EmpJob.

```json
{
  "userId": "String",
  "firstName": "String",
  "lastName": "String",
  "email": "String",
  "department": "String",
  "managerId": "String",
  "onboardingStatus": "Enum [NotStarted, InProgress, Completed]"
}
```

## 2. Knowledge Graph Schema

The SAP Knowledge Graph connects these entities semantically.

### 2.1 Relationships

- **Supplier** `HAS_CONTRACT` **Contract**
- **Contract** `GOVERNS` **PurchaseOrder**
- **PurchaseOrder** `HAS_INVOICE` **Invoice**
- **Employee** `MANAGES` **Supplier** (Account Manager relationship)

### 2.2 Semantic Types

- `@DataType: SupplierID` -> Automatically links to S/4HANA Supplier Master.
- `@DataType: Money` -> Handles currency conversion automatically.

## 3. Agent Context Model

The "Memory" of the agent during a conversation.

```json
{
  "sessionId": "UUID",
  "userContext": {
    "userId": "String",
    "roles": ["Procurement_Manager"],
    "locale": "en-US"
  },
  "conversationState": {
    "currentIntent": "Negotiate_Contract",
    "slotFilling": {
      "supplierId": "1000123",
      "contractId": "Pending"
    },
    "lastAction": "GetSupplierData"
  }
}
```
