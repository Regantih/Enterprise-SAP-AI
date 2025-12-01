import json
import sys

# --- 1. THE LOGIC (Mirrored from v6.html) ---
# This ensures our Python QA matches the JavaScript behavior exactly.

INTENTS = {
    "TITAN": {
        "keywords": ['titan', 'tesla', 'strategic', 'growth', 'expansion', 'project', 'simulation', 'deploy', 'protocol'],
        "threshold": 1
    },
    "MARKET_LAUNCH": {
        "keywords": ['launch', 'brazil', 'market', 'new region', 'expansion', 'go-to-market', 'subsidiary', 'compliance'],
        "threshold": 1
    },
    "SUPPLY_CHAIN_IMPACT": {
        "keywords": ['impact', 'delayed', 'delay', 'quality', 'consequence', 'downstream', 'customer orders', 'late', 'affect'],
        "threshold": 2
    },
    "SUSTAINABILITY": {
        "keywords": ['carbon', 'sustainability', 'emission', 'green', 'audit', 'co2', 'scope 3', 'climate', 'report'],
        "threshold": 1
    },
    "ORDER_ISSUE": {
        "keywords": ['ordered', 'received', 'receive', 'missing', 'units', 'delivery', 'shipment', 'wrong', 'shortage', 'discrepancy', 'where is', 'track', 'status'],
        "threshold": 1
    },
    "INVENTORY": {
        "keywords": ['stock', 'inventory', 'warehouse', 'availability', 'count', 'sku', 'levels'],
        "threshold": 1
    },
    "HR_HIRING": {
        "keywords": ['hire', 'candidate', 'recruit', 'staffing', 'developer', 'employee', 'headcount', 'requisition', 'interview', 'needs'],
        "threshold": 1
    },
    "FINANCE": {
        "keywords": ['budget', 'finance', 'cost', 'revenue', 'profit', 'margin', 'spend', 'money', 'forecast', 'trends', 'roi', 'ebitda', 'opex', 'cash flow'],
        "threshold": 1
    }
}

def classify_intent(text):
    tokens = text.lower().replace(',', '').replace('.', '').replace('?', '').split()
    best_intent = 'GENERIC'
    max_score = 0

    for intent, data in INTENTS.items():
        score = 0
        for k in data['keywords']:
            if k in text.lower():
                score += 2 # Phrase match
            elif k in tokens:
                score += 1 # Word match
        
        if score >= data['threshold'] and score > max_score:
            max_score = score
            best_intent = intent
            
    return best_intent, max_score

# --- 2. THE TEST RUNNER ---

def run_qa():
    print("🚀 Starting Automated Prompt QA...\n")
    
    filename = 'prompt_roster.json'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            roster = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {filename} not found.")
        return

    passed = 0
    failed = 0
    
    is_large = len(roster) > 100
    if not is_large:
        print(f"{'PROMPT':<50} | {'EXPECTED':<15} | {'ACTUAL':<15} | {'STATUS'}")
        print("-" * 95)

    for i, item in enumerate(roster):
        prompt = item['text']
        expected = item['expected_intent']
        
        actual, score = classify_intent(prompt)
        
        if actual == expected:
            passed += 1
        else:
            failed += 1
            if is_large and failed < 20: # Only show first 20 failures
                 print(f"FAIL: {prompt} -> Got {actual}, Expected {expected}")
            
        if not is_large:
            status = "✅ PASS" if actual == expected else "❌ FAIL"
            print(f"{prompt[:47]+'...':<50} | {expected:<15} | {actual:<15} | {status}")
        
        if is_large and i % 10000 == 0:
            print(f"Processed {i}...")

    print("-" * 95)
    accuracy = (passed / len(roster)) * 100
    print(f"\n📊 SUMMARY:")
    print(f"   Total Tests: {len(roster)}")
    print(f"   Passed:      {passed}")
    print(f"   Failed:      {failed}")
    print(f"   Accuracy:    {accuracy:.1f}%")
    
    if failed == 0:
        print("\n✨ ALL SYSTEMS GO. Logic is sound.")
    else:
        print("\n⚠️  WARNING: Some prompts failed. Adjust keywords in INTENTS.")

if __name__ == "__main__":
    run_qa()
