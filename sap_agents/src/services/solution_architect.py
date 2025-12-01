from src.services.capability_index import capability_index

class SolutionArchitect:
    """
    Evaluates requests to determine if they can be served by OOTB agents
    or require a Custom Build.
    """
    def __init__(self):
        self.custom_builds = {
            "custom_report": "Custom Financial Report Generator v1.0",
            "legacy_connector": "Mainframe Data Connector v2.1"
        }

    def evaluate(self, enriched_prompt: str) -> dict:
        """
        Decides the execution strategy: OOTB, Custom Asset, or New Build.
        """
        print(f"   [Solution Architect] 🏗️ Evaluating strategy for: '{enriched_prompt}'...")
        
        # 0. Check for Complex Scenarios (Force Fallback/Advanced Planning)
        if any(x in enriched_prompt.lower() for x in ["impact", "delayed", "delay", "quality", "late"]):
            print(f"   [Solution Architect] ⚠️ Complex Scenario Detected. Deferring to Orchestrator.")
            return {
                "strategy": "COMPLEX_SCENARIO", # Will fall through to else/fallback in Orchestrator
                "source": "Advanced Logic",
                "details": "Multi-step analysis required."
            }

        # 1. Check OOTB Capabilities (via Index)
        capability = capability_index.find_capability(enriched_prompt)
        if capability:
            return {
                "strategy": "OOTB",
                "source": "Standard Agent",
                "details": capability
            }

        # 2. Check Custom Build Registry
        for key, name in self.custom_builds.items():
            if key in enriched_prompt.lower():
                return {
                    "strategy": "CUSTOM_ASSET",
                    "source": "Custom Build Registry",
                    "details": {"name": name, "id": key}
                }

        # 3. Flag for New Build
        if "build" in enriched_prompt.lower() or "create new" in enriched_prompt.lower():
             return {
                "strategy": "NEW_BUILD",
                "source": "Development Queue",
                "details": "Request requires new custom development."
            }

        # Default fallback
        return {
            "strategy": "UNKNOWN",
            "source": "Manual Review",
            "details": "No matching capability found."
        }

# Global Instance
solution_architect = SolutionArchitect()
