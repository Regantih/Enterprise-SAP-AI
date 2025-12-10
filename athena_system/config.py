import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MOCK_MODE = not bool(OPENAI_API_KEY)

if MOCK_MODE:
    print("⚠️  Athena System running in MOCK MODE (No OpenAI API Key found).")
else:
    print("✅ Athena System running in LIVE MODE.")
