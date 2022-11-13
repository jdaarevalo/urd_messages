"""
Purpose

Post in Slack a message
"""
import os
import json
import logging
import dynamodb_operations
import templates_messages
from slack_sdk import WebClient


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

	# Compose attachments and format message
	formated_message = compose_formated_message(json_body)
	if formated_message.get("error", False):
		return { "statusCode": 400, "status": "error", "body": formated_message["error"] }

	# Fetch thread_ts if exist and if is thread_group_key is a parameter
	channel = json_body.get('channel')
	thread_group_key = json_body.get('thread_group_key')
	thread_ts = fetch_ts(thread_group_key, channel) if thread_group_key else None

	# Send slack message
	send_message_result = send_slack_message(channel, formated_message, thread_ts)
	if send_message_result.get("error", False):
		return { "statusCode": 400, "status": "error", "body": send_message_result["error"] }

	# Store message_result_ts in DynamoDB
	message_result_ts = send_message_result['ts']
	if json_body.get('thread_group_key'):
		dynamodb_operations.put_item(thread_ts, channel, thread_group_key, message_result_ts)
	
	return {
        "statusCode": 200,
        "body": '{"status":"success", "code":200, "message": "Message delivered"}'
		""
    }

def validate_body_structure(json_body, errors=[]):
	if not json_body:
		errors = ["body required"]	

	if not BODY_KEYS_REQUIRED.issubset(set(json_body.keys())):
		errors = ["missing keys, check keys_required " + str(BODY_KEYS_REQUIRED)]

	#TODO: validate keys required by templates depending on the use case
	if errors:
		logger.error('## validate_body_structure return errors  %s', str(errors))
		return {'status': "error", 'code': 400, 'errors': errors }

def compose_formated_message(json_body):
	template_name = json_body.get('template')
	message_keys = json_body.get('message_keys')
	format_template = getattr(templates_messages, 'format_'+template_name)
	return format_template(message_keys)

def fetch_ts(thread_group_key, channel):
	list_item = dynamodb_operations.get_last_item_where(thread_group_key, channel)
	if list_item:
		return list_item[0]['ts']

def send_slack_message(channel, formated_message, thread_ts):
	try:
   		# Call the chat.postMessage method using the WebClient
		return slack_client.chat_postMessage(
			channel=channel,
			attachments=formated_message.get("attachments"),
			text=formated_message.get("text"),
			thread_ts=thread_ts
		)
	except Exception as error:
		logger.error('## Error posting message:  %s', str(error))
		return {"error": str(error)}
