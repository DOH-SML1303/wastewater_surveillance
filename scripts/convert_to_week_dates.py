import sys
import pandas as pd
import datetime

def read_files(input_file_1):
    line_list = pd.read_csv(input_file_1, parse_dates=['Sample_Collection_Date'], low_memory=False)
    return line_list

def convert_dates(line_list):
    new_df = line_list.copy()
    new_df['Sample_Collection_Date'] = pd.to_datetime(new_df['Sample_Collection_Date'])

    # Define transformations for date-related columns
    transformations = {
        'ISO_Year': lambda df: df['Sample_Collection_Date'].dt.isocalendar().year,
        'ISO_Week': lambda df: df['Sample_Collection_Date'].dt.isocalendar().week
    }

    # Apply transformations using a for loop
    for column, transform_func in transformations.items():
        new_df[column] = transform_func(new_df)

    # Create 'Date' column from the transformed columns
    new_df['Date'] = (new_df['ISO_Year'].astype(str) + '-' +
                      new_df['ISO_Week'].astype(str).str.zfill(2))

    new_df = new_df.sort_values(by='Date').reset_index(drop=True)
    return new_df

def main(input_file_1, output_file):
    line_list = read_files(input_file_1)
    new_df = convert_dates(line_list)
    new_df.to_csv(output_file, index=False)
    print("Week dates have been added.")

if __name__ == "__main__":
    if len(sys.argv) !=3:
        # need to fix this when i figure out what the file names are
        print("Usage: python3 ./scripts/convert_to_week_dates.py data/WW_data_lat_long.csv data/WW_data_week_dates.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
