#!/bin/bash

# Run bot every 30 minutes in infinite loop
while true; do
    # Run your command here
    poetry run openhomeautomationbot

    # Wait for 30 minutes
    sleep 1800
done
