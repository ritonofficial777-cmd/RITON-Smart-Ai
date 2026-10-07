import os
import threading
from flask import Flask
import telebot
from google import genai

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running perfectly!'

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = genai.Client(api_key=GEMINI_KEY)

@bot.message_handler(commands=['models'])
def show_models(message):
    try:
        models = [m.name for m in client.models.list()]
        reply_text = "আপনার উপলব্ধ মডেল তালিকা:\n" + "\n".join(models[:15])
        bot.reply_to(message, reply_text)
    except Exception as e:
        bot.reply_to(message, f"লিস্ট আনতে সমস্যা: {e}")

@bot.message_handler(func=lambda message: True)
def reply(message):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"ত্রুটি: {e}\n\nউপলব্ধ মডেল দেখতে /models লিখে পাঠান।")

def run_bot():
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    
