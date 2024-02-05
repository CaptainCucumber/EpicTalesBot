import os

import toml


class Config:
    BLACKLISTED_GROUPS = []

    def __init__(self, config_path):
        with open(config_path, "r") as file:
            self.config = toml.load(file)

    def get_telegram_token(self):
        return self.config["telegram"]["bot_token"]

    def get_open_ai_key(self):
        return self.config["openai"]["api_key"]

    def get_log_path(self):
        return self.config["epictalesbot"].get("logs_path", "/var/log/epictales")

    def get_metrics_path(self):
        return self.config["epictalesbot"].get("metrics_path", "/var/log/epictales")

    def get_google_cloud_creds_file(self):
        return self.config["google.cloud"]["credentials_file"]

    def get_environment(self):
        return self.config["epictalesbot"].get("environment", "prod")

    def get_aws_environment(self):
        return self.config["aws"].get("environment")

    def get_aws_access_key_id(self):
        return self.config["aws.credentials"]["aws_access_key_id"]

    def get_aws_secret_access_key(self):
        return self.config["aws.credentials"]["aws_secret_access_key"]


config_path = "./.epictalesbot.toml"
config = Config(os.environ)
