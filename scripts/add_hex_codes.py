import sys
import pandas as pd
import datetime

def read_files(input_file_1, input_file_2):
    data_parents = pd.read_csv(input_file_1, low_memory=False)
    hexcodes = pd.read_csv(input_file_2)
    return data_parents, hexcodes

# merge
def merge_files(data_parents, hexcodes):
    new_df = data_parents.copy()
    merged_df = new_df.merge(hexcodes, on="variant", how="left")
    return merged_df

def rename_columns(merged_df):
    merged_df = merged_df.rename(columns={
        'hex_code' : 'variant__colour'})
    return merged_df

def main(input_file_1, input_file_2, output_file):
    data_parents, hexcodes = read_files(input_file_1, input_file_2)
    merged_df = merge_files(data_parents, hexcodes)
    merged_df = rename_columns(merged_df)
    merged_df.to_csv(output_file, index=False)
    print("Hexcodes for the variants have been added.")

if __name__ == "__main__":
    if len(sys.argv) !=4:
        print("Usage: python3 ./scripts/add_hex_codes.py data/WW_data_variants.csv data/WW_hexcodes.csv data/WW_data_hexcodes.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
