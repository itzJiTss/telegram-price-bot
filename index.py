import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your Telegram bot token
TELEGRAM_TOKEN = '7582488141:AAFgH0iI85zTnyMkhBFK4UVF7zlSmmitoOw'

# /price command - Fetch and display the latest market price
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://www.zebapi.com/api/v1/market/USDT-INR/ticker?group=singapore"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "sell" in data:
        price = float(data['sell'])
        high_24h = float(data["24hoursHigh"])
        low_24h = float(data["24hoursLow"])

        await update.message.reply_text(
            f"🔹 Pair: USDT-INR\n"
            f"💰 Current Price: ₹{price:.2f}\n"
            f"📈 24H High: ₹{high_24h:.2f}\n"
            f"📉 24H Low: ₹{low_24h:.2f}"
        )
    else:
        await update.message.reply_text("Could not fetch price data.")

# /calcu command - Multiply fetched price with user input
async def calcu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a number. Example: /calcu 100")
        return

    try:
        multiplier = float(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid input. Please enter a valid number.")
        return

    url = "https://www.zebapi.com/api/v1/market/USDT-INR/ticker?group=singapore"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "sell" in data:
        price = float(data['sell'])
        result = multiplier * price

        await update.message.reply_text(
            f"💰 Current Price: ₹{price:.2f}\n"
            f"🔢 Your Input: {multiplier:.1f}\n"
            f"🧮 Calculated Value: ₹{result:.2f}"
        )
    else:
        await update.message.reply_text("Could not fetch price data.")

# Function to send periodic price updates
async def send_price_updates(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = YOUR_CHAT_ID  # Replace this with the actual chat ID where updates should be sent
    url = "https://www.zebapi.com/api/v1/market/USDT-INR/ticker?group=singapore"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "sell" in data:
        price = float(data['sell'])
        high_24h = float(data["24hoursHigh"])
        low_24h = float(data["24hoursLow"])

        message = (
            f"🔹 Pair: USDT-INR\n"
            f"💰 Current Price: ₹{price:.2f}\n"
            f"📈 24H High: ₹{high_24h:.2f}\n"
            f"📉 24H Low: ₹{low_24h:.2f}"
        )

        await context.bot.send_message(chat_id=chat_id, text=message)

# Main function to start the bot
def main():
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # ✅ Initialize JobQueue
    job_queue = application.job_queue
    job_queue.run_repeating(send_price_updates, interval=3600, first=10)

    # Add command handlers
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("calcu", calcu))

    # Start polling
    application.run_polling()

# Run the bot
if __name__ == '__main__':
    main()
