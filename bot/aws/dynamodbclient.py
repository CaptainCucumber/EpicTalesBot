import boto3
from config import config


class DynamoDBClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DynamoDBClient, cls).__new__(cls, *args, **kwargs)
            cls._instance.client = boto3.resource(
                "dynamodb",
                region_name=config.aws_region,
                aws_access_key_id=config.aws_access_key_id,
                aws_secret_access_key=config.aws_secret_access_key,
            )
        return cls._instance

    def get_table(self, table_name):
        return self.client.Table(table_name)
