import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.auth import get_sap_session

def validate_connection():
    load_dotenv()
    
    print("🔍 Validating SAP Connection...")
    
    url = os.getenv("SAP_ODATA_URL")
    if not url:
        print("❌ Error: SAP_ODATA_URL not found in .env")
        return

    print(f"   Target: {url}")
    
    try:
        session, base_url = get_sap_session()
        # Try to fetch metadata or the service document
        response = session.get(base_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Connection Successful!")
            print(f"   Status: {response.status_code}")
            print("   Response snippet:", response.text[:100])
        elif response.status_code == 401:
            print("❌ Authentication Failed (401). Check Username/Password or API Key.")
        elif response.status_code == 403:
            print("❌ Access Denied (403). Check permissions.")
        else:
            print(f"⚠️  Connection returned status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")

if __name__ == "__main__":
    validate_connection()
