from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from deep_translator import GoogleTranslator
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("❌ Не знайдено токен бота!")

LANG_NAMES = {'uk': 'українською', 'en': 'англійською', 'es': 'іспанською'}

# Автоматично реагує на будь-яке повідомлення-відповідь
async def auto_translate_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.reply_to_message:
        return

    original_text = message.reply_to_message.text
    if not original_text:
        return

    context.user_data["text_to_translate"] = original_text

    keyboard = [
        [
            InlineKeyboardButton("🇺🇦 Українська", callback_data='lang_uk'),
            InlineKeyboardButton("🇬🇧 Англійська", callback_data='lang_en'),
            InlineKeyboardButton("🇪🇸 Іспанська", callback_data='lang_es'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text("🔠 Обери мову для перекладу:", reply_markup=reply_markup)

# Обробка кнопок
async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang_code = query.data.split('_')[1]
    original_text = context.user_data.get("text_to_translate")

    if not original_text:
        await query.edit_message_text("⚠️ Немає тексту для перекладу.")
        return

    try:
        translated = GoogleTranslator(source='auto', target=lang_code).translate(original_text)
        await query.edit_message_text(
            f"📥 *Переклад {LANG_NAMES[lang_code]}*:\n{translated}",
            parse_mode='Markdown'
        )
    except Exception as e:
        print("Помилка:", e)
        await query.edit_message_text("⚠️ Сталася помилка під час перекладу.")

# Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Коли є відповідь на повідомлення — автоматично пропонує переклад
    app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, auto_translate_prompt))

    # Обробка натискань на кнопки
    app.add_handler(CallbackQueryHandler(handle_language_choice, pattern=r'^lang_'))

    print("✅ Бот запущено. Відповідай на повідомлення — і отримаєш кнопки для перекладу.")
    app.run_polling()
