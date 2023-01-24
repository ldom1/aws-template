#!/bin/bash
read -p "Python version: (python3.6, python3.7, python3.8, python3.9): " python_version
echo "Python version selected: $python_version"
$python_version -m venv .venv
source .venv/bin/activate
python -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --upgrade pip
python -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org jupyter pandas numpy matplotlib pyarrow==2 awswrangler
python -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org fastdtw scikit-learn scipy tslearn
python -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org boto3 aws-glue-sessions==0.32 aws-cdk-lib
pip freeze > requirements.txt
jupyter kernelspec install .venv/lib/$python_version/site-packages/aws_glue_interactive_sessions_kernel/glue_pyspark
jupyter kernelspec install .venv/lib/$python_version/site-packages/aws_glue_interactive_sessions_kernel/glue_spark
ipython kernel install --name "aws_data_analytics_glue_workflow" --user

cat ~/ca_certs/IS_INFRA_ROOT_CRT.crt >> $(python -m certifi)
export REQUESTS_CA_BUNDLE=$(python -m certifi)
export SSL_CERT_FILE=$(python -m certifi)
export CERT_PATH=$(python -m certifi)
export AWS_REGION=eu-west-1
jupyter notebook