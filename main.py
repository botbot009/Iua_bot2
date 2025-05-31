
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# إعداد المواد حسب كل سمستر
semesters = {
    "📚 السمستر السابع": [
        "هندسة طرق 1", "هيدروليكا 1", "تصميم خرسانة 2",
        "حساب كميات", "ميكانيكيا تربة 2", "تصميم فولاذ 1",
        "اقتصاد هندسي", "فكر اسلامي", "واقع اسلامي"
    ],
    "📘 السمستر الثامن": [
        "هندسة طرق 2", "هيدروليكا 2", "تصميم خرسانة 3",
        "إدارة تشييد", "تصميم فولاذ 2", "هندسة بيئية",
        "دراسات قرآنية"
    ]
}

# حفظ حالة المستخدم: أي سمستر وأي مادة
user_state = {}

# إنشاء المجلدات عند التشغيل
for semester, subjects in semesters.items():
    folder = "semester7" if "السابع" in semester else "semester8"
    os.makedirs(folder, exist_ok=True)
    for subject in subjects:
        os.makedirs(os.path.join(folder, subject), exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton(s)] for s in semesters]
    await update.message.reply_text(
        "اختر السمستر:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # إذا اختار السمستر
    if text in semesters:
        user_state[user_id] = {"semester": text, "subject": None}
        keyboard = [[KeyboardButton(subj)] for subj in semesters[text]]
        await update.message.reply_text(
            f"اختر المادة من {text}:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    # إذا اختار المادة
    elif any(text in subjects for subjects in semesters.values()):
        if user_id in user_state and "semester" in user_state[user_id]:
            user_state[user_id]["subject"] = text
            await update.message.reply_text(f"✅ اخترت المادة: {text}. أرسل الآن الملف المراد رفعه.\n\n📂 أو اختر من الملفات الموجودة:")

            # عرض الملفات الحالية
            semester_folder = "semester7" if "السابع" in user_state[user_id]["semester"] else "semester8"
            subject_folder = user_state[user_id]["subject"]
            full_path = os.path.join(semester_folder, subject_folder)

            files = os.listdir(full_path)
            if files:
                for f in files:
                    file_path = os.path.join(full_path, f)
                    await update.message.reply_document(document=open(file_path, "rb"), caption=f)
            else:
                await update.message.reply_text("📭 لا توجد ملفات حالياً لهذه المادة.")
        else:
            await update.message.reply_text("❗ يرجى أولاً اختيار السمستر.")
    # إذا أرسل ملف
    elif update.message.document:
        state = user_state.get(user_id)
        if not state or not state.get("semester") or not state.get("subject"):
            await update.message.reply_text("❗ يرجى أولاً اختيار السمستر والمادة قبل رفع الملفات.")
            return

        semester_folder = "semester7" if "السابع" in state["semester"] else "semester8"
        subject_folder = state["subject"]
        full_path = os.path.join(semester_folder, subject_folder)

        # تحميل الملف
        file = await context.bot.get_file(update.message.document.file_id)
        file_name = update.message.document.file_name
        await file.download_to_drive(os.path.join(full_path, file_name))

        await update.message.reply_text(f"✅ تم رفع الملف بنجاح إلى: {state['subject']}")
    else:
        await update.message.reply_text("❓ يرجى اختيار مادة أو رفع ملف.")

if __name__ == '__main__':
    app = ApplicationBuilder().token("7562563139:AAHyVNiD835GHB6Erhkc_v7chTaNKaticvg").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    print("🤖 Bot is running...")
    from flask import Flask
from threading import Thread

app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot is alive!"

def run():
    app_flask.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

keep_alive()
    app.run_polling()
