#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Read environment variables from config.env
source config.env

# Define variables
STACK_NAME="MargaritaPetrovnaBotStack"
S3_BUCKET="margarita-petrovna-deployment"
REGION="us-west-2"
TEMPLATE_FILE="template.yaml"
PACKAGED_TEMPLATE="packaged-template.yaml"
LAMBDA_FUNCTION_DIR="bot/"
LAMBDA_FUNCTION_ZIP="bot.zip"
VIRTUAL_ENV_DIR="deployment_dependencies"
DEPLOYMENT_DIR="deployment_package"

setup_virtual_env() {
    echo "Setting up virtual environment..."
    python3 -m venv $VIRTUAL_ENV_DIR
    source $VIRTUAL_ENV_DIR/bin/activate
}

install_dependencies() {
    echo "Installing dependencies..."
    pip install -r requirements.txt
}

prepare_deployment_package() {
    echo "Preparing deployment package..."
    mkdir -p $DEPLOYMENT_DIR
    cp -r $VIRTUAL_ENV_DIR/lib/python3.*/site-packages/* $DEPLOYMENT_DIR/
    cp -r $LAMBDA_FUNCTION_DIR/* $DEPLOYMENT_DIR/
}

create_deployment_package() {
    echo "Creating deployment package..."
    cd $DEPLOYMENT_DIR
    zip -r ../$LAMBDA_FUNCTION_ZIP .
    cd ..
    # Deactivate virtual environment only if it's active
    if [[ -n "$VIRTUAL_ENV" ]]; then
        deactivate
    fi
}

upload_to_s3() {
    if aws s3 ls "s3://$S3_BUCKET" 2>&1 | grep -q 'NoSuchBucket'
    then
        echo "Creating S3 bucket: $S3_BUCKET"
        aws s3 mb "s3://$S3_BUCKET" --region $REGION
    else
        echo "S3 bucket $S3_BUCKET already exists"
    fi

    echo "Uploading Lambda function to S3..."
    aws s3 cp $LAMBDA_FUNCTION_ZIP s3://$S3_BUCKET/$LAMBDA_FUNCTION_ZIP
}

package_cloudformation() {
    echo "Packaging the CloudFormation template..."
    aws cloudformation package \
        --template-file $TEMPLATE_FILE \
        --s3-bucket $S3_BUCKET \
        --output-template-file $PACKAGED_TEMPLATE
}

deploy_cloudformation() {
    echo "Deploying the CloudFormation stack..."
    aws cloudformation deploy \
        --template-file $PACKAGED_TEMPLATE \
        --stack-name $STACK_NAME \
        --region $REGION \
        --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
        --parameter-overrides \
            LambdaFunctionS3Bucket=$S3_BUCKET \
            LambdaFunctionS3Key=$LAMBDA_FUNCTION_ZIP \
            TelegramTokenParameter=$TELEGRAM_TOKEN \
            OpenAiApiKeyParameter=$OPENAI_API_KEY \
        --debug
}

cleanup() {
    echo "Cleaning up..."
    rm $LAMBDA_FUNCTION_ZIP
    rm -rf $DEPLOYMENT_DIR
    rm $PACKAGED_TEMPLATE
    # Clean up virtual environment directory if it exists
    if [[ -d "$VIRTUAL_ENV_DIR" ]]; then
        rm -rf $VIRTUAL_ENV_DIR
    fi
}

case "$1" in
    --full-deploy)
        setup_virtual_env
        install_dependencies
        prepare_deployment_package
        create_deployment_package
        upload_to_s3
        package_cloudformation
        deploy_cloudformation
        cleanup
        ;;
    --package-deploy)
        prepare_deployment_package
        create_deployment_package
        upload_to_s3
        package_cloudformation
        deploy_cloudformation
        cleanup
        ;;
    *)
        echo "Usage: $0 [--full-deploy | --package-deploy]"
        exit 1
        ;;
esac

echo "Deployment complete."
