# urd_messages

Create Slack app, include the scope chat:write
## Run locally

To run DynamoDB it is required to execute 
docker-compose up

## Deploy

## Usage
Parameters to send a message

### Required arguments

**channel:** channel to send message to. Can be an encoded ID, or a name
**template** template used to send the message (report_status)
message_keys
### Optional arguments

**thread_group_key:** Is a key used to thread messages (project_id=1234&study_id=456)
