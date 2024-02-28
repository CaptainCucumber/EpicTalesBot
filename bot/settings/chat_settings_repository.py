from datetime import datetime

from aws.dynamodbclient import DynamoDBClient


class ChatSettingsRepository:
    def __init__(self, table_name):
        self.table = DynamoDBClient().get_table(table_name)

    def get_chat_settings(self, chat_id):
        response = self.table.get_item(Key={"chat_id": chat_id})
        return response.get("Item", {})

    def update_chat_settings(self, chat_id, settings):
        current_datetime = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        updated_settings = {
            "chat_id": chat_id,
            "last_updated": current_datetime,
            **settings,
        }
        self.table.put_item(Item=updated_settings)
        return True

    def delete_chat_settings(self, chat_id):
        self.table.delete_item(Key={"chat_id": chat_id})
        return True
