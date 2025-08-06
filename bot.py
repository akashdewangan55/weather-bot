import os
import requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, OPENWEATHER_API_KEY

# Flask app
app = Flask(__name__)

# Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)

# Telegram Application (without run_polling)
application = Application.builder().token(TELEGRAM_TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Use /weather <city> to get weather info.")

# /weather command
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please provide a city name.")
        return

    city = ' '.join(context.args)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    res = requests.get(url).json()

    if res.get("cod") != 200:
        await update.message.reply_text("❌ City not found.")
        return

    name = res["name"]
    temp = res["main"]["temp"]
    desc = res["weather"][0]["description"]
    await update.message.reply_text(f"🌆 {name}\n🌡️ {temp}°C\n☁️ {desc.capitalize()}")

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("weather", weather))

# Root route
@app.route('/')
def home():
    return '🌐 Webhook bot is running!'

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return 'OK'

# Set webhook when app starts
@app.before_first_request
def set_webhook():
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    bot.set_webhook(webhook_url)

# Start Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))