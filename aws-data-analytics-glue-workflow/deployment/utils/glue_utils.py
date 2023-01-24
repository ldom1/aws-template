from ast import Raise
import string
from aws_cdk import aws_glue as glue

from config.global_variables import CDH_PROJECT_ROLE_ARN, GLUE_SCRIPTS_BUCKET_NAME, GLUE_STARTUP_TRIGGER

# GLUE JOBS PARAMS
GLUE_JOB_ALLOCATED_CAPACITY = 10
GLUE_VERSION = '3.0'
PYTHON_VERSION = '3'
AWS_DEFAULT_REGION = 'eu-west-1'

# high volume
GLUE_JOB_WORKERS_TYPE_HIGH_VOLUME = 'G.1X'
GLUE_JOB_NUMBER_OF_WORKERS_HIGH_VOLUME = 10

# low volume
GLUE_JOB_WORKERS_TYPE_LOW_VOLUME = 'Standard'
GLUE_JOB_NUMBER_OF_WORKERS_LOW_VOLUME = 2




def create_glue_job(
    self, job_name: string, glue_job_path: string, default_arguments: dict = {},
    high_volume_job: bool = False
):


    if high_volume_job:
        nomber_of_workers = GLUE_JOB_NUMBER_OF_WORKERS_HIGH_VOLUME
        worker_type = GLUE_JOB_WORKERS_TYPE_HIGH_VOLUME
    else:
        nomber_of_workers = GLUE_JOB_NUMBER_OF_WORKERS_LOW_VOLUME
        worker_type = GLUE_JOB_WORKERS_TYPE_LOW_VOLUME

    return glue.CfnJob(
        self,
        job_name,
        role=CDH_PROJECT_ROLE_ARN,
        number_of_workers=nomber_of_workers,
        worker_type=worker_type,
        glue_version=GLUE_VERSION,
        command=glue.CfnJob.JobCommandProperty(
            name='glueetl',
            script_location=f's3://{GLUE_SCRIPTS_BUCKET_NAME}/glue-scripts/{glue_job_path}',
            python_version=PYTHON_VERSION
        ),
        default_arguments=default_arguments
    )


def create_startup_trigger(
    self, workflow, glue_job_to_start: list,
    cron: string = 'cron(0 8 * * ? *)', to_activate=False,
    glue_startup_trigger_name=None
):

    if glue_startup_trigger_name:
        trigger_name = glue_startup_trigger_name
    else:
        trigger_name = GLUE_STARTUP_TRIGGER

    return glue.CfnTrigger(
        self,
        trigger_name,
        actions=[
            glue.CfnTrigger.ActionProperty(
                job_name=job.ref,
            )
            for job in glue_job_to_start
        ],
        type='SCHEDULED',
        workflow_name=workflow.ref,
        schedule=cron,
        start_on_creation=to_activate
    )


def create_job_trigger(
    self, workflow, trigger_name: string, input_jobs: list, output_jobs: list,
    all_jobs_succeeded: bool = True, to_activate: bool = True
):
    if all_jobs_succeeded:
        logical = "AND"
    else:
        logical = "ANY"

    return glue.CfnTrigger(
        self,
        trigger_name,
        workflow_name=workflow.ref,
        type='CONDITIONAL',
        start_on_creation=to_activate,
        predicate=glue.CfnTrigger.PredicateProperty(
            conditions=[
                glue.CfnTrigger.ConditionProperty(
                    job_name=job.ref,
                    logical_operator="EQUALS",
                    state="SUCCEEDED",
                )
                for job in input_jobs
            ],
            logical=logical,
        ),
        actions=[
            glue.CfnTrigger.ActionProperty(
                job_name=job.ref,
            )
            for job in output_jobs
        ],
    )
