from langchain.tools import Tool
import os

from src.tools.sap_document_ai import SAPDocumentClient

def extract_document_data(file_path: str) -> str:
    """
    Extracts data from a document.
    1. Tries Real SAP Document Information Extraction (if configured).
    2. Falls back to LLM-based extraction (Mock/Simulation).
    """
    print(f"   [Tool] 📄 Processing document: {file_path}...")
    
    # Handle relative paths
    if not os.path.isabs(file_path):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        potential_path = os.path.join(base_path, file_path)
        if os.path.exists(potential_path):
            file_path = potential_path
        elif os.path.exists(file_path):
            pass 
        else:
             return f"Error: File not found at {file_path}"

    # 1. Try Real SAP Service
    try:
        sap_client = SAPDocumentClient()
        if sap_client.service_key:
            print("   [Tool] 🚀 Using Real SAP Document AI Service...")
            result = sap_client.process_document(file_path)
            if result:
                return result
    except Exception as e:
        print(f"   [Tool] ⚠️ SAP Service failed: {e}. Falling back to LLM.")

    # 2. Fallback to LLM Extraction
    print("   [Tool] 🧠 Using LLM-based Extraction (Fallback)...")
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return f"--- DOCUMENT CONTENT START ---\n{content}\n--- DOCUMENT CONTENT END ---\n\n(Instruction: Extract key fields like Vendor, Items, and Total Amount from the above content.)"
    except Exception as e:
        return f"Error reading document: {str(e)}"

def get_document_tools():
    return [
        Tool(
            name="ExtractDocumentData",
            func=extract_document_data,
            description="Extract data from a document (Invoice, PO, etc.). Input: File path (e.g., 'invoice.txt')."
        )
    ]
