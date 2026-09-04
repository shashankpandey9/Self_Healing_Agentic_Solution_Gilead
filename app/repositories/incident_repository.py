from app.services.aws.dynamodb_service import DynamoDBService


class IncidentRepository:

    def __init__(self):

        self.db = DynamoDBService()

    def find_incident(
        self,
        error_type: str,
        error_message: str
    ):

        response = self.db.table.scan()

        items = response.get(
            "Items",
            []
        )

        for item in items:

            if (
                item.get("error_type")
                == error_type
            ) and (
                item.get("error_message")
                == error_message
            ):
                return item

        return None