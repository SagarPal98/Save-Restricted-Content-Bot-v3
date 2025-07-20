from aiogram import Bot, Dispatcher, types
import asyncio
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! Bot is working.")

async def start_bot():
    print("Starting test bot...", flush=True)
    await dp.start_polling()

if __name__ == "__main__":
    import threading
    from flask import Flask
    
    app = Flask(__name__)

    @app.route("/")
    def welcome():
        return "Hello Flask"

    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))).start()

    asyncio.run(start_bot())
