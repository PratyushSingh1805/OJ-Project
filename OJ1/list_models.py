import google.generativeai as genai

# Replace with your actual API key
genai.configure(api_key="AIzaSyAfJzfuB2dBohAO5TSMZtUNF_TU39VJBkQ")


for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(f"Model Name: {model.name}, Display Name: {model.display_name}")