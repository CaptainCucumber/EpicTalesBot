import json
import os
import random

phrases = []

class Config:

    @staticmethod
    def get_telegram_token():
        return os.environ.get('TELEGRAM_TOKEN', 'default_telegram_token')

    @staticmethod
    def get_open_api_key():
        return os.environ.get('OPENAI_API_KEY', 'default_oepn_api_key')

    @staticmethod
    def get_generic_error():
        global phrases

        if not phrases:
            with open('phrases.json', 'r', encoding='utf-8') as file:
                phrases = json.load(file)

        return random.choice(phrases)
