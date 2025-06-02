import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

BOT_TOKEN = "7863548329:AAGp1hEWdamJ0aKeRJVEWKyPAt1oUUHC_Hw"

user_state = {}

semester_subjects = {
    "السمستر السابع": [
        "هندسة طرق 1", "هيدروليكا 1", "تصميم خرسانة 2", "حساب كميات",
        "ميكانيكيا تربة 2", "تصميم فولاذ 1", "اقتصاد هندسي",
        "فكر اسلامي", "واقع اسلامي"
    ],
    "السمستر الثامن": [
        "هندسة طرق 2", "هيدروليكا 2", "تصميم خرسانة 3", "إدارة تشييد",
        "تصميم فولاذ 2", "هندسة بيئية", "دراسات قرآنية"
    ]
}

# الرد على /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["السمستر السابع", "السمستر الثامن"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("👋 اختر السمستر:", reply_markup=markup)

# التعامل مع الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text in semester_subjects:
        user_state[user_id] = {"semester": text}
        keyboard = [[s] for s in semester_subjects[text]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text("📘 اختر المادة:", reply_markup=markup)

    elif user_id in user_state and "subject" not in user_state[user_id]:
        user_state[user_id]["subject"] = text
        await update.message.reply_text("📎 أرسل الملف الذي تريد رفعه.")

        sem_folder = "semester7" if "السابع" in user_state[user_id]["semester"] else "semester8"
        subject = user_state[user_id]["subject"]
        full_path = os.path.join(sem_folder, subject)
        os.makedirs(full_path, exist_ok=True)

        files = os.listdir(full_path)
        if files:
            await update.message.reply_text("📂 ملفات سابقة:")
            for file in files:
                with open(os.path.join(full_path, file), "rb") as f:
                    await update.message.reply_document(document=f, caption=file)
        else:
            await update.message.reply_text("📭 لا توجد ملفات حالياً.")

# رفع الملفات
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_state or "subject" not in user_state[user_id]:
        await update.message.reply_text("❗️اختر المادة أولاً باستخدام /start")
        return

    document = update.message.document
    file_name = document.file_name

    sem_folder = "semester7" if "السابع" in user_state[user_id]["semester"] else "semester8"
    subject = user_state[user_id]["subject"]
    save_dir = os.path.join(sem_folder, subject)
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, file_name)
    await document.download_to_drive(file_path)
    await update.message.reply_text(f"✅ تم حفظ الملف: {file_name}")

# keep alive باستخدام Flask
app_flask = Flask("")

@app_flask.route("/")
def home():
    return "✅ البوت شغال"

def run():
    app_flask.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run).start()

# التشغيل الفعلي
def start_bot():
    keep_alive()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    start_bot()
