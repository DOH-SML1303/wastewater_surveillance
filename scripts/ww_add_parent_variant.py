import sys
import pandas as pd

def read_files(input_file_1, input_file_2):
    data = pd.read_csv(input_file_1, sep=",", low_memory=False)
    variants = pd.read_csv(input_file_2)
    return data, variants

# merge
def merge_files(data, variants):
    new_df = data.copy()
    merged_df = new_df.merge(variants, on="Variant_name", how="left")
    return merged_df

def main(input_file_1, input_file_2, output_file):
    data, variants = read_files(input_file_1, input_file_2)
    merged_df = merge_files(data, variants)
    merged_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    if len(sys.argv) !=4:
        print("Usage: python3 ./scripts/ww_add_parent_variant.py data/WW_master.csv data/WW_variants.csv data/WW_data_variants.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
