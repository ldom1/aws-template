import sys
from awsglue.utils import getResolvedOptions
import awswrangler as wr
import pandas as pd
import numpy as np
from tslearn.clustering import TimeSeriesKMeans


args = getResolvedOptions(
    sys.argv,
    ['BUCKET_NAME']
)
BUCKET_NAME = args['BUCKET_NAME']

# Read & format data
df = wr.s3.read_parquet(
    "s3://{BUCKET_NAME}/esgbu_dpv/plant_production/gold",
)

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by="date")
df = df.set_index('plant_id')

# List of unique plant id
plant_id = np.unique(df.index)

# Create time series data
data = [
    df.loc[plant]["energy_produced"].values
    for plant in plant_id
]

# Define modele and use the DTW metric
km = TimeSeriesKMeans(n_clusters=3, metric="dtw")
km_fit = km.fit(data)

# add labels to df
plant_labels = []

for k, elt in enumerate(km_fit.labels_):
    
    plant_labels.append(
        {
            "plant_id": plant_id[k],
            "label": elt
        }
    )
    
plant_labels = pd.DataFrame(plant_labels)
plant_labels = plant_labels.set_index("plant_id")

# DF with labels
df_with_labels = pd.merge(
    df,
    plant_labels,
    left_index=True,
    right_index=True
)
df_with_labels = df_with_labels.reset_index()

# Write data in S3
wr.s3.to_parquet(
    df=df_with_labels,
    path="s3://{BUCKET_NAME}/esgbu_dpv/predictions/predictions.parquet",
)

