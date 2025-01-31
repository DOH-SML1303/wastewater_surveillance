import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.lines import Line2D

def read_files(master_line_list_path, shapefile_path):
    """
    Reads the master line list CSV file and Washington shapefile.

    Parameters:
        master_line_list_path (str): Path to the master line list CSV file.
        shapefile_path (str): Path to the shapefile for Washington State counties.

    Returns:
        tuple: A tuple containing:
            - DataFrame with the master line list.
            - GeoDataFrame with the shapefile data.
    """
    try:
        # Read the master line list
        master_line_list = pd.read_csv(master_line_list_path, low_memory=False)
        print(f"Master line list loaded successfully with {len(master_line_list)} records.")

        # Read the shapefile
        shapefile = gpd.read_file(shapefile_path)
        print(f"Shapefile loaded successfully with {len(shapefile)} features.")
        return master_line_list, shapefile

    except Exception as e:
        print(f"Error reading files: {e}")
        raise


def create_geographic_maps(master_line_list_path, shapefile_path, output):
    """
    Generate two maps for Washington State:
    1. Gradient map showing sample representation by county.
    2. Pie chart map showing lineages grouped by county for 2024.

    Parameters:
        master_line_list_path (str): Path to the master line list CSV file.
        shapefile_path (str): Path to the shapefile for Washington State counties.
        output: Path to gradient map
    """
    # Step 1: Read the files
    master_line_list, wa_shape = read_files(master_line_list_path, shapefile_path)
    master_line_list = master_line_list.rename(columns={"location" : "county"})
    # Step 2: Filter for 2024 and Washington State
    master_line_list['Sample_Collection_Date'] = pd.to_datetime(master_line_list['Sample_Collection_Date'], errors='coerce')
    data_2024 = master_line_list[
        (master_line_list['State'] == 'WA') &
        (master_line_list['Sample_Collection_Date'].dt.year >= 2024) &
        (master_line_list['Sample_Collection_Date'].dt.year <= 2025)
    ]

    # Aggregate data for plotting
    county_counts = data_2024.groupby('county')['Sample_ID'].nunique().reset_index()#name='sample_count')
    county_counts.columns = ['county', 'sample_count']
    county_lineages = data_2024.groupby(['county', 'variant']).size().unstack(fill_value=0)
    county_coordinates = data_2024.groupby('county')[['latitude', 'longitude']].mean().reset_index()

    county_counts.to_csv("results/county_counts.csv")
    county_coordinates.to_csv("results/county_coordinates.csv")
    county_lineages.to_csv("results/county_lineages.csv")
    # Merge shapefile and master line list data
    wa_shape = wa_shape.rename(columns={"JURISDIC_3": "county"})  # Ensure consistent naming
    wa_shape['county'] = wa_shape['county'].str.title()  # Normalize county names
    data_2024['county'] = data_2024['county'].str.title()  # Normalize county names
    merged_data = wa_shape.merge(data_2024, on="county", how="left")  # Merge for complete data

    # 4. Create the gradient map
    print("Creating gradient map...")
    fig, ax = plt.subplots(figsize=(12, 8))
    wa_shape = wa_shape.merge(county_counts, on="county", how="left").fillna(0)
    wa_shape.to_csv("results/wa_shape.csv")
    wa_shape.plot(column='sample_count', ax=ax, cmap='Blues', legend=True,
                  edgecolor='black', legend_kwds={'label': "Number of Samples"})
    plt.title("Sample Representation by County in Washington State (2024-2025)", fontsize=16)
    plt.savefig(output, bbox_inches="tight")
    plt.close()
    print(f"Gradient map saved to {output}")


# Main function to run the script
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python generate_wa_maps.py <master_line_list_path> <shapefile_path>")
        sys.exit(1)

    master_line_list_path = sys.argv[1]
    shapefile_path = sys.argv[2]
    output = sys.argv[3]

    create_geographic_maps(master_line_list_path, shapefile_path, output)
