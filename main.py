from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# ⚠️ تنبيه: لا تضع التوكن هكذا في الإنتاج، فقط للتجربة
TOKEN = "7888413063:AAFpDgT9WsbrP8kMcNkyQ61Xcp3ClhDMEFs"

# إعداد تسجيل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 الفصل السابع", callback_data='السابع')],
        [InlineKeyboardButton("📘 الفصل الثامن", callback_data='الثامن')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📖 اختر الفصل الدراسي:", reply_markup=reply_markup)

# عند الضغط على زر
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
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 البوت يعمل الآن باستخدام polling ...")
    app.run_polling()
