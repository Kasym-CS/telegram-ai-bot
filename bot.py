import os
from telebot import TeleBot
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот на базе OpenAI. Задай мне любой вопрос!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты полезный ИИ-ассистент."},
                {"role": "user", "content": message.text}
            ]
        )
        ai_reply = response.choices.message.content
        bot.reply_to(message, ai_reply)
        
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при обращении к ИИ: {e}")

if __name__ == "__main__":
    print("Бот успешно запущен...")
    bot.infinity_polling()
