from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.ext import Application
from flask import Flask, request
import logging

# إعداد التوكن والرابط (مباشر)
TOKEN = "8034562422:AAFaIAmTNjUL4ya6MUnO4zHySMc77OPlgnQ"
WEBHOOK_URL = "https://iuabot2-production.up.railway.app/webhook"

# إعداد تسجيل الأخطاء
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

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

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 الفصل السابع", callback_data='السابع')],
        [InlineKeyboardButton("📘 الفصل الثامن", callback_data='الثامن')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📖 اختر الفصل الدراسي:", reply_markup=reply_markup)

# الضغط على الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    semester = query.data
    if semester in semester_data:
        buttons = [[InlineKeyboardButton(subject, callback_data="none")] for subject in semester_data[semester]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(text=f"📘 مواد الفصل {semester}:", reply_markup=reply_markup)
    else:
        await query.edit_message_text("📌 سيتم إضافة المحتوى لاحقًا.")

# إعداد التطبيق
app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))

# Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    telegram_app.update_queue.put_nowait(Update.de_json(request.get_json(force=True), telegram_app.bot))
    return "ok"

@app.route("/")
def home():
    return "✅ البوت يعمل الآن باستخدام Webhook!"

# تعيين Webhook بشكل غير متزامن
import asyncio
async def set_webhook():
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)

if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(port=8000, host="0.0.0.0")
