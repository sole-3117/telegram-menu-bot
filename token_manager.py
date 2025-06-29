from user_manager import load_db, save_db

def handle_token_input(bot, message, admin_id):
    user_id = str(message.from_user.id)
    token = message.text.strip()
    db = load_db()
    if user_id not in db:
        db[user_id] = {"bots": []}
    if token in db[user_id]["bots"]:
        bot.send_message(message.chat.id, "❗ Bu token allaqachon qo‘shilgan.")
        return
    if len(db[user_id]["bots"]) >= 1:
        bot.send_message(message.chat.id, "🚫 Faqat 1ta bot bepul qo‘shilishi mumkin. Ko‘proq bot qo‘shish uchun adminga murojaat qiling.")
        bot.send_message(admin_id, f"💰 {user_id} yangi bot qo‘shmoqchi: {token}")
        return
    db[user_id]["bots"].append(token)
    save_db(db)
    bot.send_message(message.chat.id, "✅ Bot token qabul qilindi va qo‘shildi.")
    bot.send_message(admin_id, f"➕ Yangi bot qo‘shildi: {token}
👤 {user_id}")
