from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import asyncio

# إعدادات البوت
TOKEN = os.environ.get("BOT_TOKEN")

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

# تشغيل البوت باستخدام polling
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ البوت يعمل باستخدام polling ...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
