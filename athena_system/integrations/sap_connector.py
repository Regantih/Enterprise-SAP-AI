"""
SAP OData Connector with Mock Fallback
Attempts SAP API Business Hub sandbox first, falls back to local mock data.
"""
import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime

# SAP API Business Hub Configuration
SAP_API_HUB_URL = os.environ.get("SAP_API_HUB_URL", "https://sandbox.api.sap.com")
SAP_API_KEY = os.environ.get("SAP_API_KEY", "")  # Get from api.sap.com

# Common SAP API endpoints (Sandbox versions)
SAP_ENDPOINTS = {
    "business_partner": "/s4hanacloud/sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner",
    "sales_order": "/s4hanacloud/sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder",
    "purchase_order": "/s4hanacloud/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder",
    "product": "/s4hanacloud/sap/opu/odata/sap/API_PRODUCT_SRV/A_Product",
}

# Enhanced mock data for realistic simulation
MOCK_BUSINESS_PARTNERS = [
    {"BusinessPartner": "10000001", "BusinessPartnerFullName": "Acme Corporation", "Industry": "Manufacturing", "Country": "US", "CreditLimit": 500000},
    {"BusinessPartner": "10000002", "BusinessPartnerFullName": "FinTech Global Ltd", "Industry": "Financial Services", "Country": "UK", "CreditLimit": 750000},
    {"BusinessPartner": "10000003", "BusinessPartnerFullName": "HealthPlus Systems", "Industry": "Healthcare", "Country": "DE", "CreditLimit": 300000},
    {"BusinessPartner": "10000004", "BusinessPartnerFullName": "GreenEnergy Corp", "Industry": "Energy", "Country": "NL", "CreditLimit": 1000000},
    {"BusinessPartner": "10000005", "BusinessPartnerFullName": "TechVentures Inc", "Industry": "Technology", "Country": "US", "CreditLimit": 450000},
]

MOCK_SALES_ORDERS = [
    {"SalesOrder": "5000001", "SalesOrderType": "OR", "SoldToParty": "10000001", "NetAmount": 125000.00, "TransactionCurrency": "USD", "CreationDate": "2024-12-01", "OverallSDProcessStatus": "A"},
    {"SalesOrder": "5000002", "SalesOrderType": "OR", "SoldToParty": "10000002", "NetAmount": 89500.00, "TransactionCurrency": "GBP", "CreationDate": "2024-12-05", "OverallSDProcessStatus": "B"},
    {"SalesOrder": "5000003", "SalesOrderType": "ZOR", "SoldToParty": "10000003", "NetAmount": 45000.00, "TransactionCurrency": "EUR", "CreationDate": "2024-12-08", "OverallSDProcessStatus": "C"},
    {"SalesOrder": "5000004", "SalesOrderType": "OR", "SoldToParty": "10000004", "NetAmount": 320000.00, "TransactionCurrency": "EUR", "CreationDate": "2024-12-10", "OverallSDProcessStatus": "A"},
]

MOCK_PURCHASE_ORDERS = [
    {"PurchaseOrder": "4500001", "Supplier": "20000001", "PurchasingOrganization": "1000", "NetAmount": 75000.00, "Currency": "USD", "CreationDate": "2024-11-20", "Status": "Open"},
    {"PurchaseOrder": "4500002", "Supplier": "20000002", "PurchasingOrganization": "1000", "NetAmount": 32500.00, "Currency": "EUR", "CreationDate": "2024-11-25", "Status": "Approved"},
    {"PurchaseOrder": "4500003", "Supplier": "20000003", "PurchasingOrganization": "2000", "NetAmount": 158000.00, "Currency": "USD", "CreationDate": "2024-12-01", "Status": "Received"},
]


class SAPConnector:
    """Hybrid SAP OData connector with sandbox + mock fallback."""
    
    def __init__(self):
        self.api_key = SAP_API_KEY
        self.base_url = SAP_API_HUB_URL
        self._sandbox_available = None
    
    def _is_sandbox_available(self) -> bool:
        """Check if SAP API Business Hub sandbox is accessible."""
        if self._sandbox_available is not None:
            return self._sandbox_available
        
        if not self.api_key:
            print("⚠️ SAP_API_KEY not set - using mock data")
            self._sandbox_available = False
            return False
        
        try:
            response = requests.get(
                f"{self.base_url}/s4hanacloud/sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner?$top=1",
                headers={"APIKey": self.api_key},
                timeout=5
            )
            self._sandbox_available = response.status_code == 200
            if self._sandbox_available:
                print("✅ SAP API Business Hub sandbox connected")
            else:
                print(f"⚠️ SAP sandbox returned {response.status_code} - using mock")
        except Exception as e:
            print(f"⚠️ SAP sandbox unavailable: {e} - using mock")
            self._sandbox_available = False
        
        return self._sandbox_available
    
    def _call_sap_api(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make authenticated call to SAP API Business Hub."""
        if not self._is_sandbox_available():
            return None
        
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(
                url,
                headers={
                    "APIKey": self.api_key,
                    "Accept": "application/json"
                },
                params=params or {},
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"⚠️ SAP API call failed: {e}")
        
        return None
    
    # --- Business Partner APIs ---
    
    def get_business_partners(self, top: int = 10, filter_str: str = None) -> Dict:
        """Get business partners from SAP or mock."""
        # Try SAP first
        params = {"$top": top, "$format": "json"}
        if filter_str:
            params["$filter"] = filter_str
        
        result = self._call_sap_api(SAP_ENDPOINTS["business_partner"], params)
        
        if result:
            return {
                "source": "sap_sandbox",
                "data": result.get("d", {}).get("results", [])
            }
        
        # Fallback to mock
        return {
            "source": "mock",
            "data": MOCK_BUSINESS_PARTNERS[:top]
        }
    
    def get_business_partner_by_id(self, bp_id: str) -> Dict:
        """Get single business partner."""
        result = self._call_sap_api(f"{SAP_ENDPOINTS['business_partner']}('{bp_id}')")
        
        if result:
            return {"source": "sap_sandbox", "data": result.get("d", {})}
        
        # Mock fallback
        for bp in MOCK_BUSINESS_PARTNERS:
            if bp["BusinessPartner"] == bp_id:
                return {"source": "mock", "data": bp}
        
        return {"source": "mock", "data": None, "error": "Not found"}
    
    # --- Sales Order APIs ---
    
    def get_sales_orders(self, top: int = 10, status: str = None) -> Dict:
        """Get sales orders from SAP or mock."""
        params = {"$top": top, "$format": "json"}
        if status:
            params["$filter"] = f"OverallSDProcessStatus eq '{status}'"
        
        result = self._call_sap_api(SAP_ENDPOINTS["sales_order"], params)
        
        if result:
            return {
                "source": "sap_sandbox",
                "data": result.get("d", {}).get("results", [])
            }
        
        # Mock fallback
        data = MOCK_SALES_ORDERS
        if status:
            data = [so for so in data if so["OverallSDProcessStatus"] == status]
        
        return {
            "source": "mock",
            "data": data[:top]
        }
    
    # --- Purchase Order APIs ---
    
    def get_purchase_orders(self, top: int = 10, status: str = None) -> Dict:
        """Get purchase orders from SAP or mock."""
        params = {"$top": top, "$format": "json"}
        
        result = self._call_sap_api(SAP_ENDPOINTS["purchase_order"], params)
        
        if result:
            return {
                "source": "sap_sandbox",
                "data": result.get("d", {}).get("results", [])
            }
        
        # Mock fallback
        data = MOCK_PURCHASE_ORDERS
        if status:
            data = [po for po in data if po["Status"].lower() == status.lower()]
        
        return {
            "source": "mock",
            "data": data[:top]
        }
    
    # --- Analytics APIs ---
    
    def get_revenue_summary(self) -> Dict:
        """Get revenue summary from sales orders."""
        orders = self.get_sales_orders(top=100)
        
        total_revenue = sum(so.get("NetAmount", 0) for so in orders["data"])
        order_count = len(orders["data"])
        
        return {
            "source": orders["source"],
            "total_revenue": round(total_revenue, 2),
            "order_count": order_count,
            "average_order_value": round(total_revenue / max(order_count, 1), 2),
            "currency": "Mixed" if orders["source"] == "mock" else "USD"
        }
    
    def get_system_status(self) -> Dict:
        """Get overall system connection status."""
        return {
            "sap_sandbox_available": self._is_sandbox_available(),
            "api_key_configured": bool(self.api_key),
            "fallback_mode": not self._is_sandbox_available(),
            "timestamp": datetime.now().isoformat()
        }


# Singleton instance
sap = SAPConnector()


# Quick test
if __name__ == "__main__":
    print("🔌 SAP Connector Test\n")
    print(f"System Status: {json.dumps(sap.get_system_status(), indent=2)}\n")
    
    print("📊 Business Partners:")
    bps = sap.get_business_partners(top=3)
    print(f"Source: {bps['source']}")
    for bp in bps['data']:
        print(f"  - {bp.get('BusinessPartnerFullName', bp.get('BusinessPartner'))}")
    
    print("\n📦 Sales Orders:")
    sos = sap.get_sales_orders(top=3)
    print(f"Source: {sos['source']}")
    for so in sos['data']:
        print(f"  - Order {so['SalesOrder']}: {so['NetAmount']} {so.get('TransactionCurrency', '')}")
    
    print("\n💰 Revenue Summary:")
    rev = sap.get_revenue_summary()
    print(f"  Total: {rev['total_revenue']} ({rev['order_count']} orders)")
