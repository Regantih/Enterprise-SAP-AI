import random

class ContextEnricher:
    """
    Enriches raw user prompts with contextual metadata (Role, Location, History).
    """
    def __init__(self):
        self.mock_users = {
            "admin": {"role": "IT Admin", "location": "Headquarters", "clearance": "L3"},
            "cfo": {"role": "CFO", "location": "New York", "clearance": "L2"},
            "manager": {"role": "Sales Manager", "location": "Berlin", "clearance": "L1"}
        }

    def enrich(self, prompt: str, user_id: str = "admin") -> dict:
        """
        Decorates the prompt with user context.
        """
        user_context = self.mock_users.get(user_id, self.mock_users["manager"])
        
        print(f"   [Context Enricher] 🧠 Enriching prompt for {user_context['role']} in {user_context['location']}...")
        
        enriched_data = {
            "original_prompt": prompt,
            "user_role": user_context["role"],
            "user_location": user_context["location"],
            "security_clearance": user_context["clearance"],
            "enriched_prompt": f"Acting as {user_context['role']} based in {user_context['location']}: {prompt}"
        }
        
        return enriched_data

# Global Instance
context_enricher = ContextEnricher()
