from flask import Flask, request
import telebot
from user_manager import handle_user_start, handle_admin_message, load_db
from token_manager import handle_token_input
from button_manager import handle_button_commands, handle_callback
from admin_panel import handle_admin_commands

API_TOKEN = "7979366222:AAHD5pq0l-B1qOCv5I_-ZA5GVLkd3noV2h0"
ADMIN_ID = 6887251996

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start_handler(message):
    handle_user_start(bot, message, ADMIN_ID)

@bot.message_handler(func=lambda m: True, content_types=['text'])
def text_handler(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if user_id == ADMIN_ID and text.startswith("javob "):
        handle_admin_message(bot, text)
    elif ":" in text and len(text) > 30:
        handle_token_input(bot, message, ADMIN_ID)
    elif text.startswith("knopka") or text.startswith("o'chirish") or text.startswith("/menu"):
        handle_button_commands(bot, message)
    elif user_id == ADMIN_ID and text.startswith("/admin"):
        handle_admin_commands(bot, message)
    elif user_id == ADMIN_ID and text.startswith("/addslot") or text.startswith("/userinfo"):
        handle_admin_commands(bot, message)
    else:
        bot.send_message(ADMIN_ID, f"📨 Xabar: 👤{message.from_user.first_name} ({user_id})\n{text}")
        bot.send_message(user_id, "✅ Xabaringiz adminga yuborildi.")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    handle_callback(bot, call)

@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/')
def index():
    return "Bot ishlayapti!"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)