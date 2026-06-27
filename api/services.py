import os
import requests
from groq import Groq

# All credentials from environment variables
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
AT_USERNAME = os.environ.get('AT_USERNAME')
AT_API_KEY = os.environ.get('AT_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# SMS URLs
AT_SMS_URL_SANDBOX = "https://api.sandbox.africastalking.com/version1/messaging"
AT_SMS_URL_LIVE = "https://api.africastalking.com/version1/messaging/"

def send_sms(phone, message):
    try:
        url = AT_SMS_URL_SANDBOX if ENVIRONMENT == 'development' else AT_SMS_URL_LIVE
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "apiKey": AT_API_KEY
        }
        payload = {
            "username": AT_USERNAME,
            "from":"10614",
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
#     openai.api_key = os.environ.get('OPENAI_API_KEY')
#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": question}
#         ]
#     )
#     return response.choices[0].message.content


