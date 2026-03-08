import os
from dotenv import load_dotenv

print(f"Current working directory: {os.getcwd()}")
print("Loading dotenv...")
load_dotenv()
print(f"GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY')}")

# Try loading from src/.env
print("Loading from src/.env...")
load_dotenv('src/.env')
print(f"GOOGLE_API_KEY from src/.env: {os.getenv('GOOGLE_API_KEY')}")
