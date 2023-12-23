import json
import os
import random

phrases = []

class Config:

    @staticmethod
    def get_telegram_token():
        return os.environ.get('TELEGRAM_TOKEN', 'default_telegram_token')

    @staticmethod
    def get_google_service_file():
        return os.environ.get('GOOGLE_SERVICE_FILE', 'default_service_file')

    @staticmethod
    def get_generic_error():
        global phrases

        if not phrases:
            with open('phrases.json', 'r', encoding='utf-8') as file:
                phrases = json.load(file)

        return random.choice(phrases)
