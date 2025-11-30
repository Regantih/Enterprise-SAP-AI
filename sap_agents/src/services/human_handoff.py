import random

class ConfidenceEngine:
    """
    Advanced Confidence Calculation & Human Handoff Logic.
    Generates a 'Probability of Accuracy' for human audit.
    """
    def __init__(self):
        self.base_reliability = {
            "SalesOrderAssistant": 0.95,
            "ProcurementNegotiationAssistant": 0.85, # Complex domain
            "AnalyticsAgent": 0.90,
            "HREmployeeAssistant": 0.98,
            "FinanceReconciliationAgent": 0.92
        }

    def evaluate(self, response: str, agent_name: str) -> dict:
        """
        Calculates confidence score, certainty level, and reasoning.
        """
        base_score = self.base_reliability.get(agent_name, 0.80)
        score = base_score
        reasoning = [f"Base Reliability for {agent_name}: {base_score}"]
        
        # Heuristic: Penalize for uncertainty keywords
        if any(w in response.lower() for w in ["maybe", "unclear", "simulated", "estimate"]):
            penalty = 0.15
            score -= penalty
            reasoning.append(f"Penalty: Uncertainty detected (-{penalty})")
            
        # Heuristic: Penalize for short responses
        if len(response.split()) < 10:
            penalty = 0.20
            score -= penalty
            reasoning.append(f"Penalty: Short response (-{penalty})")
            
        # Heuristic: Boost for specific data patterns (Numbers, Currency)
        if any(c.isdigit() for c in response) or "$" in response or "€" in response:
            boost = 0.05
            score += boost
            reasoning.append(f"Boost: Data pattern detected (+{boost})")

        # Cap score between 0.1 and 1.0
        score = max(0.1, min(1.0, score))
        
        # Determine Certainty Level
        if score >= 0.9:
            certainty = "High"
        elif score >= 0.7:
            certainty = "Medium"
        else:
            certainty = "Low"
        
        probability = f"{int(score * 100)}%"
        
        audit_trail = {
            "confidence_score": round(score, 2),
            "probability_of_accuracy": probability,
            "certainty_level": certainty,
            "reasoning": reasoning,
            "requires_human_review": score < 0.75,
            "audit_reason": "High Confidence" if score >= 0.75 else "Low Confidence: Uncertainty detected or complex domain."
        }
        
        print(f"   [Confidence Engine] 🧠 Score: {score:.2f} ({probability}) - {certainty}")
        return audit_trail

    def append_audit_info(self, response: str, audit: dict) -> str:
        """
        Appends the detailed audit trail to the response.
        """
        icon = "✅" if not audit["requires_human_review"] else "⚠️"
        
        # Generate a unique ID for this feedback block
        import uuid
        msg_id = str(uuid.uuid4())
        
        footer = f"""
<hr class="my-3 border-gray-600">
<div class="text-xs text-gray-400" id="feedback-{msg_id}">
    <div class="flex justify-between items-center">
        <div>
            <span class="font-bold text-gray-300">Confidence:</span> {audit['probability_of_accuracy']} {icon}
            <span class="mx-2">|</span>
            <span class="font-bold text-gray-300">Status:</span> {'Auto-Approved' if not audit['requires_human_review'] else 'Flagged'}
        </div>
        <div class="flex space-x-2">
            <button onclick="sendFeedback(1, '{msg_id}')" class="hover:text-green-400 transition" title="Helpful">👍</button>
            <button onclick="sendFeedback(-1, '{msg_id}')" class="hover:text-red-400 transition" title="Not Helpful">👎</button>
        </div>
    </div>
</div>
"""
        return response + footer

# Global Instance
confidence_engine = ConfidenceEngine()
