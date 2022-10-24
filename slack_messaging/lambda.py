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


STATUS_DEFAULT_COLOR = "#ffcc00"
STATUS_ERROR = "error"
STATUS_START = "start"
STATUS_FINISH = "finish"
STATUS_COLORS = {STATUS_START: "#0099cc", STATUS_ERROR: "#cc3300", STATUS_FINISH: "#006633"}
NO_ERRORS_MESSAGE = " " #empty space required by Slack to delivery the message

BODY_KEYS_REQUIRED = set(['channel', 'thread_group_key', 'template', 'message_keys'])

slack_bot_user_oauth_token = os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN")
slack_client = WebClient(slack_bot_user_oauth_token)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
	logger.info('## Invoke function with event %s', event)
	data_body = event.get("body", "{}")	
	json_body = json.loads(data_body)

	logger.info('## body_event %s', json_body)

	errors_body = validate_body_structure(json_body)
	if errors_body:
		return { "statusCode": 400, "status": "error", "body": json.dumps(errors_body) }
	
	result = send_slack_message(json_body)


	# store thread_ts
	# thread_ts = result.data['ts']
	#return thread_ts
	return {
        "statusCode": 200,
        "body": '{"status":"success", "code":200, "message": "Message delivered"}'
    }

def send_slack_message(json_body):
	# Template from the event key
	attachments = compose_attachments(json_body)
	thread_ts = fetch_ts(json_body) if json_body.get('thread_group_key') else None
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
	
def fetch_ts(json_body):
	channel = json_body.get('channel')
	thread_group_key = json_body.get('thread_group_key')
	get_last_item_where(channel, thread_group_key)
	return None


def validate_body_structure(json_body, errors=[]):
	if not json_body:
		errors = ["body required"]	
	
	if not BODY_KEYS_REQUIRED.issubset(set(json_body.keys())):
		errors = ["missing keys, check keys_required " + str(BODY_KEYS_REQUIRED)]
	
	#TODO: VALIDATE KEYS REQUIRED BY TEMPLATE, DEPENDS ON THE USE CASE

	if errors:
		logger.error('## validate_body_structure return errors  %s', str(errors))
		return {'status': "error", 'code': 400, 'errors': errors }

