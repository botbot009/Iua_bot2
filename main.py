from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from flask import Flask, request

# إعدادات البوت
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)

# بيانات الفصول
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

# بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 الفصل السابع", callback_data='السابع')],
        [InlineKeyboardButton("📘 الفصل الثامن", callback_data='الثامن')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📖 اختر الفصل الدراسي:", reply_markup=reply_markup)

# الضغط على زر
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data in semester_data:
        buttons = [[InlineKeyboardButton(subject, callback_data="none")] for subject in semester_data[data]]
        markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(f"📘 مواد الفصل {data}:", reply_markup=markup)
    else:
        await query.edit_message_text("📌 سيتم إضافة المحتوى لاحقًا.")

# تطبيق البوت
from telegram.ext import Application
telegram_app = ApplicationBuilder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))

# إعداد Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok"

@app.route("/")
def home():
    return "✅ البوت يعمل بنجاح"

@app.before_first_request
def set_webhook():
    telegram_app.bot.set_webhook(url=WEBHOOK_URL)

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")
