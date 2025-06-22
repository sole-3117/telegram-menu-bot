from user_manager import load_db, save_db

def handle_admin_commands(bot, message):
    user_id = str(message.from_user.id)
    text = message.text.strip()
    db = load_db()

    if text.startswith("/admin statistik"):
        total_users = len(db["users"])
        total_tokens = len(db["tokens"])
        bot.send_message(user_id, f"📊 Statistika:
👥 Foydalanuvchilar: {total_users}
🤖 Botlar: {total_tokens}")

    elif text.startswith("/admin foydalanuvchilar"):
        msg = "👥 Foydalanuvchilar:
"
        for uid, info in db["users"].items():
            msg += f"- {info['name']} ({uid})
"
        bot.send_message(user_id, msg if msg else "❌ Foydalanuvchi yo‘q")

    elif text.startswith("/admin tokenlar"):
        msg = "🔑 Tokenlar:
"
        for token, info in db["tokens"].items():
            msg += f"- {token} => {info['owner']}
"
        bot.send_message(user_id, msg if msg else "❌ Hech qanday token yo‘q")

    elif text.startswith("/admin broadcast "):
        msg_text = text.replace("/admin broadcast ", "")
        for uid in db["users"]:
            try:
                bot.send_message(uid, f"📢 {msg_text}")
            except:
                continue
        bot.send_message(user_id, "✅ Xabar barcha foydalanuvchilarga yuborildi.")
