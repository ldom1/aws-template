#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
pip install aws-cdk-lib==2.37.1
cd deployment/
glue_script_bucket=`cat config/global_variables.py | grep "^GLUE_SCRIPTS_BUCKET_NAME" | grep -Eo "[^=]*$" | tr -d ' ' | tr -d '"'` 
echo "Copying glue jobs in $glue_script_bucket"
aws s3 cp glue-scripts/ s3://$glue_script_bucket/glue-scripts/ --no-verify-ssl --recursive
echo "Glue jobs sync"
echo "Starting CDK synth"
cdk deploy --all
cd ..
