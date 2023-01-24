import os.path
from constructs import Construct
from aws_cdk import App, Environment, Stack, Tags, aws_glue as glue
from config.global_variables import GLUE_WORKFLOW_NAME, AWS_ACCOUNT, REGION, STACK_NAME, TAG_CDH_APPLICATION, TAG_CDH_CART, TAG_CDH_OWNER, GLUE_SCRIPTS_PATH, BUCKET_NAME
from utils.glue_utils import create_glue_job, create_job_trigger, create_startup_trigger

dir_name = os.path.dirname(__file__)


class DeploymentWorkflow(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        my_workflow = glue.CfnWorkflow(
            self, f'{GLUE_WORKFLOW_NAME}'
        )

        # JOBS
        job_data_processing = create_glue_job(
            self,
            job_name="job_data_processing",
            glue_job_path=f"{GLUE_SCRIPTS_PATH}/clean/processing_job.py",
            default_arguments={
                '--BUCKET_NAME': BUCKET_NAME
            },
            high_volume_job=True
        )

        job_predictions = create_glue_job(
            self,
            job_name="job_predictions",
            glue_job_path=f"{GLUE_SCRIPTS_PATH}/predict/predict.py",
            default_arguments={
                '--BUCKET_NAME': BUCKET_NAME,
                '--additional-python-modules': 'pyarrow==2,pandas,awswrangler,tslearn',
            },
            high_volume_job=False
        )

        # ORCHESTRATION
        create_startup_trigger(
            self,
            workflow=my_workflow,
            glue_job_to_start=[job_data_processing],
            to_activate=False
        )

        create_job_trigger(
            self,
            workflow=my_workflow,
            trigger_name="processing_to_prediction_trigger",
            input_jobs=[job_data_processing],
            output_jobs=[job_predictions],
            all_jobs_succeeded=True,
            to_activate=True
        )


env = Environment(account=AWS_ACCOUNT, region=REGION)
app = App()

aws_data_analytics_glue_workflow = DeploymentWorkflow(
    scope=app,
    id=STACK_NAME,
    env=env
)

Tags.of(aws_data_analytics_glue_workflow).add('cdh-cart', TAG_CDH_CART)
Tags.of(aws_data_analytics_glue_workflow).add('cdh-owner', TAG_CDH_OWNER)
Tags.of(aws_data_analytics_glue_workflow).add('cdh-application', TAG_CDH_APPLICATION)

app.synth()