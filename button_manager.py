from user_manager import load_db, save_db
import telebot

user_bots = {}

def handle_button_commands(bot, message):
    user_id = str(message.from_user.id)
    text = message.text.strip()
    db = load_db()

    if user_id not in db or not db[user_id]["bots"]:
        bot.send_message(message.chat.id, "❗ Avval bot tokenini yuboring.")
        return

    target_token = db[user_id]["bots"][0]
    if target_token not in user_bots:
        user_bots[target_token] = telebot.TeleBot(target_token)

    user_bot = user_bots[target_token]

    if text.startswith("knopka"):
        parts = text.split(" ", 2)
        if len(parts) < 3:
            bot.send_message(message.chat.id, "❗ Format: knopka <text> <callback_data>")
            return
        title, callback = parts[1], parts[2]
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text=title, callback_data=callback))
        user_bot.send_message(message.chat.id, "🔘 Yangi tugma:", reply_markup=markup)
        bot.send_message(message.chat.id, "✅ Tugma yuborildi.")
    elif text.startswith("o'chirish"):
        user_bot.send_message(message.chat.id, "🗑 Tugmalar o‘chirildi.")
        bot.send_message(message.chat.id, "✅ O‘chirish buyrug‘i yuborildi.")
