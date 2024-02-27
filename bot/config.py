import toml


class Config:
    _instance = None

    def __new__(cls, config_path):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            with open(config_path, "r") as file:
                cls._instance.config = toml.load(file)
        return cls._instance

    @property
    def telegram_token(self):
        return self.config["telegram"]["bot_token"]

    @property
    def open_ai_key(self):
        return self.config["openai"]["api_key"]

    @property
    def log_path(self):
        return self.config["epictalesbot"].get("logs_path", "/var/log/epictales")

    @property
    def google_cloud_creds_file(self):
        return self.config["google"]["cloud"]["credentials_file"]

    @property
    def environment(self):
        return self.config["epictalesbot"].get("environment", "prod")

    @property
    def aws_region(self):
        return self.config["aws"]["region"]

    @property
    def aws_access_key_id(self):
        return self.config["aws"]["credentials"]["aws_access_key_id"]

    @property
    def aws_secret_access_key(self):
        return self.config["aws"]["credentials"]["aws_secret_access_key"]


config = Config(".epictalesbot.toml")
