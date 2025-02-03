import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = '7582488141:AAFgH0iI85zTnyMkhBFK4UVF7zlSmmitoOw'  # Replace with your actual bot token

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetches and sends the latest USDT-INR price"""
    url = "https://www.zebapi.com/api/v1/market/USDT-INR/ticker?group=singapore"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and "sell" in data:
        price = float(data['sell'])
        message = f"🔹 Pair: USDT-INR\n💰 Current Price: ₹{price:.2f}\n📈 24H High: ₹{data['24hoursHigh']}\n📉 24H Low: ₹{data['24hoursLow']}"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Could not fetch price data.")

async def calcu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Multiplies user input by the latest USDT-INR price"""
    if not context.args:
        await update.message.reply_text("Usage: /calcu <amount>\nExample: /calcu 100")
        return

    try:
        amount = float(context.args[0])  # Get user input
    except ValueError:
        await update.message.reply_text("Please enter a valid number.\nExample: /calcu 100")
        return

    url = "https://www.zebapi.com/api/v1/market/USDT-INR/ticker?group=singapore"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and "sell" in data:
        price = float(data['sell'])
        total = price * amount
        message = f"💰 Current Price: ₹{price:.2f}\n📊 Calculation: {amount} × {price:.2f} = ₹{total:.2f}"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Could not fetch price data.")

def main():
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("calcu", calcu))  # Adding /calcu command

    application.run_polling()

if __name__ == '__main__':
    main()
