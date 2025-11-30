import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def list_models():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("No API Key found.")
        return

    genai.configure(api_key=api_key)
    
    print("Listing available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
