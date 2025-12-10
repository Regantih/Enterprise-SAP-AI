import argparse
from athena_system.agents.hestia import HestiaAgent

def run_business_review():
    print(f"🚀 Starting Weekly Business Review Workflow")
    
    hestia = HestiaAgent()
    
    # Generate Report
    report = hestia.generate_business_report()
    
    print("\n" + "="*50)
    print(report)
    print("="*50)

    print("\n✅ Business Review Complete.")

if __name__ == "__main__":
    run_business_review()
