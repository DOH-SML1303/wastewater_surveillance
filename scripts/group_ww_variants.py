import pandas as pd

ww_df = pd.read_csv('~/PycharmProjects/scripts/data/WW_master.csv')
variants = pd.read_csv('~/PycharmProjects/scripts//data/variants.csv')

groupby_variants = ww_df.groupby('Variant_name')['Variant_name'].apply(list)
groupby_variants.to_csv('~/PycharmProjects/scripts/data/groupby_variants.csv')
grouped_variants = pd.read_csv('~/PycharmProjects/scripts/data/groupby_variants.csv')

