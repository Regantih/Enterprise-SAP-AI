import requests
import json
import time

BASE_URL = "http://localhost:8000/api/interview/interact"
SESSION_ID = f"debug_session_{int(time.time())}"

def chat(stage, message):
    payload = {
        "session_id": SESSION_ID,
        "current_stage": stage,
        "message": message
    }
    try:
        res = requests.post(BASE_URL, json=payload)
        data = res.json()
        print(f"[{stage}] -> Answer: '{message}'")
        print(f"   Response Status: {data.get('status')}")
        print(f"   Next Stage: {data.get('next_stage')}")
        print("-" * 40)
        return data.get("next_stage"), data.get("status")
    except Exception as e:
        print(f"API Error: {e}")
        return None, None

# 0. Init
print("--- STARTING DEBUG SESSION ---")
current_stage, status = chat("start", "INIT")

# 1. Answer Origin
if current_stage:
    current_stage, status = chat(current_stage, "I am here to crush the competition and build a legacy.")

# 2. Answer IQ
if current_stage:
    current_stage, status = chat(current_stage, "Entropy increases but a new force could reverse it through structured logic.")

# 3. Answer EQ
if current_stage:
    current_stage, status = chat(current_stage, "I would optimize for long-term survival while minimizing suffering.")

# 4. Answer Drive
if current_stage:
    current_stage, status = chat(current_stage, "I never give up. I built a startup from zero.")

print("--- FINAL RESULT ---")
print(f"Final Status: {status}")
if status == "ACCESS_GRANTED":
    print("SUCCESS: Backend is working correctly.")
else:
    print("FAILURE: Backend logic did not trigger completion.")
