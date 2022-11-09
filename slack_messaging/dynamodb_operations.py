import os
import boto3
import time
import logging
from datetime import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)


if os.environ.get("AWS_SAM_LOCAL"):
    dynamodb = boto3.resource('dynamodb',endpoint_url='http://localhost:8000')
else:
    dynamodb = boto3.resource('dynamodb')

table_name = os.environ.get("DYNAMODB_TABLE_NAME")
table = dynamodb.Table(table_name)

## TODO
def get_last_item_where(thread_group_key, channel):
    response = table.query(
        KeyConditionExpression = Key('thread_group_key').eq(thread_group_key),
        FilterExpression = Attr('channel').eq(channel),
        Limit = 1,
        ScanIndexForward=False
    )
    return response['Items']



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


    

