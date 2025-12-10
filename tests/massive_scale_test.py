import sys
import os
import random
import time
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from athena_system.agents.orchestrator import OrchestratorAgent

def run_massive_scale_test():
    print("🚀 Starting Massive Scale Verification (400+ Agents)...")
    print(f"📅 Timestamp: {datetime.now().isoformat()}")
    print("-" * 60)

    orchestrator = OrchestratorAgent()
    
    # Test Scenarios targeting different domains
    scenarios = [
        ("Supply Chain", ["optimize logistics", "track shipment", "supplier delay", "inventory forecast"]),
        ("Finance", ["audit report", "expense analysis", "Q3 revenue", "tax compliance"]),
        ("HR", ["employee onboarding", "payroll check", "benefits enrollment", "hiring plan"]),
        ("Sales", ["customer churn", "sales pipeline", "lead qualification", "deal closing"]),
        ("IT", ["server outage", "security patch", "cloud migration", "network latency"]),
        ("Legal", ["contract review", "compliance check", "NDA drafting", "IP protection"]),
        ("R&D", ["patent search", "prototype testing", "feasibility study", "innovation lab"]),
        ("Manufacturing", ["production line", "quality control", "maintenance schedule", "yield optimization"])
    ]

    total_tests = 50
    passed = 0
    failed = 0
    agents_triggered = set()

    results = []

    start_time = time.time()

    for i in range(1, total_tests + 1):
        category, prompts = random.choice(scenarios)
        prompt = f"I need help to {random.choice(prompts)} for {category} department."
        
        print(f"Test #{i}: '{prompt}'", end=" ... ")
        
        response = orchestrator.route_request(prompt)
        
        if response['status'] == 'success':
            print(f"✅ Routed to: {response['agent']}")
            passed += 1
            agents_triggered.add(response['agent'])
            results.append(f"| {i} | {prompt} | ✅ Success | {response['agent']} |")
        else:
            print(f"❌ FAILED: {response['message']}")
            failed += 1
            results.append(f"| {i} | {prompt} | ❌ Failed | N/A |")

    end_time = time.time()
    duration = end_time - start_time

    print("-" * 60)
    print(f"📊 Test Summary:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed:      {passed}")
    print(f"   Failed:      {failed}")
    print(f"   Unique Agents Triggered: {len(agents_triggered)}")
    print(f"   Duration:    {duration:.2f}s")
    print("-" * 60)

    # Generate Evidence Artifact
    with open("test_evidence.md", "w") as f:
        f.write("# Massive Scale Test Evidence\n\n")
        f.write(f"**Date**: {datetime.now().isoformat()}\n")
        f.write(f"**Total Agents in Registry**: {len(orchestrator.registry)}\n")
        f.write(f"**Tests Run**: {total_tests}\n")
        f.write(f"**Success Rate**: {(passed/total_tests)*100:.1f}%\n\n")
        f.write("## Detailed Execution Log\n")
        f.write("| ID | Prompt | Status | Assigned Agent |\n")
        f.write("|----|--------|--------|----------------|\n")
        for line in results:
            f.write(line + "\n")

    print("📄 Evidence saved to 'test_evidence.md'")

if __name__ == "__main__":
    run_massive_scale_test()
