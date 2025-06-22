from user_manager import load_db, save_db

def handle_token_input(bot, message, ADMIN_ID):
    user_id = str(message.from_user.id)
    token = message.text.strip()
    db = load_db()
    if user_id in db["limits"] and db["limits"][user_id] >= 1:
        bot.send_message(message.chat.id, "❌ Siz allaqachon bitta bot qo‘shgansiz. Yana qo‘shish uchun admin bilan bog‘laning.")
        return
    db["tokens"][token] = {"owner": user_id}
    db["limits"][user_id] = db["limits"].get(user_id, 0) + 1
    save_db(db)
    bot.send_message(ADMIN_ID, f"✅ Yangi bot token qabul qilindi:
👤 {message.from_user.first_name} ({user_id})
🔐 Token: {token}")
    bot.send_message(message.chat.id, "✅ Bot muvaffaqiyatli ulandi. Endi unga tugmalar qo‘shishingiz mumkin.")
