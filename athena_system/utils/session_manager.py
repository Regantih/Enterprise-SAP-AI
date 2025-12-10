"""
Session Manager for Multi-User Support
Provides session-based conversation isolation for concurrent users.
"""
import uuid
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta

# Session timeout in seconds (30 minutes)
SESSION_TIMEOUT = 1800


class Session:
    """Represents a user session with conversation history."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.history: List[Dict] = []
        self.metadata: Dict = {}
    
    def add_message(self, role: str, content: str):
        """Add a message to session history."""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.last_activity = datetime.now()
    
    def get_context(self, last_n: int = 5) -> str:
        """Get recent conversation context."""
        recent = self.history[-last_n:] if len(self.history) > last_n else self.history
        return "\n".join([f"{m['role']}: {m['content']}" for m in recent])
    
    def get_last_user_message(self) -> Optional[str]:
        """Get the previous user message (for context enrichment)."""
        user_messages = [m for m in self.history if m['role'] == 'User']
        if len(user_messages) >= 2:
            return user_messages[-2]['content']  # Second to last
        return None
    
    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.now() - self.last_activity > timedelta(seconds=SESSION_TIMEOUT)
    
    def to_dict(self) -> Dict:
        """Convert session to dictionary."""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "message_count": len(self.history),
            "expired": self.is_expired()
        }


class SessionManager:
    """Manages multiple user sessions."""
    
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self._cleanup_counter = 0
    
    def create_session(self) -> str:
        """Create a new session and return its ID."""
        session_id = str(uuid.uuid4())[:8]  # Short ID for convenience
        self.sessions[session_id] = Session(session_id)
        self._maybe_cleanup()
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get an existing session by ID."""
        session = self.sessions.get(session_id)
        if session and not session.is_expired():
            return session
        return None
    
    def get_or_create_session(self, session_id: Optional[str]) -> Session:
        """Get existing session or create new one."""
        if session_id:
            session = self.get_session(session_id)
            if session:
                return session
        
        # Create new session
        new_id = self.create_session()
        return self.sessions[new_id]
    
    def delete_session(self, session_id: str):
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def _maybe_cleanup(self):
        """Periodically clean up expired sessions."""
        self._cleanup_counter += 1
        if self._cleanup_counter >= 10:  # Every 10 session creations
            self._cleanup_counter = 0
            expired = [sid for sid, s in self.sessions.items() if s.is_expired()]
            for sid in expired:
                del self.sessions[sid]
    
    def get_stats(self) -> Dict:
        """Get session statistics."""
        active = [s for s in self.sessions.values() if not s.is_expired()]
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": len(active),
            "expired_sessions": len(self.sessions) - len(active)
        }
    
    def list_sessions(self) -> List[Dict]:
        """List all sessions."""
        return [s.to_dict() for s in self.sessions.values()]


# Global session manager instance
session_manager = SessionManager()


# Cookie helper functions
def get_session_from_cookie(cookie_header: str) -> Optional[str]:
    """Extract session ID from cookie header."""
    if not cookie_header:
        return None
    
    for cookie in cookie_header.split(';'):
        cookie = cookie.strip()
        if cookie.startswith('athena_session='):
            return cookie.split('=', 1)[1]
    return None


def create_session_cookie(session_id: str) -> str:
    """Create Set-Cookie header value."""
    max_age = SESSION_TIMEOUT
    return f"athena_session={session_id}; Path=/; Max-Age={max_age}; SameSite=Lax"


# Quick test
if __name__ == "__main__":
    print("🧪 Session Manager Test\n")
    
    # Create sessions
    s1 = session_manager.get_or_create_session(None)
    s1.add_message("User", "Find leads for FinTech")
    s1.add_message("Athena", "Found 3 leads...")
    s1.add_message("User", "Draft email to them")
    
    s2 = session_manager.get_or_create_session(None)
    s2.add_message("User", "Create risk profile for Project Alpha")
    
    print(f"Session 1 ID: {s1.session_id}")
    print(f"Session 1 Context:\n{s1.get_context()}\n")
    print(f"Session 1 Last User Msg: {s1.get_last_user_message()}\n")
    
    print(f"Session 2 ID: {s2.session_id}")
    print(f"Session 2 Context:\n{s2.get_context()}\n")
    
    print(f"Stats: {session_manager.get_stats()}")
