from flask import Flask, request
import telebot
from user_manager import handle_user_start, handle_admin_message
from token_manager import handle_token_input
from button_manager import handle_button_commands
from admin_panel import handle_admin_commands
import os

# Bot sozlamalari
API_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)
ADMIN_ID = 6887251996  # O‘zingizning Telegram ID'ingizni yozing

# Flask server
app = Flask(__name__)

# /start komandasi
@bot.message_handler(commands=['start'])
def start_handler(message):
    handle_user_start(bot, message, ADMIN_ID)

# Oddiy matnli xabarlar uchun handler
@bot.message_handler(func=lambda message: True, content_types=['text'])
def text_handler(message):
    user_id = message.from_user.id
    text = message.text

    if user_id == ADMIN_ID and text.startswith("javob "):
        handle_admin_message(bot, text)
    elif ":" in text and len(text) > 20:
        handle_token_input(bot, message, ADMIN_ID)
    elif text.startswith("knopka") or text.startswith("o'chirish"):
        handle_button_commands(bot, message)
    elif user_id == ADMIN_ID and text.startswith("/admin"):
        handle_admin_commands(bot, message)
    else:
        # Oddiy foydalanuvchi xabari adminga yuboriladi
        bot.send_message(ADMIN_ID, f"📨 Xabar: 👤{message.from_user.first_name} ({user_id}) {text}")
        bot.send_message(user_id, "✅ Xabaringiz adminga yuborildi.")

# Telegram webhook uchun
@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

# Bosh sahifa
@app.route('/')
def index():
    return "Bot ishlayapti!"

# Flask serverni ishga tushirish (Render.com uchun to‘g‘ri port bilan)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render PORT o‘zgaruvchisidan oladi
    app.run(host='0.0.0.0', port=port)