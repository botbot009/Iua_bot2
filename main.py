from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, Application

import os

app = Flask(__name__)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# handlers هنا تضيف start و button_handler مثلاً
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
def setup_webhook():
    telegram_app.bot.set_webhook(url=WEBHOOK_URL)

app.run(host="0.0.0.0", port=8000)
