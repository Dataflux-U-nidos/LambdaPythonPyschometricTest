import json


def lambda_handler(event, context):

    version = event.get("version", "1.0.0")
    print(f"Version: {version}")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
            }
        ),
    }
