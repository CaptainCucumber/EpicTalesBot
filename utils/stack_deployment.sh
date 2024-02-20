#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Print commands as they are executed. For debugging.
# set -x

# Initialize variables
TEMPLATE_FILE=""
BASE_STACK_NAME=""
STAGE=""
REGION="us-west-2"
DEPLOYMENT_ID=$(date +%s)  # Unique timestamp as deployment ID

CAPABILITIES="CAPABILITY_IAM CAPABILITY_NAMED_IAM"

# Function to show usage
function show_usage {
    echo "Usage: $0 --template <CloudFormation template file> --stack-name <base stack name> --stage <stage> [--region <AWS region>]"
    exit 1
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --template) TEMPLATE_FILE="$2"; shift ;;
        --stack-name) BASE_STACK_NAME="$2"; shift ;;
        --stage) STAGE="$2"; shift ;;
        --region) REGION="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; show_usage ;;
    esac
    shift
done

# Check required parameters
if [ -z "$TEMPLATE_FILE" ] || [ -z "$BASE_STACK_NAME" ] || [ -z "$STAGE" ]; then
    echo "Error: Template, base stack name, and stage are required."
    show_usage
fi

# Construct the full stack name with stage
STACK_NAME="${BASE_STACK_NAME}-${STAGE}"

function create_or_update_stack {
    echo "Deploying stack $STACK_NAME using template $TEMPLATE_FILE in region $REGION for stage $STAGE..."
    aws cloudformation deploy \
        --template-file $TEMPLATE_FILE \
        --stack-name $STACK_NAME \
        --parameter-overrides Stage=$STAGE DeploymentId=$DEPLOYMENT_ID \
        --capabilities $CAPABILITIES \
        --region $REGION
    echo "Deployment completed."
}

# Deploy the stack (create or update)
create_or_update_stack
