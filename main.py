from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask, request
import os, asyncio

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

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

# Flask + Telegram bot
app = Flask(__name__)
from telegram.ext import Application
telegram_app = ApplicationBuilder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start := lambda u, c: u.message.reply_text("📖 اختر الفصل الدراسي:", reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton("📚 الفصل السابع", callback_data='السابع')],
    [InlineKeyboardButton("📘 الفصل الثامن", callback_data='الثامن')]
]))))
telegram_app.add_handler(CallbackQueryHandler(lambda u, c: u.callback_query.edit_message_text(
    f"📘 مواد الفصل {u.callback_query.data}:", 
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(s, callback_data="none")] for s in semester_data.get(u.callback_query.data, ["لا توجد بيانات"])])
) if u.callback_query.data in semester_data else u.callback_query.edit_message_text("📌 سيتم إضافة المحتوى لاحقًا.")))

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok"

@app.route("/")
def home():
    return "✅ البوت يعمل الآن باستخدام Webhook!"

async def set_webhook():
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Webhook تم تعيينه:", WEBHOOK_URL)

if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(port=8000, host="0.0.0.0")
