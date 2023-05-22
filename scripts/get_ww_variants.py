
import pandas as pd

# read in files
grouped_variants = pd.read_csv('~/wastewater-surveillance/data/groupby_variants.csv')
variants = pd.read_csv('~/wastewater-surveillance/data/variants.csv')

# convert variants into dictionary
dict = variants.set_index('Variant name')['variant'].to_dict()
print(dict)

# iterate through the grouped WW variants to find those variants not in a dictionary
ww_variants = 'Variant_name'
list = []
for variant in grouped_variants[ww_variants]:
    if variant not in dict:
        list.append(variant)
        print(variant)
print(list)

# add variants to dictionary
dict['XZ'] = 'Recombinant'

dict_df = pd.DataFrame(dict, index=['Variant name'])
dict_df.to_csv('~/wastewater-surveillance/data/dictionary.csv')
