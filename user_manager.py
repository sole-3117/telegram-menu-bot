import json
import os

DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "tokens": {}, "limits": {}, "buttons": {}}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def handle_user_start(bot, message, ADMIN_ID):
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    db = load_db()
    if user_id not in db["users"]:
        db["users"][user_id] = {"name": name}
        save_db(db)
        bot.send_message(ADMIN_ID, f"🆕 Yangi foydalanuvchi: {name} ({user_id})")
    bot.send_message(message.chat.id, f"👋 Salom {name}! Botga xush kelibsiz.Token yuborib yangi bot qo‘shishingiz mumkin.")

def handle_admin_message(bot, text):
    try:
        parts = text.split(" ", 2)
        user_id = parts[1]
        reply_text = parts[2]
        bot.send_message(user_id, f"📩 Admin javobi:
{reply_text}")
    except:
        pass
