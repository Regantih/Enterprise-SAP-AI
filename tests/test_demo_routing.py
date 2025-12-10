import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock the workflow runners to avoid actual execution
sys.modules['athena_system.workflows.knowledge_arbitrage'] = MagicMock()
sys.modules['athena_system.workflows.lead_gen_outreach'] = MagicMock()
sys.modules['athena_system.workflows.delivery_framework'] = MagicMock()
sys.modules['athena_system.workflows.business_review'] = MagicMock()

from athena_system.web_ui.server import AgentHandler

class TestDemoRouting(unittest.TestCase):
    def test_routing_logic(self):
        """
        Simulates the routing logic from server.py to verify keyword matching.
        """
        test_cases = [
            ("Research Agentic AI", "knowledge_arbitrage"),
            ("Draft a blog about Supply Chain", "knowledge_arbitrage"),
            ("Find leads for FinTech", "lead_gen_outreach"),
            ("Create risk profile for Project Alpha", "delivery_framework"), # The failing case
            ("Run business review", "business_review")
        ]

        print("\n🔍 Testing Routing Logic:")
        for prompt, expected_workflow in test_cases:
            prompt_lower = prompt.lower()
            detected_workflow = "unknown"

            # Replicating the logic from server.py exactly
            if "research" in prompt_lower or "blog" in prompt_lower or "topic" in prompt_lower:
                detected_workflow = "knowledge_arbitrage"
            elif "lead" in prompt_lower or "sales" in prompt_lower:
                detected_workflow = "lead_gen_outreach"
            elif "risk" in prompt_lower or "project" in prompt_lower or "profile" in prompt_lower:
                detected_workflow = "delivery_framework"
            elif "review" in prompt_lower or "business" in prompt_lower:
                detected_workflow = "business_review"
            
            print(f"   Prompt: '{prompt}' -> Workflow: {detected_workflow}")
            
            if detected_workflow != expected_workflow:
                print(f"❌ FAILED: Expected {expected_workflow}, got {detected_workflow}")
                self.fail(f"Routing failed for '{prompt}'")
            else:
                print("✅ PASS")

if __name__ == '__main__':
    unittest.main()
