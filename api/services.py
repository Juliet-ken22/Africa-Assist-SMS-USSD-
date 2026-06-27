import requests
from groq import Groq

# Africa's Talking credentials
AT_USERNAME = "afriassist"
AT_API_KEY = "atsk_4e25febabf2e15333d81173fb49eb698d481f2ffe49b1d6d47b51530e0ea5c7fb6ba97e9"

# Groq credentials - FREE!
GROQ_API_KEY = "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"

def send_sms(phone, message):
    try:
        url = "https://api.africastalking.com/version1/messaging/bulk"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "apiKey": AT_API_KEY
        }
        payload = {
            "username": AT_USERNAME,
            "to": phone,
            "message": message
        }
        response = requests.post(url, headers=headers, data=payload, verify=False)
        print(f"SMS sent: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"SMS send error: {e}")
        return None

def ask_ai(system_prompt, question):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq error: {e}")
        return "Sorry I could not process your request. Please try again."

# -----------------------------------------------
# REAL OpenAI - uncomment at hackathon
# -----------------------------------------------
# def ask_ai(system_prompt, question):
#     import openai
#     openai.api_key = "PASTE_HACKATHON_KEY_HERE"
#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": question}
#         ]
#     )
#     return response.choices[0].message.content