import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram Bot Token
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Link Shortener API setup
SHORTLINK_API = 'https://api.shrtco.de/v2/shorten?url={}'
API_KEY = 'YOUR_SHORTLINK_API_KEY'

# Premium Users (List of User IDs who can access premium features)
PREMIUM_USERS = [123456789, 987654321]  # Example user IDs


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the File Sender Bot! Use /sendfile to get a file or /shorten <url> to shorten a link."
    )


# Send File Command
async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in PREMIUM_USERS:
        await update.message.reply_text("🚫 This feature is only available to premium users.")
        return

    # Replace with actual file path
    file_path = "path/to/your/file.ext"
    try:
        await update.message.reply_document(document=open(file_path, 'rb'))
        await update.message.reply_text("Here is your file!")
    except Exception as e:
        logger.error(f"Error sending file: {e}")
        await update.message.reply_text("❌ Error: Could not send the file.")


# Shorten Link Command
async def shorten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /shorten <URL>")
        return

    url_to_shorten = context.args[0]
    try:
        response = requests.get(SHORTLINK_API.format(url_to_shorten), headers={'Authorization': f'Bearer {API_KEY}'})
        data = response.json()

        if data.get('ok'):
            short_url = data['result']['full_short_link']
            await update.message.reply_text(f"🔗 Shortened Link: {short_url}")
        else:
            await update.message.reply_text("❌ Failed to shorten the link. Please try again later.")
    except Exception as e:
        logger.error(f"Error shortening link: {e}")
        await update.message.reply_text("❌ Error: Could not shorten the link.")


def main():
    # Initialize the bot
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sendfile", send_file))
    application.add_handler(CommandHandler("shorten", shorten, filters=filters.TEXT))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
