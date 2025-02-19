import logging
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ChatMemberHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "7582488141:AAFgH0iI85zTnyMkhBFK4UVF7zlSmmitoOw"  # Replace with your bot token

# Store groups dynamically
group_chats = set()

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetch and send current USDT-INR price."""
    url = "https://www.zebapi.com/api/v1/market/USDT-INR/ticker?group=singapore"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "sell" in data:
        price = float(data["sell"])
        high = float(data["24hoursHigh"])
        low = float(data["24hoursLow"])
        message = f"🔹 Pair: USDT-INR\n💰 Current Price: ₹{price}\n📈 24H High: ₹{high}\n📉 24H Low: ₹{low}"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("❌ Could not fetch price data.")

async def calcu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Calculate value based on user input and current price."""
    try:
        amount = float(context.args[0])  # Get user input (e.g., /calcu 100)
        url = "https://www.zebapi.com/api/v1/market/USDT-INR/ticker?group=singapore"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and "sell" in data:
            price = float(data["sell"])
            total = price * amount
            message = f"💰 Current Price: ₹{price}\n🔢 Your Input: {amount}\n🧮 Calculated Value: ₹{total:.2f}"
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("❌ Could not fetch price data.")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Usage: /calcu <amount>\nExample: /calcu 100")

async def track_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Track new groups when the bot is added."""
    chat = update.chat
    if chat.type in ["group", "supergroup"]:
        group_chats.add(chat.id)
        logger.info(f"Added to group: {chat.title} (ID: {chat.id})")

async def send_price_updates(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send price updates to all groups every hour."""
    url = "https://www.zebapi.com/api/v1/market/USDT-INR/ticker?group=singapore"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "sell" in data:
        price = float(data["sell"])
        high = float(data["24hoursHigh"])
        low = float(data["24hoursLow"])
        message = f"🔹 Pair: USDT-INR\n💰 Current Price: ₹{price}\n📈 24H High: ₹{high}\n📉 24H Low: ₹{low}"

        for chat_id in group_chats:
            try:
                await context.bot.send_message(chat_id, message)
            except Exception as e:
                logger.warning(f"Could not send message to {chat_id}: {e}")

async def start_scheduled_task(application):
    """Start the hourly price update task."""
    while True:
        await send_price_updates(application)
        await asyncio.sleep(1800)  # Wait 1 hour before sending again

def main():
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("calcu", calcu))
    application.add_handler(ChatMemberHandler(track_group, ChatMemberHandler.CHAT_MEMBER))

    # Start background task for scheduled updates
    asyncio.create_task(start_scheduled_task(application))

    application.run_polling()

if __name__ == "__main__":
    main()
