import json
import time
import os

AUDIT_LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'audit_log.json')

class AuditService:
    def __init__(self):
        self.log_path = AUDIT_LOG_PATH
        self._ensure_log_file()

    def _ensure_log_file(self):
        if not os.path.exists(os.path.dirname(self.log_path)):
            os.makedirs(os.path.dirname(self.log_path))
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                json.dump([], f)

    def log_event(self, transaction_id, step, detail, status="INFO"):
        """
        Logs a step in the causal chain: Transaction -> Decision -> Action -> Outcome.
        """
        event = {
            "timestamp": time.time(),
            "transaction_id": transaction_id,
            "step": step,  # e.g., "DECISION", "ACTION", "OUTCOME"
            "detail": detail,
            "status": status
        }
        self._append_to_log(event)
        print(f"[Audit] 📝 {step}: {detail} ({status})")

    def log_feedback(self, transaction_id, rating, comment):
        """
        Logs user feedback to drive evolution.
        """
        event = {
            "timestamp": time.time(),
            "transaction_id": transaction_id,
            "step": "FEEDBACK",
            "detail": f"Rating: {rating}/5, Comment: {comment}",
            "status": "REVIEW_REQUIRED" if rating < 3 else "APPROVED"
        }
        self._append_to_log(event)
        print(f"[Audit] 🗣️ Feedback: {comment} (Rating: {rating})")

    def _append_to_log(self, event):
        try:
            with open(self.log_path, 'r+') as f:
                data = json.load(f)
                data.append(event)
                f.seek(0)
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[Audit] ❌ Error writing log: {e}")

    def get_audit_trail(self, transaction_id):
        with open(self.log_path, 'r') as f:
            data = json.load(f)
        return [e for e in data if e['transaction_id'] == transaction_id]

def create_audit_service():
    return AuditService()
