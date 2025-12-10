import json
import random

# Load existing templates
with open('sap-joule-agents/agent-templates.json', 'r') as f:
    data = json.load(f)
    templates = data['agents']

# Categories for generation
categories = ["Supply Chain", "Finance", "HR", "Sales", "Manufacturing", "R&D", "IT", "Legal"]
roles = ["Analyst", "Advisor", "Optimizer", "Assistant", "Automator", "Forecaster"]

agents = []

# Add Real Templates
for t in templates:
    agents.append({
        "id": t['name'].lower().replace(" ", "_"),
        "name": t['name'],
        "description": t['description'],
        "category": "Core",
        "status": "active",
        "type": "template"
    })

# Generate Placeholders to reach 400
count = len(agents)
while count < 400:
    cat = random.choice(categories)
    role = random.choice(roles)
    name = f"{cat} {role} {count+1}"
    agents.append({
        "id": f"agent_{count+1}",
        "name": name,
        "description": f"AI agent specialized in {cat} processes to assist as a {role}.",
        "category": cat,
        "status": "mock",
        "type": "generated"
    })
    count += 1

# Save Registry
with open('athena_system/config/registry.json', 'w') as f:
    json.dump({"agents": agents}, f, indent=2)

print(f"Generated registry with {len(agents)} agents.")
