#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Read environment variables from config.env
source config.env

.venv/bin/python ./bot/main.py