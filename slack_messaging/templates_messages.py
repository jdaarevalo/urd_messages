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