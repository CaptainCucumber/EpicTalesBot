from aws.dynamodbclient import DynamoDBClient
from botocore.exceptions import ClientError


class ChatSettingsRepository:
    def __init__(self, table_name):
        self.table = DynamoDBClient().get_table(table_name)

    def get_chat_settings(self, chat_id):
        try:
            response = self.table.get_item(Key={"chat_id": chat_id})
            return response.get("Item", {})
        except ClientError as e:
            print(e.response["Error"]["Message"])
            return None

    def update_chat_settings(self, chat_id, settings):
        try:
            self.table.put_item(Item={"user_id": chat_id, **settings})
            return True
        except ClientError as e:
            print(e.response["Error"]["Message"])
            return False

    def delete_chat_settings(self, chat_id):
        try:
            self.table.delete_item(Key={"user_id": chat_id})
            return True
        except ClientError as e:
            print(e.response["Error"]["Message"])
            return False
