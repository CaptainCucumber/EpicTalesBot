import os

class Config:

    @staticmethod
    def get_telegram_token():
        return os.environ.get('TELEGRAM_TOKEN', 'default_telegram_token')

    @staticmethod
    def get_open_api_key():
        return os.environ.get('OPENAI_API_KEY', 'default_oepn_api_key')
