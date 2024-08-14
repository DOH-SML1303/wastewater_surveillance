import sys
import pandas as pd

def read_files(input_file_1, input_file_2, input_file_3):
    lineage_classifications = pd.read_csv(input_file_1)
    new_variants = pd.read_csv(input_file_2)
    variants_list = pd.read_csv(input_file_3)
    return lineage_classifications, new_variants, variants_list

def rename_columns(lineage_classifications):
    new_df = lineage_classifications.rename(columns={
        'lineage_extracted' : 'variant_name',
        'doh_variant_name' : 'variant'})
    return new_df

def filter_classifications(new_df, new_variants):
    filtered_df = new_df[new_df['variant_name'].isin(new_variants['variant_name'])]
    return filtered_df

def merge_new_class(filtered_df, new_variants):
    merged_df = pd.merge(filtered_df, new_variants, how='left', on='variant_name')
    return merged_df

def update_variant_list_new(merged_df, variants_list):
    new_variant_list = variants_list.append(merged_df)
    new_variant_list = new_variant_list.sort_values(by='variant_name').reset_index(drop=True)
    return new_variant_list

def main(input_file_1, input_file_2, input_file_3, output_file_1, output_file_2):
    lineage_classifications, new_variants, variants_list = read_files(input_file_1, input_file_2, input_file_3)
    new_df = rename_columns(lineage_classifications)
    filtered_df = filter_classifications(new_df, new_variants)
    merged_df = merge_new_class(filtered_df, new_variants)
    merged_df.to_csv("results/new_class.csv")
    new_variant_list = update_variant_list_new(merged_df, variants_list)
    new_variant_list.to_csv("results/variants.csv")

if __name__ == "__main__":
    if len(sys.argv) !=6:
        print("Usage: python3 ./scripts/update_new_variant_class.py data/lineage_classifications.csv results/new_variants.csv data/test_variants.csv results/new_class.csv results/variants.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
