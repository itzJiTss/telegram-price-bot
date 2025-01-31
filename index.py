import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TELEGRAM_TOKEN = '7582488141:AAFgH0iI85zTnyMkhBFK4UVF7zlSmmitoOw'  # Replace with your Telegram bot token
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://www.zebapi.com/api/v1/market/USDT-INR/ticker?group=singapore"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and "sell" in data:
        price = data['sell']
        await update.message.reply_text(f"Current sell price: ₹{price}")
    else:
        await update.message.reply_text("Could not fetch price data.")
def main():
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("price", price))
    application.run_polling()

if __name__ == '__main__':
    main()
