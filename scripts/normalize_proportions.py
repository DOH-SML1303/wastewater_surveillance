import sys
import pandas as pd

def read_files(input_file_1):
    line_list = pd.read_csv(input_file_1, low_memory=False)
    return line_list

def calculate_proportions(line_list):
    line_list['normalize_proportions'] = (
        line_list['Variant_proportion'] /
        line_list.groupby('Date')['Variant_proportion'].transform('sum')
    )
    return line_list

def main(input_file_1, output_file):
    line_list = read_files(input_file_1)
    line_list = calculate_proportions(line_list)
    line_list.to_csv(output_file, index=False)
    print("Proportions have been normalized")

if __name__ == "__main__":
    if len(sys.argv) !=3:
        # need to fix this when i figure out what the file names are
        print("Usage: python3 ./scripts/normalize_proportions.py data/WW_data_week_dates.csv results/WW_data.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
