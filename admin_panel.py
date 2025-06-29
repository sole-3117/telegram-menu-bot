from user_manager import load_db

def handle_admin_commands(bot, message):
    text = message.text
    if text == "/admin_users":
        db = load_db()
        users = list(db.keys())
        msg = "👥 Bot foydalanuvchilari:
" + "\n".join(users)
        bot.send_message(message.chat.id, msg)