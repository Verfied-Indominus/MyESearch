import json
import requests

headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzljZDJkODQtNzY0Ni00Mzc1LTg0NWMtODgzZjQ2MzU4Nzk3IiwidHlwZSI6ImFwaV90b2tlbiJ9.TvXGvOKmWyy2Qkn3mV04WgYX0QHymf77x9CC8wRhs-Y"}

url = "https://api.edenai.run/v2/text/chat"

def ai_prompt(text):
    payload = {
        "providers": "google",
        "text": text,
        "chatbot_global_action": "Act as an assistant",
        "previous_history": [],
        "temperature": 0.5,
        "max_tokens": 1000,
        "fallback_providers": ""
    }
    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    print(result['google']['generated_text'])
    return result['google']['generated_text']



