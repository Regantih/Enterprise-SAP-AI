"""
Hybrid LLM Router for Athena Core
Attempts Ollama first, falls back to keyword matching if unavailable.
"""
import os
import json
import requests
from typing import Dict, Optional

# Ollama configuration
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

# Agent categories and their semantic mappings
AGENT_CATEGORIES = {
    "Research": ["research", "blog", "topic", "article", "study", "investigate", "analyze trends"],
    "Sales": ["lead", "sales", "prospect", "outreach", "customer", "client", "deal", "pipeline"],
    "Delivery": ["risk", "project", "profile", "governance", "implementation", "deploy", "rollout"],
    "Legal": ["contract", "nda", "agreement", "legal", "compliance", "terms", "liability"],
    "Finance": ["audit", "budget", "financial", "revenue", "cost", "expense", "forecast"],
    "Operations": ["review", "business", "operations", "performance", "kpi", "metrics", "dashboard"],
    "HR": ["employee", "hiring", "recruitment", "talent", "onboarding", "performance review"]
}

ROUTING_PROMPT = """You are a routing agent for an enterprise AI system called Athena Core.

Given a user request, determine which department should handle it.

Available departments:
- Research: For research, analysis, blogs, trends
- Sales: For leads, prospects, outreach, deals
- Delivery: For risk profiles, project governance, implementations
- Legal: For contracts, NDAs, agreements, compliance
- Finance: For audits, budgets, financial analysis
- Operations: For business reviews, KPIs, dashboards
- HR: For employee matters, hiring, recruitment

User request: "{prompt}"

Respond with ONLY the department name (one word), nothing else."""


def check_ollama_available() -> bool:
    """Check if Ollama is running and accessible."""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


def route_with_ollama(prompt: str) -> Optional[str]:
    """Use Ollama LLM for semantic routing."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": ROUTING_PROMPT.format(prompt=prompt),
                "stream": False,
                "options": {"temperature": 0}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            category = result.get("response", "").strip()
            # Validate category
            if category in AGENT_CATEGORIES:
                return category
        return None
    except Exception as e:
        print(f"⚠️ Ollama routing failed: {e}")
        return None


def route_with_keywords(prompt: str) -> str:
    """Fallback keyword-based routing."""
    prompt_lower = prompt.lower()
    
    scores = {}
    for category, keywords in AGENT_CATEGORIES.items():
        score = sum(1 for kw in keywords if kw in prompt_lower)
        if score > 0:
            scores[category] = score
    
    if scores:
        return max(scores, key=scores.get)
    
    return "Operations"  # Default fallback


def route_request(prompt: str) -> Dict:
    """
    Main routing function.
    Tries Ollama first, falls back to keywords.
    """
    method = "keyword"
    category = None
    
    # Try Ollama if available
    if check_ollama_available():
        category = route_with_ollama(prompt)
        if category:
            method = "llm"
    
    # Fallback to keywords
    if not category:
        category = route_with_keywords(prompt)
        method = "keyword"
    
    return {
        "category": category,
        "method": method,
        "ollama_available": check_ollama_available()
    }


# Quick test
if __name__ == "__main__":
    test_prompts = [
        "Find leads for FinTech startups",
        "Create risk profile for Project Alpha",
        "Draft NDA for the new partnership",
        "Analyze revenue trends Q4",
        "Research agentic AI market"
    ]
    
    print("🧪 Testing Hybrid LLM Router\n")
    print(f"Ollama available: {check_ollama_available()}\n")
    
    for prompt in test_prompts:
        result = route_request(prompt)
        print(f"📝 \"{prompt}\"")
        print(f"   → {result['category']} (via {result['method']})\n")
