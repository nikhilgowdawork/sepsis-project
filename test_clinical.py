import google.generativeai as genai

# Test the API key
api_key = "AIzaSyDFKc6DCTSSkuwmAAe7VYzUaJce4mdoxyw"
genai.configure(api_key=api_key)

# Test with clinical vitals
vitals_data = {
    'temperature': 39.2,
    'heart_rate': 125,
    'respiratory_rate': 28,
    'systolic_bp': 85,
    'diastolic_bp': 50,
    'wbc_count': 16.5,
    'lactate': 4.2,
    'age': 65,
    'gender': 'M'
}

prompt = f"""Review these ICU patient vitals and provide 3 numbered interventions:

Patient Vitals: {vitals_data}

Format:
1. [Intervention with specific details]
2. [Intervention with specific details] 
3. [Intervention with specific details]"""

try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.3,
            "max_output_tokens": 1000,
        },
    )
    
    print("✅ GEMINI AI CLINICAL RECOMMENDATIONS:")
    print(response.text)
    
except Exception as e:
    print(f"❌ Error: {e}")
