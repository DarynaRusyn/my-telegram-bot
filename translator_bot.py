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

async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.reply_to_message:
        await message.reply_text(
            "🔁 Please reply to a message with /translate <language_code>.\n"
            "Available languages: uk, en, es, mg"
        )
        return

    original_text = message.reply_to_message.text
    if not original_text:
        await message.reply_text("⚠️ No text found to translate.")
        return

    args = context.args
    if not args or args[0].lower() not in LANG_NAMES:
        await message.reply_text(
            "⚠️ Unknown or missing language code.\n"
            "Please use one of: uk, en, es, mg"
        )
        return

    target_lang = args[0].lower()

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

    app.add_handler(CommandHandler("translate", translate_command))

    print("✅ Bot is running. Use /translate <language_code> in reply to a message.")
    app.run_polling()
