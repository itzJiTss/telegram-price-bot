from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.ext import CallbackContext

# Function to fetch the price (replace with your actual API call)
async def fetch_price():
    # Example price fetching logic
    return "94.700000"  # Example price value

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply("Welcome! Type /price to get the current price.")

# Price command handler (with buttons)
async def price_with_buttons(update: Update, context: CallbackContext):
    # Inline buttons for "Refresh" and "Delete"
    refresh_button = InlineKeyboardButton("Refresh Price", callback_data="refresh_price")
    delete_button = InlineKeyboardButton("Delete Price", callback_data="delete_price")
    keyboard = InlineKeyboardMarkup([[refresh_button, delete_button]])

    price = await fetch_price()  # Fetch price from the API
    message = await update.message.reply(f"The current price is: {price}", reply_markup=keyboard)

    # Store the message ID in context for later use (if needed)
    context.user_data["price_message_id"] = message.message_id

# Callback function for the "Refresh" button
async def refresh_price(update: Update, context: CallbackContext):
    price = await fetch_price()  # Fetch updated price
    await update.callback_query.answer()  # Acknowledge the button click
    await update.callback_query.edit_message_text(f"The current price is: {price}")  # Update the message

# Callback function for the "Delete" button
async def delete_price(update: Update, context: CallbackContext):
    await update.callback_query.answer()  # Acknowledge the button click
    # Delete the message that contains the price and buttons
    await update.callback_query.message.delete()

# Main function to set up the bot
async def main():
    application = Application.builder().token("7582488141:AAFgH0iI85zTnyMkhBFK4UVF7zlSmmitoOw").build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price_with_buttons))  # Command to show price with buttons
    
    # Callback handlers for buttons
    application.add_handler(CallbackQueryHandler(refresh_price, pattern="refresh_price"))
    application.add_handler(CallbackQueryHandler(delete_price, pattern="delete_price"))
    
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
