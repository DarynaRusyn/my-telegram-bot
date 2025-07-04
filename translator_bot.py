import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from deep_translator import GoogleTranslator

# Отримуємо токен з середовища
BOT_TOKEN = os.getenv('BOT_TOKEN') or "тут_твій_токен"  # тимчасово можна вставити напряму

if not BOT_TOKEN:
    raise ValueError("❌ Не знайдено токен бота! Додай змінну BOT_TOKEN.")

# Основна команда для перекладу
async def translate_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.reply_to_message:
        await update.message.reply_text(
            "🔁 Напиши /translate <мова> у *відповідь* на повідомлення, яке потрібно перекласти.\n"
            "Доступні мови: `uk` (українська), `en` (англійська), `es` (іспанська), `mg` (малагасійська)",
            parse_mode='Markdown'
        )
        return

    original_text = update.message.reply_to_message.text
    if not original_text:
        await update.message.reply_text("⚠️ Не знайдено текст для перекладу.")
        return

    args = context.args
    target_lang = 'uk'
    allowed_langs = {
        'uk': 'українською',
        'en': 'англійською',
        'es': 'іспанською',
        'mg': 'малагасійською'
    }

    if args:
        selected_lang = args[0].lower()
        if selected_lang in allowed_langs:
            target_lang = selected_lang
        else:
            await update.message.reply_text("⚠️ Невідома мова. Обери: uk, en, es, mg.")
            return

    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(original_text)
        await update.message.reply_text(
            f"📥 *Переклад {allowed_langs[target_lang]}*:\n{translated}",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text("⚠️ Помилка під час перекладу.")
        print(f"Translation error: {e}")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("translate", translate_reply))
    print("✅ Бот запущено. Використовуй /translate у відповідь на повідомлення.")
    app.run_polling()
