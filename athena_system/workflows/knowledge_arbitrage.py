import argparse
from athena_system.agents.apollo import ApolloAgent
from athena_system.agents.clio import ClioAgent
from athena_system.agents.critic import CriticAgent

def run_knowledge_arbitrage(topic):
    print(f"🚀 Starting Knowledge Arbitrage Workflow for: '{topic}'")
    
    # 1. Research (Apollo)
    apollo = ApolloAgent()
    research_report = apollo.research(topic)
    print("\n✅ Research Complete.")
    
    # 2. Content Generation (Clio)
    clio = ClioAgent()
    linkedin_post = clio.generate_content(research_report, "linkedin")
    blog_post = clio.generate_content(research_report, "blog")
    
    print("\n✅ Content Generation Complete.")

    # 3. Critic Review (The Quality Gate)
    critic = CriticAgent()
    review = critic.review_content(linkedin_post, "linkedin_post")
    
    if review['status'] == "Approved":
        linkedin_post += f"\n\n{review['verification_stamp']}"
        print(f"\n✅ Critic Approved with Score: {review['safety_score']}")
    else:
        print("\n❌ Critic Rejected Content.")
    
    # 4. Output
    print("\n" + "="*50)
    print("OUTPUT: LINKEDIN POST")
    print("="*50)
    print(linkedin_post)
    
    print("\n" + "="*50)
    print("OUTPUT: BLOG POST")
    print("="*50)
    print(blog_post)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Knowledge Arbitrage Workflow')
    parser.add_argument('--topic', type=str, required=True, help='Topic to research')
    args = parser.parse_args()
    
    run_knowledge_arbitrage(args.topic)
