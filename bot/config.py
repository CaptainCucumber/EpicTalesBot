import os


class Config:
    BLACKLISTED_GROUPS = []

    def __init__(self, env: os.environ):
        self._env = env

    def get_telegram_token(self):
        return self._env["TELEGRAM_TOKEN"]

    def get_open_ai_key(self):
        return self._env["OPENAI_KEY"]

    def get_log_path(self):
        return self._env.get("EPICTALES_LOG_PATH", "/var/log/epictales")

    def get_metrics_path(self):
        return self._env.get("EPICTALES_METRICS_PATH", "/var/log/epictales")

    def get_message_queue_url(self):
        return self._env["MESSAGE_QUEUE_URL"]

    def get_google_cloud_creds_file(self):
        return self._env["GOOGLE_APPLICATION_CREDENTIALS"]

    def get_environment(self):
        return self._env.get("EPICTALES_ENVIRONMENT", "prod")


config = Config(os.environ)
