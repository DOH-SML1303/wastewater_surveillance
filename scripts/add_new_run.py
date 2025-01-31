import pandas as pd
import sys
import glob

def load_data(master_file, new_run_files):
    # Load the master line list
    master_df = pd.read_csv(master_file, low_memory=False)

    # Load all new run files and concatenate them
    new_run_dfs = []
    for file in new_run_files:
        new_run_df = pd.read_csv(file, sep="\t")
        new_run_df['Source_File'] = file  # Track source file for duplicate checking
        new_run_dfs.append(new_run_df)

    new_run_df_combined = pd.concat(new_run_dfs, ignore_index=True)
    return master_df, new_run_df_combined

def check_for_duplicates(master_df, new_run_df):
    # Find duplicates between master and new run based on Sample_ID
    duplicate_ids = new_run_df[new_run_df['Sample_ID'].isin(master_df['Sample_ID'])]

    if not duplicate_ids.empty:
        duplicate_report = duplicate_ids[['Sample_ID', 'Source_File']].drop_duplicates()
        raise ValueError(f"Duplicate Sample_IDs found:\n{duplicate_report.to_string(index=False)}")

def add_new_run(master_df, new_run_df):
    # get unique files
    added_files = new_run_df['Source_File'].unique().tolist()
    # Concatenate new run data to master line list
    combined_df = pd.concat([master_df, new_run_df.drop(columns=['Source_File'])]).drop_duplicates().reset_index(drop=True)
    #combined_df = combined_df.drop(columns=[['Lab_ID', 'Sample_County', 'Sample_Zip']])

# Identify new variants based on 'Variant_name' and 'Sample_Collection_Date'
    #master_index = master_df.set_index(['Variant_name', 'Sample_Collection_Date']).index
    #new_index = new_run_df.set_index(['Variant_name', 'Sample_Collection_Date']).index
    #new_variants = new_run_df[~new_index.isin(master_index)]['Variant_name']
    #new_variants = new_run_df_combined[~new_run_df_combined.set_index(['Variant_name', 'Sample_Collection_Date']).index.isin(master_df.set_index(
    #    ['Variant_name', 'Sample_Collection_Date']).index)][['Variant_name', 'Sample_Collection_Date']]

    new_variants = new_run_df[~new_run_df['Variant_name'].isin(master_df['Variant_name'])][['Variant_name', 'Sample_Collection_Date']]
    new_variants_report = new_variants.groupby('Variant_name').agg(
        First_Appearance_Date=('Sample_Collection_Date', 'min'),
    ).reset_index()

    return combined_df, new_variants_report, added_files

def save_outputs(combined_df, new_variants_report, output_file, new_variants_file):
    # Save the updated master list
    combined_df.to_csv(output_file, index=False)
    # Save the new variants report
    new_variants_report.to_csv(new_variants_file, index=False)

def main(master_file, new_run_dir, output_file, new_variants_file):
    # Read all TSV files in the new run directory
    new_run_files = glob.glob(f"{new_run_dir}/*.tsv")
    if not new_run_files:
        raise FileNotFoundError(f"No TSV files found in {new_run_dir}")

    master_df, new_run_df = load_data(master_file, new_run_files)
    check_for_duplicates(master_df, new_run_df)  # Check for duplicates

    combined_df, new_variants_report, added_files = add_new_run(master_df, new_run_df)
    save_outputs(combined_df, new_variants_report, output_file, new_variants_file)
    print(f"Runs successfully added: {', '.join(added_files)}")
    print(f"Updated master line list saved to {output_file}")
    print(f"New variants report saved to {new_variants_file}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python add_new_run_to_master.py <master_file> <new_run_dir> <output_file> <new_variants_file>")
        sys.exit(1)
    main(*sys.argv[1:])
