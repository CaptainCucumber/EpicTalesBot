import os


class Config:
    BLACKLISTED_GROUPS = []

    def __init__(self, env: os.environ):
        self._env = env

    def get_telegram_token(self):
        return self._env['TELEGRAM_TOKEN']
    
    def get_open_ai_key(self):
        return self._env['OPENAI_KEY']
