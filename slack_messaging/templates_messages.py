from aws_lambda_powertools import Logger

logger = Logger()

STATUS_DEFAULT_COLOR = "#ffcc00"
STATUS_ERROR = "error"
STATUS_START = "start"
STATUS_FINISH = "finish"
STATUS_COLORS = {STATUS_START: "#0099cc", STATUS_ERROR: "#cc3300", STATUS_FINISH: "#006633"}
NO_ERRORS_MESSAGE = " " #empty space required by Slack to delivery the message

def details_error_section_report_status(message_keys):
	if message_keys.get("status") != STATUS_ERROR:
		return NO_ERRORS_MESSAGE
	error = str(message_keys.get("error", "NO DETAILS"))
	data = str(message_keys.get("data", "NO DETAILS"))
	return "*Error details:* ```" +error+ "``` *Params:* ```" +data+ "``` "

def format_report_status(message_keys):
    try:
        return {
            "attachments": [
                {
                    "color": STATUS_COLORS.get(message_keys.get("status"), STATUS_DEFAULT_COLOR),
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": message_keys.get("header")
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": "*Triggered by:*\n" +  message_keys.get("triggered_by")
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "*Update:*\n" + message_keys.get("module") + " is now " + message_keys.get("status").upper()
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": details_error_section_report_status(message_keys)
                            }
                        }
                    ]
                }
            ]
        }
    except Exception as error:
        logger.error({"action":"format_report_status", "payload":{"error":str(error)}})
        return {"error": str(error)}

def format_text_message(message_keys):
    try:
        return {
            "text": message_keys.get("text")
        }
    except Exception as error:
        logger.error({"action":"format_text_message", "payload":{"error":str(error)}})
        return {"error": str(error)}
