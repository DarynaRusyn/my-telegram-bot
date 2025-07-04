import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from deep_translator import GoogleTranslator

BOT_TOKEN = "7619972145:AAGo6bGzkS5dkyPYd_Qw2xQ20RoqsH4gz20"
if not BOT_TOKEN:
    raise ValueError("❌ Bot token not found! Please set BOT_TOKEN.")

LANG_NAMES = {
    'uk': 'Ukrainian',
    'en': 'English',
    'es': 'Spanish',
    'mg': 'Malagasy'
}

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE, target_lang: str):
    message = update.message
    if not message or not message.reply_to_message:
        await message.reply_text(
            f"🔁 Please reply to a message with /{target_lang} to translate."
        )
        return

    original_text = message.reply_to_message.text
    if not original_text:
        await message.reply_text("⚠️ No text found to translate.")
        return

    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(original_text)
        await message.reply_text(
            f"📥 *Translated into {LANG_NAMES[target_lang]}*:\n{translated}",
            parse_mode='Markdown'
        )
    except Exception as e:
        print("Translation error:", e)
        await message.reply_text("⚠️ An error occurred during translation.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Додаємо командні хендлери для кожної мови
    for lang_code in LANG_NAMES.keys():
        app.add_handler(CommandHandler(lang_code, lambda u, c, lc=lang_code: translate(u, c, lc)))

    print("✅ Bot is running. Use /uk, /en, /es, or /mg in reply to a message.")
    app.run_polling()
