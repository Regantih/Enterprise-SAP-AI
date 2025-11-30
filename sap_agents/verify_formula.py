import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.enterprise_formula import enterprise_formula

def verify_formula():
    print("🚀 Testing Enterprise Formula")
    print("----------------------------")
    
    # Test Case 1: Balanced Enterprise
    print("\n🔹 Case 1: Balanced Enterprise")
    metrics1 = {
        "performance": 80,
        "efficiency": 70,
        "innovation": 60,
        "risk": 1
    }
    # Expected: ((80*0.4) + (70*0.3) + (60*0.2)) / (1 + 1*0.1)
    # Numerator: 32 + 21 + 12 = 65
    # Denominator: 1.1
    # Result: 59.09
    
    result1 = enterprise_formula.calculate_score(metrics1)
    print(f"   Score: {result1['score']}")
    print(f"   Formula: {result1['formula']}")
    
    assert 59.0 <= result1['score'] <= 59.2, f"Expected ~59.1, got {result1['score']}"
    
    # Test Case 2: High Risk Drag
    print("\n🔹 Case 2: High Risk Drag")
    metrics2 = {
        "performance": 90,
        "efficiency": 90,
        "innovation": 90,
        "risk": 9 # High Risk
    }
    # Numerator: 36 + 27 + 18 = 81
    # Denominator: 1.9
    # Result: 42.6
    
    result2 = enterprise_formula.calculate_score(metrics2)
    print(f"   Score: {result2['score']}")
    
    assert result2['score'] < 50, "High risk should drag score below 50"
    
    print("\n✅ Enterprise Formula Verification Passed!")

if __name__ == "__main__":
    verify_formula()
