import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load it
load_dotenv('src/.env')
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("FAILED: GOOGLE_API_KEY not found in src/.env")
    exit(1)

print(f"Testing key: {api_key[:10]}...")
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('gemini-1.5-flash-8b') # Use small model for fast test
    response = model.generate_content("hello")
    print("SUCCESS: Key is valid and working!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"FAILED: Key check failed with error: {e}")
