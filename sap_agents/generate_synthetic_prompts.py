import json
import random
import itertools

# --- CONFIGURATION ---
TARGET_COUNT = 150000

# --- DATA SLOTS ---
VENDORS = ['Alcoa', 'Rio Tinto', 'LogiBras', 'Tesla', 'Supplier X', 'Acme Corp', 'Globex', 'Soylent Corp', 'Umbrella Corp', 'Stark Ind']
PRODUCTS = ['X100', 'Y200', 'Z300', 'Aluminum', 'Copper', 'Steel', 'Lithium', 'Microchips', 'Sensors', 'Batteries']
METRICS = ['revenue', 'profit', 'margin', 'cost', 'budget', 'spend', 'cash flow', 'roi', 'ebitda', 'opex']
ROLES = ['developer', 'engineer', 'manager', 'director', 'analyst', 'consultant', 'designer', 'architect', 'admin', 'vp']
REGIONS = ['Brazil', 'Germany', 'USA', 'China', 'India', 'Japan', 'UK', 'France', 'Canada', 'Mexico']
PROJECTS = ['Titan', 'Tesla', 'Apollo', 'Gemini', 'Mercury', 'Manhattan', 'BlueBook', 'Origin', 'Omega', 'Alpha']

# --- TEMPLATES PER INTENT ---
TEMPLATES = {
    "ORDER_ISSUE": [
        "Where is my shipment from {vendor}?",
        "I ordered {qty} units of {product} but received {qty2}",
        "Missing delivery from {vendor}",
        "Track order #{order_id}",
        "Discrepancy in shipment of {product}",
        "My order of {product} is wrong",
        "Did we receive the {product} from {vendor}?",
        "Shipment from {vendor} is short {qty} units",
        "Where is the {product} stock?",
        "Check delivery status for {vendor}"
    ],
    "TITAN": [
        "Execute Project {project}",
        "Initiate {project} protocol",
        "Start strategic growth plan: {project}",
        "Run simulation for {project}",
        "Status of Project {project}",
        "Deploy {project} sequence"
    ],
    "MARKET_LAUNCH": [
        "Launch product in {region}",
        "Expand market to {region}",
        "Go-to-market strategy for {region}",
        "Open new subsidiary in {region}",
        "Check compliance for {region} launch"
    ],
    "FINANCE": [
        "Check {metric} for Q4",
        "Show me {metric} trends",
        "What is our current {metric}?",
        "Analyze {metric} vs budget",
        "Forecast for {metric}"
    ],
    "HR_HIRING": [
        "Hire a new {role}",
        "Recruit candidate for {role} position",
        "Open requisition for {role}",
        "Staffing needs for {role}",
        "Interviewing {role} candidates"
    ],
    "INVENTORY": [
        "Check inventory for {product}",
        "Stock availability of {product}",
        "Count {product} in warehouse",
        "Do we have {product} in stock?",
        "Warehouse levels for {product}"
    ],
    "SUSTAINABILITY": [
        "Audit carbon footprint for {vendor}",
        "Check co2 emissions for {region} plant",
        "Sustainability report for {vendor}",
        "Green audit for {product} line",
        "Scope 3 emissions for {vendor}"
    ]
}

def generate_prompts():
    print(f"🚀 Generating {TARGET_COUNT} synthetic prompts...")
    dataset = []
    
    # We will loop until we hit the target
    while len(dataset) < TARGET_COUNT:
        for intent, templates in TEMPLATES.items():
            template = random.choice(templates)
            
            # Fill slots
            text = template.format(
                vendor=random.choice(VENDORS),
                product=random.choice(PRODUCTS),
                metric=random.choice(METRICS),
                role=random.choice(ROLES),
                region=random.choice(REGIONS),
                project=random.choice(PROJECTS),
                qty=random.randint(10, 1000),
                qty2=random.randint(1, 100),
                order_id=random.randint(10000, 99999)
            )
            
            dataset.append({
                "text": text,
                "expected_intent": intent
            })
            
            if len(dataset) >= TARGET_COUNT:
                break
    
    print(f"✅ Generated {len(dataset)} prompts.")
    
    with open('prompt_roster_large.json', 'w') as f:
        json.dump(dataset, f, indent=None) # Compact JSON to save space
    print("💾 Saved to prompt_roster_large.json")

if __name__ == "__main__":
    generate_prompts()
