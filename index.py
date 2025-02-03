import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TELEGRAM_TOKEN = '7582488141:AAFgH0iI85zTnyMkhBFK4UVF7zlSmmitoOw'  # Replace with your actual bot token

# Function to fetch and send price details
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://www.zebapi.com/api/v1/market/USDT-INR/ticker?group=singapore"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "sell" in data:
        pair = data.get("pair", "Unknown Pair")
        current_price = float(data.get("sell", "N/A"))  # Convert price to float
        high_24h = data.get("24hoursHigh", "N/A")
        low_24h = data.get("24hoursLow", "N/A")

        message = (
            f"🔹 **Pair:** {pair}\n"
            f"💰 **Current Price:** ₹{current_price}\n"
            f"📈 **24H High:** ₹{high_24h}\n"
            f"📉 **24H Low:** ₹{low_24h}"
        )

        await update.message.reply_text(message, parse_mode="Markdown")
    else:
        await update.message.reply_text("⚠️ Could not fetch price data.")

# Function to calculate the price * user input
async def calcu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the user provided a number
    if len(context.args) == 0:
        await update.message.reply_text("⚠️ Please provide a number. Example: `/calcu 100`", parse_mode="Markdown")
        return

    try:
        user_input = float(context.args[0])  # Convert user input to float

        # Fetch the latest price from the API
        url = "https://www.zebapi.com/api/v1/market/USDT-INR/ticker?group=singapore"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and "sell" in data:
            current_price = float(data['sell'])
            result = current_price * user_input  # Perform multiplication

            message = (
                f"💰 **Current Price:** ₹{current_price}\n"
                f"🔢 **Your Input:** {user_input}\n"
                f"🧮 **Calculated Value:** ₹{result:.2f}"  # Display result with 2 decimal places
            )

            await update.message.reply_text(message, parse_mode="Markdown")
        else:
            await update.message.reply_text("⚠️ Could not fetch price data.")
    
    except ValueError:
        await update.message.reply_text("⚠️ Invalid number. Please use: `/calcu 100`", parse_mode="Markdown")

# Main function to start the bot
def main():
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("calcu", calcu))  # ✅ Added new command

    application.run_polling()

# Run the bot
if __name__ == '__main__':
    main()
