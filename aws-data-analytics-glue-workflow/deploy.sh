#!/bin/bash
read -p "aws profile name used to deploy (default or defined admin profile with aws configure): " aws_profile
echo "AWS profile used to deploy: --profile=$aws_profile"
cd deployment
glue_script_bucket=`cat config/global_variables.py | grep "^GLUE_SCRIPTS_BUCKET_NAME" | grep -Eo "[^=]*$" | tr -d ' ' | tr -d '"'` 
echo "Copying glue jobs in $glue_script_bucket"
aws s3 cp glue-scripts/ s3://$glue_script_bucket/glue-scripts/ --no-verify-ssl --recursive
echo "Glue jobs sync"
echo "Starting CDK synth"
cdk synth --profile=$aws_profile --verbose
echo "CDK synth done."
echo "Starting CDK deploy"
cdk deploy --all --profile=$aws_profile --verbose
echo "CDK deploy done."
cd ..