"""
Purpose

Post in Slack a message
"""
import os
import json
import logging
import templates_messages
from slack_sdk import WebClient
from dynamodb_operations import get_last_item_where

BODY_KEYS_REQUIRED = set(['channel', 'template', 'message_keys'])

slack_bot_user_oauth_token = os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN")
slack_client = WebClient(slack_bot_user_oauth_token)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
	logger.info('## Invoke function with event %s', event)
	
	# Load body JSON for processing
	try:
		json_body = json.loads(event.get("body", "{}"))
	except:
		return {'statusCode': 400, 'body': 'malformed JSON'}

	# Validate body structure and check possible errors
	errors_body = validate_body_structure(json_body)
	if errors_body:
		return { "statusCode": 400, "status": "error", "body": json.dumps(errors_body) }
	
	# Fetch thread_ts if exist and if is thread_group_key is a parameter
	channel = json_body.get('channel')
	thread_group_key = json_body.get('thread_group_key')
	#thread_ts = fetch_ts(thread_group_key, channel) if thread_group_key else None
	thread_ts = fetch_ts("pruebas_1", "channel_3") if thread_group_key else None

	template = json_body.get('template')
	print("#"*100)
	print(thread_group_key)
	print(thread_ts)
	print("#"*100)
	## traer template de acuerdo al nombre y formatear
	#result = send_slack_message(json_body, thread_ts)


	# guardar thread_ts en dynamo if json_body.get('thread_group_key')

	# thread_ts = result.data['ts']
	
	return {
        "statusCode": 200,
        "body": '{"status":"success", "code":200, "message": "Message delivered"}'
    }


def validate_body_structure(json_body, errors=[]):
	if not json_body:
		errors = ["body required"]	
	
	if not BODY_KEYS_REQUIRED.issubset(set(json_body.keys())):
		errors = ["missing keys, check keys_required " + str(BODY_KEYS_REQUIRED)]
	
	#TODO: validate keys required by template, depends on the use case
	if errors:
		logger.error('## validate_body_structure return errors  %s', str(errors))
		return {'status': "error", 'code': 400, 'errors': errors }

def fetch_ts(thread_group_key, channel):
	list_item = get_last_item_where(thread_group_key, channel)
	if list_item:
		return list_item[0]['ts']





def send_slack_message(json_body, thread_ts):
	# Template from the event key
	attachments = compose_attachments(json_body)
	try:
   		# Call the chat.postMessage method using the WebClient
		return slack_client.chat_postMessage(
			channel=json_body['channel'], 
			attachments=attachments,
			thread_ts=thread_ts
		)
	except Exception as error:
		logger.error('## Error posting message:  %s', str(error))
		return {"error": str(error)}

## TODO
def compose_attachments(json_body):
	template = json_body["template"].upper()
	# constant as variable
	# templates_messages.(template).format()
