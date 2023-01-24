# AWS Data Analytics Glue Workflow

Medium Article: 

## **Prerequisites**

* Python3 installed (version 3.6+)
* npm installed
* AWS CLI v2 installed


## **Update your AWS credentials**

Open the aws credentials file (linked to AWS CLI) and setup the credentials of your project as well as the glue_job_arn_role you will use to deploy your application.

On Mac

```
open ~/.aws/credentials
```

On Windows, go to :

```
C:\Users\username\.aws\credentials
```

Paste the credentials

```
[default]
aws_access_key_id = <>
aws_secret_access_key = <>
aws_session_token = <>
glue_role_arn = <AWS project role>
```

To get the credentials, of the AWS ARN role you aim to use.

## **Initial setup**

#### For MacOS run:

```
sh install.sh
```

Choose your prefered python version between: python3.6, python3.7, python3.8

**Note**: as of 21/09/2022 the newest version of aws-glue-sessions (0.35) doesn't work. Please stick to 0.32 as specified.

### **Details**

Setup a [virtul environment](https://python-guide-pt-br.readthedocs.io/fr/latest/dev/virtualenvs.html)

#### Run

```python
python3 -m venv .venv
```

#### Activate your venv (MacOS)

```python
source .venv/bin/activate
```

Install the mandatory packages to benefit from the full MODAPI experience

```python
pip install --upgrade jupyter boto3 aws-glue-sessions==0.32 jupyter pytest aws-cdk-lib
```

**Note:** If you have an SSL Certificate error when trying to install packages, use this command instead

```
pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --upgrade <package-to-be-installed>
```

## **Exploration**

For the exploration phase, we will use [Glue interactive session](https://docs.aws.amazon.com/glue/latest/dg/interactive-sessions-overview.html) with [jupyter notebooks](https://jupyter.org/).

For the initialisation, you will have to install the glue interactive session kernel.

### **Installation of Glue interactive session kernel**

#### **Generic command**

##### MacOS

```python
jupyter kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_pyspark

jupyter kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_spark
```

##### **Windows**

```
jupyter-kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_pyspark

jupyter-kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_spark

```

#### **Example**

Find the SITE_PACKAGES path using:

```python
pip3 show aws-glue-sessions | grep Location
```

With a venv in Python3.8 version:

```python
jupyter kernelspec install .venv/lib/python3.8/site-packages/aws_glue_interactive_sessions_kernel/glue_pyspark

jupyter kernelspec install .venv/lib/python3.8/site-packages/aws_glue_interactive_sessions_kernel/glue_spark
```

### **Start your notebook**

```python
cd exploration
jupyter notebook
```

And select the kernel of your choice : **Glue PySpark or Glue Spark**.

More information here: [How to use jupyter notebooks](https://www.codecademy.com/article/how-to-use-jupyter-notebooks)
