import json
from telebot import types
from user_manager import load_data, save_data

def handle_button_commands(bot, message):
    user_id = str(message.from_user.id)
    text = message.text.strip()
    data = load_data()

    # Tekshirish
    if user_id not in data or "bots" not in data[user_id] or not data[user_id]["bots"]:
        bot.send_message(message.chat.id, "❗️Avval bot tokenini yuboring.")
        return

    current_bot = data[user_id]["bots"][-1]
    if "buttons" not in current_bot:
        current_bot["buttons"] = []

    # Tugma qo‘shish
    if text.startswith("knopka "):
        try:
            content = text[7:]
            name, url = content.split("|")
            current_bot["buttons"].append({"text": name.strip(), "url": url.strip()})
            save_data(data)
            bot.send_message(message.chat.id, f"✅ Tugma qo‘shildi: {name}")
        except:
            bot.send_message(message.chat.id, "⚠️ Noto‘g‘ri format. Masalan:\nknopka 🎬 Kino|https://kino.uz")

    # Tugmalarni ko‘rish
    elif text == "ko‘rish":
        if not current_bot["buttons"]:
            bot.send_message(message.chat.id, "⚠️ Tugmalar mavjud emas.")
            return

        msg = "📋 Tugmalar ro‘yxati:\n\n"
        for i, btn in enumerate(current_bot["buttons"], start=1):
            msg += f"{i}. {btn['text']} - {btn['url']}\n"
        bot.send_message(message.chat.id, msg)

    # Tugma o‘chirish (raqam orqali)
    elif text.startswith("o‘chirish "):
        try:
            index = int(text.split()[1]) - 1
            removed = current_bot["buttons"].pop(index)
            save_data(data)
            bot.send_message(message.chat.id, f"❌ O‘chirildi: {removed['text']}")
        except:
            bot.send_message(message.chat.id, "⚠️ Noto‘g‘ri format yoki noto‘g‘ri raqam. Masalan:\no‘chirish 1")

    # Tugma tahrirlash (raqam bilan yangi text|url)
    elif text.startswith("tahrirla "):
        try:
            parts = text.split(maxsplit=2)
            index = int(parts[1]) - 1
            name, url = parts[2].split("|")
            current_bot["buttons"][index] = {"text": name.strip(), "url": url.strip()}
            save_data(data)
            bot.send_message(message.chat.id, f"✏️ Tahrirlandi: {name}")
        except:
            bot.send_message(message.chat.id, "⚠️ Format xato. Masalan:\ntahrirla 1 📺 Kino|https://kino.uz")