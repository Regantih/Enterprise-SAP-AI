from src.services.auth_service import AuthService
from src.services.hana_vector_db import HanaVectorDB
from src.services.build_pa import BuildProcessAutomation

class ServiceManager:
    """
    Central registry for Enterprise Services.
    """
    def __init__(self):
        print("[Service Manager] 🔄 Initializing Enterprise Services...")
        self.auth = AuthService()
        self.hana_db = HanaVectorDB()
        self.build_pa = BuildProcessAutomation()
        print("[Service Manager] ✅ All services initialized.")

    def get_auth_service(self):
        return self.auth

    def get_hana_db(self):
        return self.hana_db

    def get_build_pa(self):
        return self.build_pa

    def health_check(self):
        """Returns the status of all subscribed services."""
        return {
            "Auth": self.auth.get_status(),
            "HANA_DB": self.hana_db.get_status(),
            "Build_PA": self.build_pa.get_status()
        }

# Global Instance
service_manager = ServiceManager()
