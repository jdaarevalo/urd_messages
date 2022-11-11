import os
import boto3
import time
import logging
from datetime import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
    logger.info('## dynamo filter where thread_group_key %s', thread_group_key)
    response = table.query(
        KeyConditionExpression = Key('thread_group_key').eq(thread_group_key),
        FilterExpression = Attr('channel').eq(channel),
        Limit = 1,
        ScanIndexForward=False
    )
    logger.info('## dynamo response %s', response)
    return response['Items']

## TODO






def get_item(item, data_response={}, errors={}):
    logger.info("get project_item with item: {}".format(item))
    try:
        data_response = table.get_item(Key=item)["Item"]
    except Exception as e:
        logger.warning("Item doesn't exist")
        errors = str(e)
    
    return data_response, errors

def create_item(item, data_response={}, errors={}):
    logger.info("create project_item with item: {}".format(item))
    TABLE_KEYS_REQUIRED = set(["project_wave", "module_status", "triggered_by"])
    
    if not TABLE_KEYS_REQUIRED.issubset(set(item.keys())):
        return {}, {"missing keys": TABLE_KEYS_REQUIRED }
        
    item["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        data_response = table.put_item(Item=item)
        logger.info("created project_item with item: {}".format(item))
    except Exception as e:
        logger.warning("Item couldn’t be created errors {}".format(str(e)))
        errors = str(e)
    return data_response, errors


    

