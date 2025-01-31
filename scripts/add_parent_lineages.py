import pandas as pd

def load_data(master_file, lineage_file):
    # Load the updated WW master file and lineage classifications
    master_df = pd.read_csv(master_file, low_memory=False)
    lineage_df = pd.read_csv(lineage_file)

    return master_df, lineage_df

def add_lineages(master_df, lineage_df):
    # Merge with lineage classifications to add parent lineage and hex code
    enriched_df = master_df.merge(
        lineage_df[['wastewater_variant_name', 'lineage_extracted', 'hex_code']],
        how='left',
        left_on='Variant_name',
        right_on='lineage_extracted'
    ).rename(columns={'wastewater_variant_name': 'variant'})  # Rename for clarity

    # Drop any unnecessary columns after merge
    enriched_df = enriched_df.drop(columns=['lineage_extracted'])
    return enriched_df

def save_output(enriched_df, output_file):
    # Save the enriched master file as WW_data.csv
    enriched_df.to_csv(output_file, index=False)
    print(f"Enriched data with parent lineages and hex codes saved to {output_file}")

def main(master_file, lineage_file, output_file):
    master_df, lineage_df = load_data(master_file, lineage_file)
    enriched_df = add_lineages(master_df, lineage_df)
    save_output(enriched_df, output_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python add_parent_lineages.py <master_file> <lineage_file> <output_file>")
        sys.exit(1)
    main(*sys.argv[1:])
