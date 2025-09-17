#!/usr/bin/env python3
import pandas as pd
from datetime import datetime
import os

REPORTS_DIR = "reports"
DATA_FILE = "data/sample_data.csv"

def generate_report():
    # Load data
    df = pd.read_csv(DATA_FILE)

    # Example summary
    average_price = df['price'].mean()
    most_expensive_product = df.loc[df['price'].idxmax(), 'name']

    # Prepare report filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    report_file = f"{REPORTS_DIR}/price_report_{date_str}.xlsx"

    # Save Excel report
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    df.to_excel(report_file, index=False)

    # Return summary for Telegram message
    summary = (
        f"📊 Daily Price Report\n"
        f"Average Price: ${average_price:.2f}\n"
        f"Most Expensive Product: {most_expensive_product}\n"
        f"File: {report_file}"
    )
    return summary, report_file

if __name__ == "__main__":
    summary, report_file = generate_report()
    print(summary)
