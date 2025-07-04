import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from deep_translator import GoogleTranslator

# 🔐 Insert your token here
BOT_TOKEN = "your_bot_token_here"
if not BOT_TOKEN:
    raise ValueError("❌ Bot token not found! Please set BOT_TOKEN.")

# Supported languages
LANG_NAMES = {
    'uk': 'Ukrainian',
    'en': 'English',
    'es': 'Spanish',
    'mg': 'Malagasy'
}

# Show language selection buttons when user replies to a message
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
            InlineKeyboardButton("🇺🇦 Ukrainian", callback_data='lang_uk'),
            InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
        ],
        [
            InlineKeyboardButton("🇪🇸 Spanish", callback_data='lang_es'),
            InlineKeyboardButton("🇲🇬 Malagasy", callback_data='lang_mg'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text("🌐 Select the target language for translation:", reply_markup=reply_markup)

# Handle language button clicks
async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang_code = query.data.split('_')[1]
    original_text = context.user_data.get("text_to_translate")

    if not original_text:
        await query.edit_message_text("⚠️ No text found to translate.")
        return

    try:
        translated = GoogleTranslator(source='auto', target=lang_code).translate(original_text)
        await query.edit_message_text(
            f"📥 *Translated into {LANG_NAMES[lang_code]}*:\n{translated}",
            parse_mode='Markdown'
        )
    except Exception as e:
        print("Translation error:", e)
        await query.edit_message_text("⚠️ An error occurred while translating.")

# Run the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, auto_translate_prompt))
    app.add_handler(CallbackQueryHandler(handle_language_choice, pattern=r'^lang_'))

    print("✅ Bot is running. Reply to any message to get translation options.")
    app.run_polling()

