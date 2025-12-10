import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.engine import engine
from tests.generate_scenarios import ScenarioGenerator
import time

def run_stress_test():
    print("Initializing Stress Test...")
    generator = ScenarioGenerator()
    scenarios = generator.generate_scenarios(150)
    
    passed = 0
    failed = 0
    total_confidence = 0.0
    
    print(f"Running {len(scenarios)} Scenarios...")
    print("-" * 60)
    
    for i, query in enumerate(scenarios):
        print(f"[{i+1}/{len(scenarios)}] Query: {query}")
        
        start_time = time.time()
        result = engine.execute(query)
        duration = time.time() - start_time
        
        if result["status"] == "success":
            passed += 1
            confidence = result["trace"]["confidence"]
            total_confidence += confidence
            print(f"   ✅ PASSED (Conf: {confidence:.2f}, Time: {duration:.3f}s)")
            print(f"      Tool: {result['tool_used']}")
            print(f"      Params: {result['params_used']}")
        else:
            failed += 1
            print(f"   ❌ FAILED")
            print(f"      Error: {result.get('message')}")
            print(f"      Trace: {result.get('trace')}")
            
    print("-" * 60)
    print("STRESS TEST RESULTS")
    print("-" * 60)
    print(f"Total Scenarios: {len(scenarios)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if passed > 0:
        avg_conf = total_confidence / passed
        print(f"Average Confidence: {avg_conf:.2f}")
    else:
        print("Average Confidence: 0.00")
        
    success_rate = (passed / len(scenarios)) * 100
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("\n✅ PASSED: 150/150 Scenarios Solved.")
        sys.exit(0)
    else:
        print(f"\n❌ FAILED: Only {passed}/{len(scenarios)} Solved.")
        sys.exit(1)

if __name__ == "__main__":
    run_stress_test()
