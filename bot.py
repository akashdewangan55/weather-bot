import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, Application, ContextTypes
from config import TELEGRAM_TOKEN, OPENWEATHER_API_KEY

app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! Send /weather <city> to get weather info.")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please specify a city.")
        return

    city = ' '.join(context.args)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    res = requests.get(url).json()

    if res.get("cod") != 200:
        await update.message.reply_text("❌ City not found!")
        return

    name = res["name"]
    temp = res["main"]["temp"]
    weather = res["weather"][0]["description"]
    await update.message.reply_text(f"🌆 City: {name}\n🌡️ Temp: {temp}°C\n🌤️ Condition: {weather.capitalize()}")

application = Application.builder().token(TELEGRAM_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("weather", weather))

@app.route('/')
def index():
    return "Bot is running."

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok"

if __name__ == '__main__':
    application.run_polling()
