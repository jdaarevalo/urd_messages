#!/bin/bash

# $chmod +x deploy.sh
# $./deploy.sh staging

# Variables
export AWS_REGION=eu-west-1
export STACK_NAME="urd-messages"


sam build
sam deploy \
--stack-name "${STACK_NAME}" \
--region "${AWS_REGION}" \
--resolve-s3 \
--capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
