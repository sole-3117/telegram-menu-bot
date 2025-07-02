from user_manager import load_db, save_db

def handle_admin_commands(bot, message):
    text = message.text
    db = load_db()

    if text == "/admin_users":
        msg = "👥 Foydalanuvchilar ro‘yxati:\n"
        for uid in db:
            msg += f"• {db[uid]['first_name']} ({uid})\n"
        bot.send_message(message.chat.id, msg)

    elif text.startswith("/addslot"):
        try:
            _, uid = text.split(" ", 1)
            if uid in db:
                db[uid]["bot_limit"] += 1
                save_db(db)
                bot.send_message(message.chat.id, f"✅ {uid} uchun 1 slot qo‘shildi. Limit: {db[uid]['bot_limit']}")
        except:
            bot.send_message(message.chat.id, "❗ Foydalanuvchi ID noto‘g‘ri.")

    elif text.startswith("/userinfo"):
        try:
            _, uid = text.split(" ", 1)
            user = db.get(uid)
            if not user:
                bot.send_message(message.chat.id, "❗ Bunday foydalanuvchi topilmadi.")
                return
            info = f"""👤 Foydalanuvchi haqida:
            Ismi: {user['first_name']}
            Username: @{user['username']}
            Ro‘yxatdan o‘tgan: {user['joined']}
            Botlar soni: {len(user['bots'])} / {user.get('bot_limit',1)}
            Tugmalar soni: {len(user.get('buttons', []))}
            ID: {uid}"""
            bot.send_message(message.chat.id, info)
        except:
            bot.send_message(message.chat.id, "❗ Foydalanuvchi ID noto‘g‘ri.")