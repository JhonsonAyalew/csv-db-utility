#!/usr/bin/env python3
from apscheduler.schedulers.blocking import BlockingScheduler
from report_generator import generate_report
from utils.telegram_utils import send_message_sync

# Telegram bot config
TOKEN = "7408634674:AAE3gJdXaMJNiRyqfQCwtY-rMjFvG5uSdaY"
CHAT_ID = "1288895410"

def job():
    summary, report_file = generate_report()
    send_message_sync(TOKEN, CHAT_ID, summary, report_file)
    print("Report sent successfully!")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    
    # Schedule daily at 08:00 AM
    scheduler.add_job(job, 'cron', hour=8, minute=0)
    
    print("Scheduler started. Reports will be sent daily at 08:00 AM.")
    scheduler.start()
