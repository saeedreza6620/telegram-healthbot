from flask import Flask, request
import openai
import telegram

TOKEN = "8216009666:AAH8cP6TlzG71B3mBSNbYe86QgyCruOrokA"
API_KEY = "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"
BOT = telegram.Bot(token=TOKEN)

openai.api_key = API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

app = Flask(__name__)

def normalize_input(text):
    replacements = {
        "قند خون": "Blood Glucose", "قند": "Blood Sugar", "تری‌گلیسرید": "Triglycerides",
        "کلسترول کل": "Total Cholesterol", "ویتامین D": "Vitamin D", "HbA1c": "HbA1c",
        "CRP": "CRP", "HDL": "HDL", "LDL": "LDL"
    }
    for fa, en in replacements.items():
        text = text.replace(fa, en)
    return text

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    user_input = normalize_input(data['message']['text'])

    messages = [
        {"role": "system", "content": "شما یک پزشک متخصص هستید. نتایج آزمایش را تحلیل کرده و به فارسی توصیه تغذیه‌ای بدهید."},
        {"role": "user", "content": user_input}
    ]

    try:
        completion = openai.ChatCompletion.create(
            model="openchat/openchat-7b",
            messages=messages
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"❌ خطا: {e}"

    BOT.send_message(chat_id=chat_id, text=reply)
    return 'ok'

@app.route('/')
def home():
    return "✅ ربات سالمه و در حال اجراست"

