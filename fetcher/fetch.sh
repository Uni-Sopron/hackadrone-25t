#!/bin/bash

# Set variables
URL="https://hackadrone.gazd.info/admin/status"

# Get directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUTPUT_DIR="${SCRIPT_DIR}/logs"
LOG_FILE="${SCRIPT_DIR}/fetch_log.txt"

# Create timestamp for filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="${OUTPUT_DIR}/data_${TIMESTAMP}.json"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Fetch the JSON and save it to the timestamped file
curl -s "$URL" > "$OUTPUT_FILE"

# Log the result
if [ $? -eq 0 ]; then
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] Successfully fetched JSON and saved to $OUTPUT_FILE" >> "$LOG_FILE"
else
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] Failed to fetch JSON" >> "$LOG_FILE"
fi
