from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# بيانات المواد حسب الفصل
semester_data = {
    "السابع": [
        "اقتصاد هندسي", "تصميم خرسانة 2", "تصميم فولاذ 1", "حساب كميات", "فكر إسلامي",
        "ميكانيكا تربة 2", "هندسة طرق 1", "هيدروليكا 1", "واقع إسلامي"
    ],
    "الثامن": [
        "إدارة تشييد", "تصميم خرسانة 3", "تصميم فولاذ 2", "دراسات قرآنية",
        "هندسة بيئية", "هندسة طرق 2", "هيدروليكا 2"
    ]
}

# عند /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 الفصل السابع", callback_data='السابع')],
        [InlineKeyboardButton("📘 الفصل الثامن", callback_data='الثامن')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📖 اختر الفصل الدراسي:", reply_markup=reply_markup)

# عند الضغط على زر الفصل أو المادة
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data in semester_data:
        subjects = semester_data[data]
        keyboard = [[InlineKeyboardButton(subject, callback_data="none")] for subject in subjects]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"📘 مواد الفصل {data}:", reply_markup=reply_markup)
    else:
        await query.edit_message_text("📌 سيتم إضافة المحتوى قريبًا إن شاء الله.")

# ======== Webhook + تشغيل السيرفر ========
if __name__ == '__main__':
    from flask import Flask, request
    from telegram.ext import Application

    app = Flask(__name__)

    TELEGRAM_TOKEN = "7863548329:AAGp1hEWdamJ0aKeRJVEWKyPAt1oUUHC_Hw"
    WEBHOOK_URL = "https://iuabot2-production.up.railway.app/webhook"

    telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CallbackQueryHandler(button_handler))

    @app.route("/webhook", methods=["POST"])
    def webhook():
        telegram_app.update_queue.put_nowait(Update.de_json(request.get_json(force=True), telegram_app.bot))
        return "ok"

    @app.route("/")
    def home():
        return "✅ البوت شغال باستخدام Webhook"

    @app.before_first_request
    def set_webhook():
        telegram_app.bot.set_webhook(url=WEBHOOK_URL)

    app.run(host="0.0.0.0", port=8000)
