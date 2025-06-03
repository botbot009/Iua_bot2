from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask, request
import os
import asyncio

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

semester_data = {
    "السابع": ["اقتصاد هندسي", "تصميم خرسانة 2", "تصميم فولاذ 1", "حساب كميات", "فكر إسلامي",
               "ميكانيكا تربة 2", "هندسة طرق 1", "هيدروليكا 1", "واقع إسلامي"],
    "الثامن": ["إدارة تشييد", "تصميم خرسانة 3", "تصميم فولاذ 2", "دراسات قرآنية",
               "هندسة بيئية", "هندسة طرق 2", "هيدروليكا 2"]
}

app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 الفصل السابع", callback_data='السابع')],
        [InlineKeyboardButton("📘 الفصل الثامن", callback_data='الثامن')]
    ]
    await update.message.reply_text("📖 اختر الفصل الدراسي:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    subjects = semester_data.get(data, [])
    keyboard = [[InlineKeyboardButton(subject, callback_data="none")] for subject in subjects]
    await query.edit_message_text(f"📘 مواد الفصل {data}:", reply_markup=InlineKeyboardMarkup(keyboard))

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok"

@app.route("/")
def home():
    return "✅ البوت يعمل باستخدام Webhook!"

async def main():
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Webhook تم تعيينه")
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    asyncio.run(main())
