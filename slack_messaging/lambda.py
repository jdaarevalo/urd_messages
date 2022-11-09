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
	print("#"*100)
	print(type(event))
	print("#"*100)

	logger.info('## Invoke function with event %s', event)
	data_body = event.get("body", "{}")	
	json_body = json.loads(data_body)

	logger.info('## body_event %s', json_body)
	# Validate body structure and check possible errors
	errors_body = validate_body_structure(json_body)
	if errors_body:
		return { "statusCode": 400, "status": "error", "body": json.dumps(errors_body) }
	
	# Fetch thread_ts if exist and if is thread_group_key is a parameter
	channel = json_body.get('channel')
	thread_group_key = json_body.get('thread_group_key')	
	thread_ts = fetch_ts(thread_group_key, channel) if thread_group_key else None

	
	## traer template de acuerdo al nombre y formatear
	#result = send_slack_message(json_body, thread_ts)


	# guardar thread_ts en dynamo if json_body.get('thread_group_key')

	# thread_ts = result.data['ts']
	#return thread_ts
	return {
        "statusCode": 200,
        "body": '{"status":"success", "code":200, "message": "Message delivered"}'
    }

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



def validate_body_structure(json_body, errors=[]):
	if not json_body:
		errors = ["body required"]	
	
	if not BODY_KEYS_REQUIRED.issubset(set(json_body.keys())):
		errors = ["missing keys, check keys_required " + str(BODY_KEYS_REQUIRED)]
	
	#TODO: VALIDATE KEYS REQUIRED BY TEMPLATE, DEPENDS ON THE USE CASE

	if errors:
		logger.error('## validate_body_structure return errors  %s', str(errors))
		return {'status': "error", 'code': 400, 'errors': errors }

def fetch_ts(thread_group_key, channel):
	list_item = get_last_item_where(thread_group_key, channel)
	if list_item:
		return list_item[0]['ts']