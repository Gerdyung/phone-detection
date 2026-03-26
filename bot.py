import phonenumbers
import os
from phonenumbers import geocoder, carrier
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

TOKEN = os.getenv('8218215870:AAF_btuAd-D6U5cFgdVhDnv9v1NOCz_IR8w')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send a phone number!')

async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        number = update.message.text.strip()

        # Ensure number has country code
        pn = phonenumbers.parse(number, None)

        if not phonenumbers.is_valid_number(pn):
            await update.message.reply_text("Invalid phone number.")
            return

        country = geocoder.description_for_number(pn, 'en')
        carrier_name = carrier.name_for_number(pn, 'en')

        await update.message.reply_text(
            f"Country: {country}\nCarrier: {carrier_name}"
        )

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# 🔧 Increase timeout (important for your error)
request = HTTPXRequest(connect_timeout=20, read_timeout=20)

app = ApplicationBuilder().token(TOKEN).request(request).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_info))

print("Bot is running...")
app.run_polling()

