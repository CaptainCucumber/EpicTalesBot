#!/bin/bash

# Variables
bucket_name="epictalesbot.com"
region="us-west-2"
local_directory="./web/public"
version_folder=$(date +%Y%m%d-%H%M%S)
stack_name="EpicTalesWebsite"
template_file="./inf/website_hosting.yaml"

# Deploy CloudFormation template
aws cloudformation deploy \
    --template-file $template_file \
    --stack-name $stack_name \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides BucketName=$bucket_name VersionFolder=$version_folder

# Sync website content to the S3 bucket (after CloudFormation deployment)
aws s3 sync $local_directory s3://$bucket_name/$version_folder

echo "Deployment to version folder $version_folder complete."
