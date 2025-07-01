import json
import os
from datetime import datetime

DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def handle_user_start(bot, message, admin_id):
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    username = message.from_user.username or "yo‘q"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    db = load_db()

    if user_id not in db:
        db[user_id] = {
            "first_name": name,
            "username": username,
            "joined": now,
            "bots": [],
            "bot_limit": 1,
            "buttons": []
        }
        save_db(db)
        bot.send_message(admin_id, f"🆕 Yangi foydalanuvchi: {name} ({user_id})")

    if int(user_id) == int(admin_id):
        bot.send_message(message.chat.id, "👋 Salom Solejon! Botga xush kelibsiz.")
    else:
        bot.send_message(message.chat.id, f"👋 Salom {name}! Botga xush kelibsiz.")

def handle_admin_message(bot, text):
    try:
        _, uid, msg = text.split(" ", 2)
        bot.send_message(int(uid), f"📩 Admin javobi:\n{msg}")
    except:
        pass