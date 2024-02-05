import os

import toml


class Config:
    BLACKLISTED_GROUPS = []
    _instance = None

    def __new__(cls, config_path):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            with open(config_path, "r") as file:
                cls._instance.config = toml.load(file)
        return cls._instance

    def get_telegram_token(self):
        return self.config["telegram"]["bot_token"]

    def get_open_ai_key(self):
        return self.config["openai"]["api_key"]

    def get_log_path(self):
        return self.config["epictalesbot"].get("logs_path", "/var/log/epictales")

    def get_metrics_path(self):
        return self.config["epictalesbot"].get("metrics_path", "/var/log/epictales")

    def get_google_cloud_creds_file(self):
        return self.config["google"]["cloud"]["credentials_file"]

    def get_environment(self):
        return self.config["epictalesbot"].get("environment", "prod")

    def get_aws_region(self):
        return self.config["aws"]["region"]

    def get_aws_access_key_id(self):
        return self.config["aws"]["credentials"]["aws_access_key_id"]

    def get_aws_secret_access_key(self):
        return self.config["aws"]["credentials"]["aws_secret_access_key"]


config = Config(".epictalesbot.toml")
