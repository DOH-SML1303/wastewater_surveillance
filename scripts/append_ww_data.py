import os
import pandas as pd

directory = '/home/ubuntu/wastewater_surveillance/data/db_update_dump'

dataframes = []

for filename in os.listdir(directory):
    if filename.endswith('batch_output.tsv'):
        file_path = os.path.join(directory, filename)

        df = pd.read_csv(file_path, sep='\t')
        dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)
print(combined_df.head())

combined_df.to_csv('~/wastewater_surveillance/data/WW_master.csv')
