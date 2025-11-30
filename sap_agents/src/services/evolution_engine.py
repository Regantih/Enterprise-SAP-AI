from src.services.audit_service import create_audit_service

class EvolutionEngine:
    def __init__(self):
        self.audit_service = create_audit_service()

    def analyze_feedback(self, transaction_id, rating, comment):
        """
        Analyzes feedback and triggers evolution if necessary.
        """
        if rating < 3:
            print(f"[Evolution] 🧬 Negative feedback detected for {transaction_id}. Initiating analysis...")
            
            # Simulate RLHF / Self-Correction Logic
            revision = self._generate_revision(comment)
            
            self.audit_service.log_event(
                transaction_id, 
                "EVOLUTION", 
                f"System updated behavior based on feedback: '{comment}'. New Rule: {revision}", 
                "APPLIED"
            )
            return f"System evolved: {revision}"
        
        return "No evolution required."

    def _generate_revision(self, comment):
        # In a real system, this would use an LLM to rewrite the prompt.
        # Here we simulate it with simple rules.
        if "too short" in comment.lower():
            return "Increase response verbosity."
        if "wrong agent" in comment.lower():
            return "Adjust routing weights for this query type."
        if "outdated" in comment.lower():
            return "Trigger knowledge base refresh."
        return "General quality improvement applied."

def create_evolution_engine():
    return EvolutionEngine()
