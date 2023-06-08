#!/bin/bash

# Run bot every 30 minutes in infinite loop
while true; do
    # Run your command here
    poetry run openhomeautomationbot

    echo "Sleeping..."
    # Wait for 30 minutes
    sleep 1800
    echo "Sleep done"
done
