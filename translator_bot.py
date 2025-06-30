import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from deep_translator import GoogleTranslator

# Отримуємо токен з середовища
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Якщо токен не вказано — програма зупиниться з помилкою
import os
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("❌ Не знайдено токен бота! Додай змінну BOT_TOKEN у Railway.")

async def translate_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Перевіряємо, чи команда /translate є відповіддю на якесь повідомлення
    if not update.message or not update.message.reply_to_message:
        await update.message.reply_text("🔁 Напиши /translate у відповідь на повідомлення, яке потрібно перекласти.")
        return

    original_text = update.message.reply_to_message.text
    if not original_text:
        await update.message.reply_text("⚠️ Не знайдено текст для перекладу.")
        return

    try:
        translated = GoogleTranslator(source='auto', target='uk').translate(original_text)
        await update.message.reply_text(
            f"📥 *Переклад українською*:\n`{translated}`",
            parse_mode='Markdown'
        )
    except Exception:
        await update.message.reply_text("⚠️ Сталася помилка під час перекладу.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("translate", translate_reply))

    print("✅ Бот запущено. Очікую команду /translate у відповідь на повідомлення...")
    app.run_polling()
