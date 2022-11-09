STATUS_DEFAULT_COLOR = "#ffcc00"
STATUS_ERROR = "error"
STATUS_START = "start"
STATUS_FINISH = "finish"
STATUS_COLORS = {STATUS_START: "#0099cc", STATUS_ERROR: "#cc3300", STATUS_FINISH: "#006633"}
NO_ERRORS_MESSAGE = " " #empty space required by Slack to delivery the message

REPORT_STATUS = """
    [
        {
            "color": "#cc3300",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "header_message"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Triggered by:*\n David Test"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Update:*\n" + "update"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "details_error_section(body_event)"
                    }
                }
            ]
        }
    ]
"""