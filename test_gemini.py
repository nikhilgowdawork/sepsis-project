import google.generativeai as genai
import os

# Test the API key
api_key = "AIzaSyDFKc6DCTSSkuwmAAe7VYzUaJce4mdoxyw"
genai.configure(api_key=api_key)

print("Testing Gemini API...")

# List available models
try:
    models = genai.list_models()
    print("Available models:")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")

# Test with a simple prompt
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello, say 'API is working!'")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error generating content: {e}")

# Test with different models
models_to_test = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-flash-latest', 'gemini-pro-latest']

for model_name in models_to_test:
    try:
        print(f"\nTesting {model_name}...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'working'", generation_config={"max_output_tokens": 50})
        print(f"✅ {model_name}: {response.text}")
    except Exception as e:
        print(f"❌ {model_name}: {e}")
