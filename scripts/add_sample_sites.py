import pandas as pd

def load_data(data_file, sites_file):
    data_df = pd.read_csv(data_file)
    sites_df = pd.read_csv(sites_file)
    return data_df, sites_df

def add_site_info(data_df, sites_df):
    # Merge with sample site details
    merged_df = data_df.merge(
        sites_df[['Sample_Site', 'location', 'latitude', 'longitude']],
        how='left',
        on='Sample_Site'
    )
    return merged_df

def save_output(merged_df, output_file):
    merged_df.to_csv(output_file, index=False)
    print(f"Data with sample site information saved to {output_file}")

def main(data_file, sites_file, output_file):
    data_df, sites_df = load_data(data_file, sites_file)
    merged_df = add_site_info(data_df, sites_df)
    save_output(merged_df, output_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python add_sample_sites.py <data_file> <sites_file> <output_file>")
        sys.exit(1)
    main(*sys.argv[1:])
