from langchain.tools import Tool
import time
import random

# Mock Database with SAP-like Schema
INVOICES = {
    "INV-9001": {
        "SupplierInvoice": "9001",
        "InvoicingParty": "Office Supplies Co.",
        "TotalGrossAmount": 5000,
        "DocumentCurrency": "USD",
        "InvoiceStatus": "Pending Approval",
        "PostingDate": "2023-12-15"
    },
    "INV-9002": {
        "SupplierInvoice": "9002",
        "InvoicingParty": "Tech Equipment Ltd.",
        "TotalGrossAmount": 25000,
        "DocumentCurrency": "USD",
        "InvoiceStatus": "Paid",
        "PostingDate": "2023-11-30"
    },
    "INV-9003": {
        "SupplierInvoice": "9003",
        "InvoicingParty": "Cleaning Services Inc.",
        "TotalGrossAmount": 2500,
        "DocumentCurrency": "USD",
        "InvoiceStatus": "Overdue",
        "PostingDate": "2023-11-01"
    }
}

GL_ACCOUNTS = {
    "GL-1000": {"GLAccount": "1000", "GLAccountName": "Office Supplies", "BalanceTransactionCurrency": 12500, "Currency": "USD"},
    "GL-2000": {"GLAccount": "2000", "GLAccountName": "IT Equipment", "BalanceTransactionCurrency": 45000, "Currency": "USD"},
    "GL-3000": {"GLAccount": "3000", "GLAccountName": "Travel Expenses", "BalanceTransactionCurrency": 8500, "Currency": "USD"}
}

def check_invoice_status(invoice_id: str) -> str:
    """Checks the status of a specific Supplier Invoice."""
    print(f"   [Finance Tool] 🔍 Checking invoice {invoice_id}...")
    time.sleep(0.5)
    inv = INVOICES.get(invoice_id)
    if inv:
        return f"Invoice **{inv['SupplierInvoice']}** from {inv['InvoicingParty']} is **{inv['InvoiceStatus']}**. Amount: {inv['TotalGrossAmount']} {inv['DocumentCurrency']}."
    return f"Invoice {invoice_id} not found."

def get_gl_balance(account_id: str) -> str:
    """Gets the balance of a General Ledger (GL) account."""
    print(f"   [Finance Tool] 📊 Checking GL Account {account_id}...")
    time.sleep(0.5)
    acc = GL_ACCOUNTS.get(account_id)
    if acc:
        return f"GL Account **{acc['GLAccount']}** ({acc['GLAccountName']}): Balance is **{acc['BalanceTransactionCurrency']} {acc['Currency']}**."
    return f"GL Account {account_id} not found."

def approve_expense(invoice_id: str) -> str:
    """Simulates approving a Supplier Invoice for payment."""
    print(f"   [Finance Tool] ✅ Approving invoice {invoice_id}...")
    time.sleep(1.0)
    
    inv = INVOICES.get(invoice_id)
    if not inv:
        return f"Error: Invoice {invoice_id} not found."
    
    if inv['InvoiceStatus'] == "Paid":
        return f"Invoice {invoice_id} is already paid."
        
    inv['InvoiceStatus'] = "Approved"
    return f"✅ Invoice **{inv['SupplierInvoice']}** for {inv['TotalGrossAmount']} {inv['DocumentCurrency']} has been successfully **APPROVED** for payment."

def get_finance_tools():
    return [
        Tool(
            name="CheckInvoiceStatus",
            func=check_invoice_status,
            description="Check the status of a specific Invoice. Input: Invoice ID (e.g., 'INV-9001')."
        ),
        Tool(
            name="GetGLAccountBalance",
            func=get_gl_balance,
            description="Get the balance of a General Ledger (GL) Account. Input: Account ID (e.g., 'GL-1000')."
        ),
        Tool(
            name="ApproveExpense",
            func=approve_expense,
            description="Approve an expense invoice for payment. Input: Invoice ID (e.g., 'INV-9001')."
        )
    ]
