import os
import boto3
import time
from datetime import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
from aws_lambda_powertools import Logger


logger = Logger()

dev_environment = os.environ.get('DEV_ENV_NAME')
region_name = os.environ.get('REGION_NAME')
table_name = os.environ.get("DYNAMODB_TABLE_NAME")

# Check if executing locally or on AWS, and configure DynamoDB connection accordingly.
if os.environ.get("AWS_SAM_LOCAL"):
    # SAM LOCAL
    if dev_environment == "OSX":
        # Environment ins Mac OSX
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://docker.for.mac.localhost:8000/")
    elif dev_environment == "Windows":
        # Environment is Windows
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://docker.for.windows.localhost:8000/")
    else:
        # Environment is Linux
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:8000")
else:
    # AWS
    dynamodb = boto3.resource('dynamodb', region_name=region_name)

table = dynamodb.Table(table_name)

def get_last_item_where(thread_group_key, channel):
    logger.info({"action":"get_last_item", "payload":{"thread_group_key":thread_group_key, "channel":channel}})
    response = table.query(
        KeyConditionExpression = Key('thread_group_key').eq(thread_group_key),
        FilterExpression = Attr('channel').eq(channel),
        Limit = 1,
        ScanIndexForward=False
    )
    logger.info({"action":"get_last_item_response", "payload":{"response":response}})
    return response['Items']

def put_item(thread_ts, channel, thread_group_key, message_result_ts):
    try:
        item = {
            'thread_group_key': thread_group_key,
            'ts': message_result_ts,
            'channel': channel,
            'thread_ts': thread_ts
            }
        table.put_item(Item=item)
        logger.info({"action":"put_item", "payload":{"item":item}})
    except Exception as error:
        logger.error({"action":"error_put_item", "payload":{"error":str(error)}})
