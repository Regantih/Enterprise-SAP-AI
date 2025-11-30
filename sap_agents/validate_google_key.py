import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def validate_google_key():
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in .env")
        print("   Please add it to your .env file: GOOGLE_API_KEY=AIzaSy...")
        return

    print(f"🔑 Found Key: {api_key[:5]}...{api_key[-5:]}")
    print("🧠 Connecting to Google Gemini...")

    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
        response = llm.invoke("Hello, are you working?")
        
        print("\n✅ Success! Google Gemini responded:")
        print(f"   '{response.content}'")
        
    except Exception as e:
        print(f"\n❌ Connection Failed: {str(e)}")
        print("   Check if the key is valid and has the 'Generative Language API' enabled.")

if __name__ == "__main__":
    validate_google_key()
