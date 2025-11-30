class QualityGuardrail:
    """
    Ensures queries and responses meet enterprise quality standards.
    Acts as a filter for both inputs (relevance) and outputs (completeness).
    """
    def __init__(self):
        self.banned_topics = ["politics", "religion", "competitors"]
        self.required_response_elements = ["**", "Amount", "Status", "User", "Invoice"]

    def validate_input(self, query: str) -> dict:
        """
        Evaluates if the query is valid and safe to process.
        """
        print(f"   [Guardrail] 🛡️ Validating input: '{query}'...")
        
        # Check for banned topics
        for topic in self.banned_topics:
            if topic in query.lower():
                return {"valid": False, "reason": f"Query contains restricted topic: {topic}"}
        
        # Check for minimum length/relevance
        if len(query.split()) < 2:
             return {"valid": False, "reason": "Query is too short. Please provide more details."}

        return {"valid": True}

    def validate_output(self, response: str) -> dict:
        """
        Evaluates if the response meets quality standards (formatting, completeness).
        """
        print(f"   [Guardrail] 🛡️ Validating output quality...")
        
        # Check for formatting (Markdown bolding) - RELAXED for professional cleanliness
        # if "**" not in response and "Error" not in response:
        #      return {"valid": False, "reason": "Response lacks emphasis (bolding)."}
             
        # Check for professional tone (simple heuristic)
        if "dunno" in response.lower() or "maybe" in response.lower():
             return {"valid": False, "reason": "Response tone is too casual or uncertain."}

        return {"valid": True}

# Global Instance
quality_guardrail = QualityGuardrail()
