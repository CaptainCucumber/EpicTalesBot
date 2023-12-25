import os


class Config:
    WHITELISTED_GROUPS = [-4084203084, -809833778, -1002093229047]

    def __init__(self, env: os.environ):
        self._env = env

    def get_telegram_token(self):
        return self._env['TELEGRAM_TOKEN']

    def get_google_service_file(self):
        return self._env['GOOGLE_SERVICE_FILE']
    
    def get_open_ai_key(self):
        return self._env['OPENAI_KEY']
