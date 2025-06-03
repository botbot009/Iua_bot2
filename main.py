import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

# إعداد المتغيرات
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # مثال: https://xxxxxx.up.railway.app/webhook

# تحقق من التوكن
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN غير موجود في المتغيرات البيئية")

# بيانات المواد
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

# Flask app
app = Flask(__name__)

# Telegram App
telegram_app = Application.builder().token(TOKEN).build()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 الفصل السابع", callback_data='السابع')],
        [InlineKeyboardButton("📘 الفصل الثامن", callback_data='الثامن')]
    ]
    await update.message.reply_text("📖 اختر الفصل الدراسي:", reply_markup=InlineKeyboardMarkup(keyboard))

# عند اختيار المواد
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data in semester_data:
        buttons = [[InlineKeyboardButton(subject, callback_data="none")] for subject in semester_data[data]]
        await query.edit_message_text(f"📘 مواد الفصل {data}:", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await query.edit_message_text("📌 سيتم إضافة المحتوى لاحقًا.")

# تسجيل الهاندلرات
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok"

# فحص البوت
@app.route("/", methods=["GET"])
def home():
    return "✅ البوت يعمل على Railway"

# تشغيل البوت وتعيين الـ Webhook
async def main():
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Webhook set")

# إعداد الـ webhook عند التشغيل
@app.before_first_request
def activate_webhook():
    loop = asyncio.get_event_loop()
    loop.create_task(main())

# تشغيل الخادم
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
