import sys
import pandas as pd
import numpy as np

def read_files(input_file_1):
    data = pd.read_csv(input_file_1, index_col=['variant'])
    data = data.T
    return data

def get_last_8_weeks(data):
    last_8_weeks = data.tail(8)
    return last_8_weeks

def drop_old_variants(last_8_weeks):
    cleaned = last_8_weeks.loc[:, (last_8_weeks !=0).any(axis=0)]
    cleaned = cleaned * 100
    cleaned = cleaned.round(3)
    cleaned.to_csv("results/latest_proportions.csv")
    return cleaned

def main(input_file_1, output_file):
    data = read_files(input_file_1)
    last_8_weeks = get_last_8_weeks(data)
    cleaned = drop_old_variants(last_8_weeks)
    print("proportions table generated")

if __name__ == "__main__":
    if len(sys.argv) !=3:
        print("Usage: python3 ./scripts/get_latest_proportions.py results/proportions_table.csv results/latest_proportions.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
