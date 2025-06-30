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

if not BOT_TOKEN:
    raise ValueError("❌ Не знайдено токен бота! Додай змінну BOT_TOKEN у Railway.")

async def translate_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Друкуємо аргументи в консоль для налагодження
    print("Отримані аргументи:", context.args)

    # Перевірка, чи команда є відповіддю на повідомлення
    if not update.message or not update.message.reply_to_message:
        await update.message.reply_text(
            "🔁 Напиши /translate <lang> у відповідь на повідомлення, яке потрібно перекласти.\n"
            "Доступні мови: uk (українська), en (англійська), es (іспанська)"
        )
        return

    original_text = update.message.reply_to_message.text
    if not original_text:
        await update.message.reply_text("⚠️ Не знайдено текст для перекладу.")
        return

    # Отримуємо аргумент мови (за замовчуванням – 'uk')
    args = context.args
    target_lang = 'uk'
    if args:
        lang = args[0].lower()
        if lang in ['uk', 'en', 'es']:
            target_lang = lang
        else:
            await update.message.reply_text("⚠️ Невідома мова. Використовуйте одну з: uk, en, es.")
            return

    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(original_text)
        lang_names = {'uk': 'українською', 'en': 'англійською', 'es': 'іспанською'}
        await update.message.reply_text(
            f"📥 *Переклад {lang_names[target_lang]}*:\n{translated}",
            parse_mode='Markdown'
        )
    except Exception as e:
        print("Помилка при перекладі:", e)
        await update.message.reply_text("⚠️ Сталася помилка під час перекладу.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("translate", translate_reply))

    print("✅ Бот запущено. Очікую команду /translate у відповідь на повідомлення...")
    app.run_polling()
