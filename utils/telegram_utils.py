#!/usr/bin/env python3
from telegram import Bot

# Fully async function
async def send_message(token, chat_id, text, file_path=None):
    bot = Bot(token=token)

    # Send text message
    await bot.send_message(chat_id=chat_id, text=text)

    # Send file if provided
    if file_path:
        with open(file_path, "rb") as f:
            await bot.send_document(chat_id=chat_id, document=f)
