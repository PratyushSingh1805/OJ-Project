import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API with the loaded key
genai.configure(api_key=api_key)

# List and display available models
for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(f"Model Name: {model.name}, Display Name: {model.display_name}")
