import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from deep_translator import GoogleTranslator

# Токен з середовища
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("❌ Не знайдено токен бота! Додай змінну BOT_TOKEN у Railway.")

# Словник для назв мов
LANG_NAMES = {'uk': 'українською', 'en': 'англійською', 'es': 'іспанською'}

# Команда /translate
async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message or not message.reply_to_message:
        await message.reply_text("🔁 Напиши /translate у відповідь на повідомлення, яке потрібно перекласти.")
        return

    original_text = message.reply_to_message.text
    if not original_text:
        await message.reply_text("⚠️ Не знайдено текст для перекладу.")
        return

    # Зберігаємо ID повідомлення з текстом, який треба перекласти
    context.user_data["text_to_translate"] = original_text

    # Створюємо кнопки мов
    keyboard = [
        [
            InlineKeyboardButton("🇺🇦 Українська", callback_data='lang_uk'),
            InlineKeyboardButton("🇬🇧 Англійська", callback_data='lang_en'),
            InlineKeyboardButton("🇪🇸 Іспанська", callback_data='lang_es'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text("🔠 Обери мову для перекладу:", reply_markup=reply_markup)

# Обробка натискання кнопок
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
        print("❌ Помилка перекладу:", e)
        await query.edit_message_text("⚠️ Сталася помилка під час перекладу.")

# Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("translate", translate_command))
    app.add_handler(CallbackQueryHandler(handle_language_choice, pattern=r'^lang_'))

    print("✅ Бот запущено. Очікую команду /translate у відповідь на повідомлення...")
    app.run_polling()
