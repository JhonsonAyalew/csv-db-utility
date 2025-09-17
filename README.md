# Telegram Report Delivery Bot

A Python automation bot that generates daily reports (CSV/Excel/PDF) and delivers them directly to your Telegram chat.  

This bot is perfect for businesses, analysts, or e-commerce shops that want **automated report delivery** without checking dashboards manually.

---

## Features

- 📊 **Generate Reports**
  - Pull data from CSV, Excel, or APIs
  - Scrape websites (prices, jobs, news, etc.)
  - Generate summary statistics (totals, averages, trends)

- 📲 **Telegram Delivery**
  - Send reports and messages to a specific user or group
  - Supports text summaries + file attachments

- ⏰ **Custom Scheduling**
  - Schedule daily reports at any time via Telegram input
  - Users can type the time in HH:MM format (24h)

- 📄 **Report Formats**
  - Export to CSV, Excel (.xlsx), or PDF

- 🔄 **Fully Automated**
  - Uses APScheduler for daily scheduled tasks
  - Async handling for smooth Telegram messaging

---

## Tech Stack

- Python 3
- [Pandas](https://pandas.pydata.org/) – data processing
- [python-telegram-bot](https://python-telegram-bot.org/) – Telegram API integration
- [APScheduler](https://apscheduler.readthedocs.io/) – scheduling daily reports
- [openpyxl / fpdf](https://openpyxl.readthedocs.io/) – Excel/PDF generation

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/YOUR_USERNAME/csv-db-utility.git
cd csv-db-utility
