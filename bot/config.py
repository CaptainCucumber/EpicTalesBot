import os


WHITELISTED_GROUPS = [-4084203084, -809833778, -1002093229047]

class Config:
    @staticmethod
    def get_telegram_token():
        return os.environ.get('TELEGRAM_TOKEN', 'default_telegram_token')

    @staticmethod
    def get_google_service_file():
        return os.environ.get('GOOGLE_SERVICE_FILE', 'default_service_file')

