from user_manager import load_db, save_db

def handle_button_commands(bot, message):
    user_id = str(message.from_user.id)
    db = load_db()
    text = message.text.strip()
    user_tokens = [t for t, info in db["tokens"].items() if info["owner"] == user_id]
    if not user_tokens:
        bot.send_message(message.chat.id, "❌ Siz hech qanday bot qo‘shmagansiz.")
        return
    token = user_tokens[0]
    if text.startswith("knopka"):
        try:
            parts = text.split(" ", 2)
            button_text = parts[1]
            button_data = parts[2]
            if token not in db["buttons"]:
                db["buttons"][token] = []
            db["buttons"][token].append({"text": button_text, "data": button_data})
            save_db(db)
            bot.send_message(message.chat.id, f"✅ Tugma '{button_text}' qo‘shildi.")
        except:
            bot.send_message(message.chat.id, "❌ Tugma qo‘shishda xatolik. Format: knopka [matn] [ma’lumot]")
    elif text.startswith("o'chirish") or text.startswith("ochirish"):
        try:
            parts = text.split(" ", 1)
            button_text = parts[1]
            if token in db["buttons"]:
                old_len = len(db["buttons"][token])
                db["buttons"][token] = [b for b in db["buttons"][token] if b["text"] != button_text]
                if len(db["buttons"][token]) < old_len:
                    bot.send_message(message.chat.id, f"🗑 Tugma '{button_text}' o‘chirildi.")
                else:
                    bot.send_message(message.chat.id, f"❌ Bunday tugma topilmadi.")
            else:
                bot.send_message(message.chat.id, "⚠️ Sizda hali hech qanday tugma mavjud emas.")
            save_db(db)
        except:
            bot.send_message(message.chat.id, "❌ Tugma o‘chirishda xatolik. Format: o'chirish [matn]")
