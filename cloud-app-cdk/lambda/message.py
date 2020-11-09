import os
import json
import boto3

def handler(event, context):
    table = os.environ.get('table')
    dynamodb = boto3.client('dynamodb')

    item = {
            "author":{'S':event["queryStringParameters"]["author"]},
            "message":{'S':event["queryStringParameters"]["message"]}
            }

    
    response = dynamodb.put_item(TableName=table,
            Item=item
            )

    message = 'Status of the write to DynamoDB {}!'.format(response)  
    return {
        "statusCode": 200,
        "body": json.dumps(message)
    }