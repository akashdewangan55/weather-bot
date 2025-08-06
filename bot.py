import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Set your bot token
BOT_TOKEN = os.environ.get("BOT_TOKEN") or "7710160278:AAEuNEnQOfIz2zNMWGWLLNCiNwiBn_4h-gw"
WEBHOOK_URL = "https://weather-bot-mk58.onrender.com/webhook"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

# Basic command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Your bot is working.")

application.add_handler(CommandHandler("start", start))

# Telegram webhook endpoint
@app.route('/webhook', methods=['POST'])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
    return "OK"

# Root endpoint
@app.route("/", methods=['GET'])
def index():
    return "Bot is running."

# Set webhook when starting app
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook set to {WEBHOOK_URL}")

if __name__ == "__main__":
    import asyncio

    async def main():
        await set_webhook()
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

    asyncio.run(main())