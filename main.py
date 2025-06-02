from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from flask import Flask, request
from telegram.ext import Application

app = Flask(__name__)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎥 فيديوهات الاقتصاد", callback_data='eco_videos')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحباً 👋 اختر المحتوى:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'eco_videos':
        keyboard = [
            [InlineKeyboardButton("🎞️ Lecture 2", url="https://t.me/c/2646509467/4")],
            [InlineKeyboardButton("🎞️ Lecture 3", url="https://t.me/c/2646509467/5")],
            [InlineKeyboardButton("🔙 رجوع", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📹 فيديوهات اقتصاد هندسي:", reply_markup=reply_markup)

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))

@app.route("/webhook", methods=["POST"])
def webhook():
    telegram_app.update_queue.put_nowait(Update.de_json(request.get_json(force=True), telegram_app.bot))
    return "ok"

@app.route("/")
def home():
    return "✅ Webhook شغال"

@app.before_first_request
def setup_webhook():
    telegram_app.bot.set_webhook(url=WEBHOOK_URL)

app.run(host="0.0.0.0", port=8000)
