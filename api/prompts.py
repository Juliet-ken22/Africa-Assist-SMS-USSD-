education_prompt = """
You are a knowledgeable teacher in Uganda covering all education levels from primary to secondary school.
When answering:
- For simple or basic questions, explain like you are talking to a primary school student.
- For advanced questions, explain at secondary school level.
- Always use simple clear language.
- Give practical examples where possible.
- Keep your answer under 100 words.
- IMPORTANT: Reply in the same language as instructed in the system message.
"""

farming_prompt = """
You are an agricultural extension officer in Uganda.
Give practical farming advice that a small-scale farmer can apply immediately.
Keep your answer under 100 words.
- IMPORTANT: Reply in the same language as instructed in the system message.
"""

health_prompt = """
You are a community health worker in Uganda.
Give simple, practical, and safe health advice.
Always recommend visiting a health center for serious symptoms.
Keep your answer under 100 words.
- IMPORTANT: Reply in the same language as instructed in the system message.
"""

default_reply = (
    "Welcome to AfriAssist!\n"
    "Send:\n"
    "LEARN <question> - for education\n"
    "FARM <question> - for farming\n"
    "HEALTH <question> - for health advice\n\n"
    "Examples:\n"
    "LEARN What is photosynthesis?\n"
    "FARM My maize has yellow leaves\n"
    "HEALTH My child has a fever"
)

LANGUAGE_PROMPTS = {
    "1": {
        "name": "English",
        "instruction": "Reply in English.",
        "welcome": "Welcome to AfriAssist!",
        "choose_service": "Choose a service:",
        "service_1": "1. Learning",
        "service_2": "2. Farming",
        "service_3": "3. Health",
        "enter_question": "Type your question:",
        "invalid": "Invalid option. Please dial again.",
        "thanks": "Thank you for using AfriAssist!",
    },
    "2": {
        "name": "Luganda",
        "instruction": "Reply in Luganda language.",
        "welcome": "Gyebale! Tukulamusizza ku AfriAssist!",
        "choose_service": "Londa:",
        "service_1": "1. Okusoma (Learning)",
        "service_2": "2. Obulimi (Farming)",
        "service_3": "3. Obulamu (Health)",
        "enter_question": "Wandiika ekibuuzo kyawo:",
        "invalid": "Sirivana. Ddamu okukuba enamba.",
        "thanks": "Webale okozesa AfriAssist!",
    },
    "3": {
        "name": "Swahili",
        "instruction": "Reply in Swahili language.",
        "welcome": "Karibu AfriAssist!",
        "choose_service": "Chagua huduma:",
        "service_1": "1. Elimu (Learning)",
        "service_2": "2. Kilimo (Farming)",
        "service_3": "3. Afya (Health)",
        "enter_question": "Andika swali lako:",
        "invalid": "Chaguo batili. Piga simu tena.",
        "thanks": "Asante kwa kutumia AfriAssist!",
    },
    "4": {
        "name": "Runyankole",
        "instruction": "Reply in Runyankole language.",
        "welcome": "Karimu ku AfriAssist!",
        "choose_service": "Hunduura:",
        "service_1": "1. Kwegyesa (Learning)",
        "service_2": "2. Obuhingi (Farming)",
        "service_3": "3. Obuzima (Health)",
        "enter_question": "Handika ikibuuzo kyawe:",
        "invalid": "Ebiro bibi. Oza okukuba.",
        "thanks": "Webale okozesa AfriAssist!",
    },
    "5": {
        "name": "Acholi",
        "instruction": "Reply in Acholi language.",
        "welcome": "Ibed maber! Abiyo i AfriAssist!",
        "choose_service": "Yero tic:",
        "service_1": "1. Pwony (Learning)",
        "service_2": "2. Pur (Farming)",
        "service_3": "3. Yot Kome (Health)",
        "enter_question": "Coo penyo ni:",
        "invalid": "Ayela. Tem doki.",
        "thanks": "Apwoyo pi tiyo ki AfriAssist!",
    },
}