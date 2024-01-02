#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Read environment variables from config.env
source config.env

# Compile .po files to .mo files for localization
function compile_locales() {
    for lang in bot/locales/*/LC_MESSAGES; do
        msgfmt "$lang"/*.po -o "$lang"/epictales.mo
    done
}

# Call the compile_locales function
compile_locales

# Run the Python application
.venv/bin/python ./bot/main.py
