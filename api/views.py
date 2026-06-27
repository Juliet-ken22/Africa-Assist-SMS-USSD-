from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .prompts import (
    education_prompt, farming_prompt, health_prompt,
    default_reply, LANGUAGE_PROMPTS
)
from .services import ask_ai, send_sms 
from .models import Message


@csrf_exempt
def sms_reply(request):
    if request.method == "POST":
        message = request.POST.get("text", "").strip()
        phone = request.POST.get("from", "")

        print(f"Message from {phone}: {message}")
        message_upper = message.upper()

        # Detect language prefix
        LANG_PREFIXES = {
            "LG ": "Luganda",
            "SW ": "Swahili",
            "RN ": "Runyankole",
            "AC ": "Acholi",
        }

        LANG_INSTRUCTIONS = {
            "Luganda": "Reply in Luganda language.",
            "Swahili": "Reply in Swahili language.",
            "Runyankole": "Reply in Runyankole language.",
            "Acholi": "Reply in Acholi language.",
            "English": "Reply in English.",
        }

        # Detect language prefix
        detected_language = "English"
        clean_message = message

        for prefix, lang in LANG_PREFIXES.items():
            if message_upper.startswith(prefix):
                detected_language = lang
                clean_message = message[len(prefix):].strip()
                break

        lang_instruction = LANG_INSTRUCTIONS[detected_language]
        clean_upper = clean_message.upper()

        # Smart prompt that handles any message automatically
        smart_prompt = """
You are AfriAssist, an AI assistant for Ugandans.
You help with Education, Farming and Health questions.
Automatically detect what the user is asking about and answer appropriately:
- For education/learning questions: explain clearly at the right level
- For farming questions: give practical Uganda-specific advice
- For health questions: give basic safe advice and recommend visiting a health center for serious issues
- For anything else: answer helpfully and briefly
Always keep answers under 100 words.
Never ask the user to use keywords or change their message format.
"""

        if clean_upper.startswith("LEARN"):
            question = clean_message[5:].strip()
            if not question:
                question = clean_message
            prompt = education_prompt + f"\n{lang_instruction}"
            msg_type = "LEARN"

        elif clean_upper.startswith("FARM"):
            question = clean_message[4:].strip()
            if not question:
                question = clean_message
            prompt = farming_prompt + f"\n{lang_instruction}"
            msg_type = "FARM"

        elif clean_upper.startswith("HEALTH"):
            question = clean_message[6:].strip()
            if not question:
                question = clean_message
            prompt = health_prompt + f"\n{lang_instruction}"
            msg_type = "HEALTH"

        else:
            # No keyword — use smart prompt to answer anything!
            question = clean_message
            prompt = smart_prompt + f"\n{lang_instruction}"
            msg_type = "LEARN"  # default type

        if not question:
            reply = "Welcome to AfriAssist! Ask me anything about farming, health or education."
        else:
            reply = ask_ai(prompt, question)

        Message.objects.create(
            phone=phone,
            message_type=msg_type,
            question=question,
            answer=reply,
            language=detected_language
        )

        send_sms(phone, reply)

        return HttpResponse(reply, content_type="text/plain")

    return HttpResponse("AfriAssist is running!", content_type="text/plain")


@csrf_exempt
def ussd_reply(request):
    if request.method == "POST":
        phone = request.POST.get("phoneNumber", "")
        text = request.POST.get("text", "").strip()

        print(f"USSD from {phone}: text={text}")

        parts = text.split("*") if text else []

        # Step 0 — Language selection menu
        if text == "":
            response = "CON Gyebale! Welcome to AfriAssist!\n"
            response += "Choose language / Londa olulimi:\n"
            response += "1. English\n"
            response += "2. Luganda\n"
            response += "3. Swahili\n"
            response += "4. Runyankole\n"
            response += "5. Acholi"

        # Step 1 — User chose language, show service menu
        elif len(parts) == 1:
            lang_key = parts[0]
            lang = LANGUAGE_PROMPTS.get(lang_key)
            if not lang:
                response = "END Invalid option. Please dial again."
            else:
                response = f"CON {lang['welcome']}\n"
                response += f"{lang['choose_service']}\n"
                response += f"{lang['service_1']}\n"
                response += f"{lang['service_2']}\n"
                response += f"{lang['service_3']}"

        # Step 2 — User chose service, ask for question
        elif len(parts) == 2:
            lang_key = parts[0]
            service = parts[1]
            lang = LANGUAGE_PROMPTS.get(lang_key)
            if not lang or service not in ["1", "2", "3"]:
                response = f"END {lang['invalid'] if lang else 'Invalid option.'}"
            else:
                response = f"CON {lang['enter_question']}"

        # Step 3 — User typed question, get AI answer
        elif len(parts) == 3:
            lang_key = parts[0]
            service = parts[1]
            question = parts[2].strip()
            lang = LANGUAGE_PROMPTS.get(lang_key)

            if not lang or not question:
                response = "END Please enter a valid question."
            else:
                # Build prompt with language instruction
                if service == "1":
                    prompt = education_prompt + f"\n{lang['instruction']}"
                    msg_type = "LEARN"
                elif service == "2":
                    prompt = farming_prompt + f"\n{lang['instruction']}"
                    msg_type = "FARM"
                elif service == "3":
                    prompt = health_prompt + f"\n{lang['instruction']}"
                    msg_type = "HEALTH"
                else:
                    prompt = education_prompt + f"\n{lang['instruction']}"
                    msg_type = "OTHER"

                answer = ask_ai(prompt, question)

                Message.objects.create(
                    phone=phone,
                    message_type=msg_type,
                    question=question,
                    answer=answer,
                    language=lang['name']
                )

                response = f"END {answer}"

        else:
            lang = LANGUAGE_PROMPTS.get(parts[0])
            response = f"END {lang['thanks'] if lang else 'Thank you for using AfriAssist!'}"

        return HttpResponse(response, content_type="text/plain")

    return HttpResponse("USSD endpoint running!", content_type="text/plain")


def dashboard(request):
    messages = Message.objects.all().order_by('-created_at')
    total = messages.count()
    learn_count = messages.filter(message_type='LEARN').count()
    farm_count = messages.filter(message_type='FARM').count()
    health_count = messages.filter(message_type='HEALTH').count()
    unique_users = messages.values('phone').distinct().count()

    context = {
        'messages': messages[:20],
        'total': total,
        'learn_count': learn_count,
        'farm_count': farm_count,
        'health_count': health_count,
        'unique_users': unique_users,
        'learn_pct': round((learn_count / total * 100) if total > 0 else 0),
        'farm_pct': round((farm_count / total * 100) if total > 0 else 0),
        'health_pct': round((health_count / total * 100) if total > 0 else 0),
        'english_count': messages.filter(language='English').count(),
        'luganda_count': messages.filter(language='Luganda').count(),
        'swahili_count': messages.filter(language='Swahili').count(),
        'runyankole_count': messages.filter(language='Runyankole').count(),
        'acholi_count': messages.filter(language='Acholi').count(),
    }
    return render(request, 'dashboard.html', context)


def api_messages(request):
    messages = Message.objects.all().order_by('-created_at')[:20]
    data = list(messages.values(
        'phone', 'message_type', 'language', 'question', 'answer', 'created_at'
    ))
    return JsonResponse({'messages': data})