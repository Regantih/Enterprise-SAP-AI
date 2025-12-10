import argparse
from athena_system.agents.hermes import HermesAgent

def run_lead_gen_workflow(criteria):
    print(f"🚀 Starting Lead Gen & Outreach Workflow for: '{criteria}'")
    
    hermes = HermesAgent()
    
    # 1. Identify Leads
    leads = hermes.identify_leads(criteria)
    print(f"\n✅ Found {len(leads)} potential leads.")
    
    # 2. Draft Outreach for each lead
    print("\n📝 Generating Outreach Drafts...")
    for i, lead in enumerate(leads, 1):
        print(f"\n--- Lead {i}: {lead['company']} ---")
        email_draft = hermes.draft_outreach(lead)
        print(email_draft)
        print("-" * 30)

    print("\n✅ Workflow Complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Lead Gen & Outreach Workflow')
    parser.add_argument('--criteria', type=str, required=True, help='Target criteria for leads (e.g., "FinTech AI Risk")')
    args = parser.parse_args()
    
    run_lead_gen_workflow(args.criteria)
