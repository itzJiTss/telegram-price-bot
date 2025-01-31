import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests

# Your bot API token
application = Application.builder().token("7582488141:AAFgH0iI85zTnyMkhBFK4UVF7zlSmmitoOw").build()

# Function to fetch price data
def fetch_price():
    url = 'https://api.example.com/price'
    response = requests.get(url)
    data = response.json()
    return data['sell']  # Assuming the price is under 'sell' in the response

# Command handler for /price
async def price(update, context):
    price = fetch_price()
    keyboard = [
        [InlineKeyboardButton("Refresh", callback_data='refresh')],
        [InlineKeyboardButton("Delete", callback_data='delete')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"The current price is: {price} INR", reply_markup=reply_markup)

# Callback handler for button presses
async def button(update, context):
    query = update.callback_query
    if query.data == 'refresh':
        price = fetch_price()
        await query.edit_message_text(text=f"The current price is: {price} INR")
    elif query.data == 'delete':
        await query.edit_message_text(text="Message deleted.")
        await query.message.delete()

# Main function to set up the bot
async def main():
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot
    await application.run_polling()

# Run the bot with the asyncio loop
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
