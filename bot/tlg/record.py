from aws.dynamodbclient import DynamoDBClient


class RecordRepository:
    def __init__(self, table_name):
        self.table = DynamoDBClient().get_table(table_name)

    def put_record(self, update_id, settings):
        self.table.put_item(Item={"update_id": update_id, **settings})
        return True
