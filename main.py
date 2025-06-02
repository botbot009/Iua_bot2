from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# مواد الفصول
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

# دالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 الفصل السابع", callback_data='السابع')],
        [InlineKeyboardButton("📘 الفصل الثامن", callback_data='الثامن')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر الفصل الدراسي:", reply_markup=reply_markup)

# دالة الفيديوهات للاقتصاد
async def show_eco_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎞️ Lecture 2", url="https://t.me/c/2646509467/4")],
        [InlineKeyboardButton("🎞️ Lecture 3", url="https://t.me/c/2646509467/5")],
        [InlineKeyboardButton("🎞️ Lecture 4", url="https://t.me/c/2646509467/6")],
        [InlineKeyboardButton("🎞️ Lecture 5", url="https://t.me/c/2646509467/7")],
        [InlineKeyboardButton("🎞️ Lecture 6", url="https://t.me/c/2646509467/9")],
        [InlineKeyboardButton("🎞️ Lecture 7", url="https://t.me/c/2646509467/8")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="اقتصاد هندسي")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text("🎥 فيديوهات مادة الاقتصاد الهندسي:", reply_markup=reply_markup)

# دالة اختيار المواد والأزرار الفرعية
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "السابع" or data == "الثامن":
        subjects = semester_data.get(data, [])
        keyboard = [[InlineKeyboardButton(f"📘 {subject}", callback_data=subject)] for subject in subjects]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"📖 مواد الفصل {data}:", reply_markup=reply_markup)

    elif data == "اقتصاد هندسي":
        keyboard = [
            [InlineKeyboardButton("📄 ملفات", callback_data="eco_files")],
            [InlineKeyboardButton("🎥 فيديوهات", callback_data="eco_videos")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="السابع")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 اختر نوع المحتوى لمادة الاقتصاد الهندسي:", reply_markup=reply_markup)

    elif data == "eco_videos":
        await show_eco_videos(update, context)

    elif data == "eco_files":
        await query.edit_message_text("📄 ملفات الاقتصاد الهندسي:\n\n- Lecture 1 PDF\n- Lecture 2 PDF\n- Lecture 3 PDF\n(📌 سيتم التحديث لاحقًا)")

# ========= تشغيل Webhook ===========
if __name__ == '__main__':
    from telegram.ext import Application
    from flask import Flask, request

    app = Flask(__name__)
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # تأكد من تعيينها في Railway
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")        # تأكد من تعيينها في Railway

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
    def setup_webhook():
        telegram_app.bot.set_webhook(url=WEBHOOK_URL)

    app.run(host="0.0.0.0", port=8000)
