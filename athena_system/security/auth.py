"""
Authentication Module for Athena Core
Provides basic auth, API key, and middleware for protected endpoints.
"""
import os
import hashlib
import hmac
import base64
from typing import Optional, Tuple, Dict
from functools import wraps

# Configuration
AUTH_ENABLED = os.environ.get("ATHENA_AUTH_ENABLED", "false").lower() == "true"
API_KEY = os.environ.get("ATHENA_API_KEY", "")
ADMIN_PASSWORD_HASH = os.environ.get("ATHENA_ADMIN_HASH", "")

# Default users (for demo - in production, use database)
DEFAULT_USERS = {
    "admin": "athena2024",  # Default admin password
    "demo": "demo123",       # Demo user
}


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return hmac.compare_digest(hash_password(password), password_hash)


def check_basic_auth(auth_header: str) -> Tuple[bool, Optional[str]]:
    """
    Check Basic Authentication header.
    Returns (is_valid, username).
    """
    if not auth_header or not auth_header.startswith("Basic "):
        return False, None
    
    try:
        encoded = auth_header.split(" ", 1)[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        
        # Check against default users
        if username in DEFAULT_USERS:
            if DEFAULT_USERS[username] == password:
                return True, username
        
        # Check against admin hash if set
        if ADMIN_PASSWORD_HASH and username == "admin":
            if verify_password(password, ADMIN_PASSWORD_HASH):
                return True, username
        
        return False, None
    except Exception:
        return False, None


def check_api_key(api_key_header: str) -> bool:
    """Check API key authentication."""
    if not API_KEY:
        return False  # API key auth not configured
    
    return hmac.compare_digest(api_key_header or "", API_KEY)


def get_auth_status(headers: Dict) -> Dict:
    """
    Check authentication status from request headers.
    Supports: Basic Auth, API Key (X-API-Key header).
    """
    # Check if auth is disabled
    if not AUTH_ENABLED:
        return {
            "authenticated": True,
            "method": "disabled",
            "user": "anonymous"
        }
    
    # Check API Key
    api_key = headers.get("X-API-Key", "")
    if api_key and check_api_key(api_key):
        return {
            "authenticated": True,
            "method": "api_key",
            "user": "api_user"
        }
    
    # Check Basic Auth
    auth_header = headers.get("Authorization", "")
    is_valid, username = check_basic_auth(auth_header)
    if is_valid:
        return {
            "authenticated": True,
            "method": "basic",
            "user": username
        }
    
    # Not authenticated
    return {
        "authenticated": False,
        "method": None,
        "user": None
    }


def require_auth(handler_method):
    """
    Decorator for protected endpoints.
    Returns 401 if not authenticated.
    """
    @wraps(handler_method)
    def wrapper(self, *args, **kwargs):
        if not AUTH_ENABLED:
            return handler_method(self, *args, **kwargs)
        
        headers = {k: v for k, v in self.headers.items()}
        auth_status = get_auth_status(headers)
        
        if not auth_status["authenticated"]:
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Athena Core"')
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Authentication required"}')
            return
        
        # Store auth info for handler to use
        self.auth_user = auth_status["user"]
        self.auth_method = auth_status["method"]
        
        return handler_method(self, *args, **kwargs)
    
    return wrapper


def generate_api_key() -> str:
    """Generate a new API key."""
    import secrets
    return f"athena_{secrets.token_hex(24)}"


# Quick test
if __name__ == "__main__":
    print("🔐 Authentication Module Test\n")
    
    # Test password hashing
    password = "test123"
    hashed = hash_password(password)
    print(f"Password hash: {hashed[:20]}...")
    print(f"Verify correct: {verify_password(password, hashed)}")
    print(f"Verify wrong: {verify_password('wrong', hashed)}")
    
    # Test Basic Auth
    import base64
    creds = base64.b64encode(b"admin:athena2024").decode()
    valid, user = check_basic_auth(f"Basic {creds}")
    print(f"\nBasic Auth (admin): valid={valid}, user={user}")
    
    # Test API Key
    print(f"\nGenerated API Key: {generate_api_key()}")
    
    # Test auth status
    print(f"\nAuth enabled: {AUTH_ENABLED}")
    print(f"API Key configured: {bool(API_KEY)}")
