import pandas as pd

ww_df = pd.read_csv('~/wastewater-surveillance/data/WW_master.csv')
groupby_variants = ww_df.groupby('Variant_name')['Variant_name'].apply(list)
groupby_variants.to_csv('~/wastewater-surveillance/data/groupby_variants.csv')

