import sys
import pandas as pd

def read_files(input_file_1, input_file_2):
    line_list = pd.read_csv(input_file_1, low_memory=False)
    geo = pd.read_csv(input_file_2)
    return line_list, geo

def merge_files(line_list, geo):
    merged_df = line_list.merge(geo, on="Sample_Site", how="left")
    return merged_df

def main(input_file_1, input_file_2, output_file):
    line_list, geo = read_files(input_file_1, input_file_2)
    merged_df = merge_files(line_list, geo)
    merged_df.to_csv(output_file, index=False)
    print("Latitude and Longitude for sampling sites added.")

if __name__ == "__main__":
    if len(sys.argv) !=4:
        # need to fix this when i figure out what the file names are
        print("Usage: python3 ./scripts/add_lat_long.py data/WW_data_hexcodes.csv data/sample_site-counties.csv data/WW_data_lat_long.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
