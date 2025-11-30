import time
import uuid

class AuthService:
    """
    Simulates SAP Identity Authentication Service (IAS) / XSUAA.
    Handles token generation and validation.
    """
    def __init__(self):
        self.service_name = "SAP Identity Authentication Service"
        self.status = "Active"
        self.tokens = {}

    def generate_token(self, user_id: str, scopes: list) -> str:
        """Generates a mock OAuth2 access token."""
        print(f"   [Auth Service] 🔐 Generating token for {user_id} with scopes {scopes}...")
        token = f"ey-{uuid.uuid4()}"
        self.tokens[token] = {
            "user_id": user_id,
            "scopes": scopes,
            "expires_at": time.time() + 3600
        }
        return token

    def validate_token(self, token: str) -> bool:
        """Validates an access token."""
        if token in self.tokens:
            data = self.tokens[token]
            if data["expires_at"] > time.time():
                return True
        return False

    def get_status(self):
        return f"✅ {self.service_name} is {self.status}."
