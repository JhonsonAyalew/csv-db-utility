#!/usr/bin/env python3
import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Bot
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from report_generator import generate_report
from apscheduler.schedulers.background import BackgroundScheduler

# ------------------------------
# Bot token
# ------------------------------
TOKEN = "8191854029:AAFdBYDf5wqAMXEXEubrzLfmsJubF6icm1w"

# ------------------------------
# Scheduler setup
# ------------------------------
scheduler = BackgroundScheduler()
scheduler.start()

# Track users entering custom schedule time
user_schedules = {}

# ------------------------------
# Async function to send messages and files
# ------------------------------
async def send_message(token, chat_id, text, file_path=None):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=text)
    if file_path:
        with open(file_path, "rb") as f:
            await bot.send_document(chat_id=chat_id, document=f)

# ------------------------------
# Generate inline keyboard
# ------------------------------
def get_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 Generate Today's Report", callback_data='generate')],
        [InlineKeyboardButton("⏰ Schedule Daily Report", callback_data='schedule')],
        [InlineKeyboardButton("ℹ️ About Bot", callback_data='about')],
    ]
    return InlineKeyboardMarkup(keyboard)

# ------------------------------
# /start command
# ------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        f"👋 Hello {update.effective_user.first_name}!\n"
        "I am your Report Delivery Bot.\n"
        "Choose an option below:"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_menu_keyboard())

# ------------------------------
# Callback for inline buttons
# ------------------------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    if query.data == 'generate':
        summary, report_file = generate_report()
        await send_message(context.bot.token, chat_id, summary, report_file)
        await query.edit_message_text(
            text="✅ Report generated! Choose an option:", 
            reply_markup=get_menu_keyboard()
        )

    elif query.data == 'schedule':
        await query.edit_message_text(
            text="Please enter the daily report time in HH:MM (24h format):"
        )
        user_schedules[chat_id] = {'waiting_for_time': True}

    elif query.data == 'about':
        await query.edit_message_text(
            text="📌 This bot automatically generates daily reports "
                 "and sends them directly to your Telegram.",
            reply_markup=get_menu_keyboard()
        )

# ------------------------------
# Handle text input for custom schedule
# ------------------------------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()

    if chat_id in user_schedules and user_schedules[chat_id].get('waiting_for_time'):
        try:
            hour, minute = map(int, text.split(":"))
            if 0 <= hour < 24 and 0 <= minute < 60:
                scheduler.add_job(
                    lambda: asyncio.run(send_report_daily(context.bot.token, chat_id)),
                    'cron',
                    hour=hour,
                    minute=minute,
                    id=str(chat_id),
                    replace_existing=True
                )
                user_schedules[chat_id]['waiting_for_time'] = False
                await update.message.reply_text(f"⏰ Daily report scheduled at {text}!", reply_markup=get_menu_keyboard())
            else:
                raise ValueError
        except:
            await update.message.reply_text("❌ Invalid time format. Please use HH:MM (24h).")

# ------------------------------
# Async function for scheduled daily report
# ------------------------------
async def send_report_daily(token, chat_id):
    summary, report_file = generate_report()
    await send_message(token, chat_id, summary, report_file)

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Bot is running...")
    app.run_polling()
