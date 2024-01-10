#!/bin/bash

# Define the log file path
LOG_PATH="application.log"

# Extract the last 5 lines before the last "ERROR"
MESSAGE=$(grep -n "ERROR" "$LOG_PATH" | tail -n1 | cut -d: -f1 | xargs -I{} awk "NR>={}-5 && NR<={}" "$LOG_PATH")

# Check if MESSAGE is not empty
if [ -n "$MESSAGE" ]; then
    # Send the message using your Telegram notification script
    /etc/monit/telegram_notify.sh "`$MESSAGE`"
fi