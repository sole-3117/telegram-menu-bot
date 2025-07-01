from user_manager import load_db, save_db
import telebot

def handle_button_commands(bot, message):
    user_id = str(message.from_user.id)
    text = message.text.strip()
    db = load_db()

    if user_id not in db or not db[user_id]["bots"]:
        bot.send_message(message.chat.id, "❗ Avval bot tokenini yuboring.")
        return

    if text.startswith("knopka"):
        parts = text.split(" ", 2)
        if len(parts) < 3:
            bot.send_message(message.chat.id, "❗ Format: knopka <matn> <callback>")
            return
        title, callback = parts[1], parts[2]
        db[user_id]["buttons"].append({"text": title, "callback_data": callback})
        save_db(db)
        bot.send_message(message.chat.id, f"✅ Tugma saqlandi: {title}")

    elif text.startswith("/menu"):
        markup = telebot.types.InlineKeyboardMarkup()
        for btn in db[user_id]["buttons"]:
            markup.add(telebot.types.InlineKeyboardButton(text=btn["text"], callback_data=btn["callback_data"]))
        bot.send_message(message.chat.id, "📋 Sizning menyuingiz:", reply_markup=markup)

    elif text.startswith("o'chirish"):
        db[user_id]["buttons"] = []
        save_db(db)
        bot.send_message(message.chat.id, "🗑 Barcha tugmalar o‘chirildi.")

def handle_callback(bot, call):
    bot.answer_callback_query(call.id, f"✅ Siz '{call.data}' tugmasini bosdingiz.")