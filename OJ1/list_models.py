import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(f"Model Name: {model.name}, Display Name: {model.display_name}")
