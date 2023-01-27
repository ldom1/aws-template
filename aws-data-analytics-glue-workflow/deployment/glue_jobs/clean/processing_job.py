import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql import functions as F
from pyspark.sql.window import Window
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

args = getResolvedOptions(
    sys.argv,
    ['BUCKET_NAME']
)
BUCKET_NAME = args['BUCKET_NAME']

plant_with_hour_granularity = spark.read.option("header", "true").parquet(
    f"s3://{BUCKET_NAME}/esgbu_dpv/plant/plant_hour.parquet"
)

plant_with_minute_granularity = spark.read.option("header", "true").parquet(
    f"s3://{BUCKET_NAME}/esgbu_dpv/plant/plant_minute.parquet"
)

plant_production = spark.read.option("header", "true").parquet(
    f"s3://{BUCKET_NAME}/esgbu_dpv/plant_production/raw"
)

# Concatenate granularity hour & minute
df_minute = (
    plant_with_minute_granularity
    .join(
        plant_production,
        on=["plant_id"],
        how="left"
    )
    .select(
        "country", "date", "average_irradiation", "plant_id", "energy_produced"
    )
)

df_hour = (
    plant_with_hour_granularity
    .join(
        plant_production,
        on=["plant_id"],
        how="left"
    )
    .select(
        "country", "date", "average_irradiation", "plant_id", "energy_produced"
    )
)

# Concat the two dataframes, both at the hour level
df = df_minute.union(df_hour)

# aggregate on daily level
df = (
    df
    .withColumn(
        "date",
        F.date_trunc('day', F.col("date"))
    )
    .groupBy(
        *["country", "date", "average_irradiation", "plant_id"]
    )
    .agg(
        F.sum('energy_produced').alias('energy_produced'),
    )
)

# Write the final dataset
df.write.mode("overwrite").save(
    f"s3://{BUCKET_NAME}/esgbu_dpv/plant_production/gold",
    format='parquet'
)