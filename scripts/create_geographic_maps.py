import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
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
    Generates Maps of the dominant variant for each two-week period over the past three months.

    Parameters:
        master_line_list_path (str): Path to the master line list CSV file.
        shapefile_path (str): Path to the shapefile for Washington State counties.
        output_file_prefix (str): Prefix for the output map file.
    """
    # Step 1: Read the files
    master_line_list, wa_shape = read_files(master_line_list_path, shapefile_path)
    master_line_list = master_line_list.rename(columns={"location": "county"})
    master_line_list['Sample_Collection_Date'] = pd.to_datetime(master_line_list['Sample_Collection_Date'], errors='coerce')
    wa_shape = wa_shape.rename(columns={"JURISDIC_3": "county"})  # Ensure consistent naming
    wa_shape['county'] = wa_shape['county'].str.title()  # Normalize county names
    master_line_list['county'] = master_line_list['county'].str.title()  # Normalize county names

    # Step 2: Filter for data from the last three months
    current_date = pd.Timestamp.now()
    start_date = current_date - timedelta(weeks=12)
    recent_data = master_line_list[master_line_list['Sample_Collection_Date'] >= start_date]

    # Step 3: Generate two-week intervals
    recent_data['Two_Week_Interval'] = recent_data['Sample_Collection_Date'].dt.to_period('W-SUN')
    intervals = sorted(recent_data['Two_Week_Interval'].unique(), key=lambda x: x.start_time)

    # Step 4: Create maps for each two-week interval
    rows = (len(intervals) + 3) // 4  # Number of rows for the grid
    cols = 4  # Fixed number of columns
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 10, rows * 10))
    axes = axes.flatten()

    for ax, interval in zip(axes, intervals):
        print(f"Processing interval: {interval} ({interval.start_time} to {interval.end_time})...")
        interval_data = recent_data[recent_data['Two_Week_Interval'] == interval]

        # Aggregate by county
        county_aggregates = interval_data.groupby(['county', 'variant']).agg({
            'Variant_proportion': 'sum',
            'hex_code': 'first'
        }).reset_index()

        # Normalize proportions and find dominant variants
        county_aggregates['normalized_proportion'] = county_aggregates.groupby('county')['Variant_proportion'].transform(lambda x: x / x.sum())
        dominant_variants = county_aggregates.loc[county_aggregates.groupby('county')['normalized_proportion'].idxmax()]

        # Merge with shapefile
        interval_shape = wa_shape.merge(
            dominant_variants[['county', 'variant', 'hex_code']],
            on='county',
            how='left'
        )
        interval_shape.to_csv('results/interval_shape.csv')
        #variant_to_hex = dict(zip(interval_shape['variant'], interval_shape['hex_code']))
        #interval_shape['hex_code'] = interval_shape['variant'].map(variant_to_hex)
        # Assign default gray color for counties without data
        interval_shape['hex_code'] = interval_shape['hex_code'].fillna('#D3D3D3')

        # Plot the map
        interval_shape.plot(ax=ax, color=interval_shape['hex_code'], edgecolor='black')
        ax.set_title(f"Dominant Variants\n{interval.start_time.strftime('%b %d')} - {interval.end_time.strftime('%b %d')}", fontsize=24)
        ax.axis('off')

    all_variants = recent_data[['variant', 'hex_code']].drop_duplicates().sort_values(by='variant')

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label=variant, markersize=14, markerfacecolor=color)
        for variant, color in zip(all_variants['variant'].unique(), all_variants['hex_code'])
    ]
    # add legend
    fig.legend(
        handles=legend_elements,
        title_fontsize=18,
        title="Variants",
        #bbox_to_anchor=(1.05, 1.05),
        loc='lower right',
        #borderaxespad=1.5,
        prop={'size': 24},
        markerscale=2,
        #frameon=True,
        #fancybox=True,
        #shadow=True,
        ncol=4,
        fontsize=24
        )

    # Remove unused subplots
    for ax in axes[len(intervals):]:
        fig.delaxes(ax)

    plt.subplots_adjust(top=0.9)
    # Adjust layout and save the combined map
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    plt.close()
    print(f"Maps of dominant variants saved to {output}")


# Main function to run the script
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python generate_wa_maps.py <master_line_list_path> <shapefile_path> results/wa_geographic_map_dominant_variants_last_3_months.jpg")
        sys.exit(1)

    master_line_list_path = sys.argv[1]
    shapefile_path = sys.argv[2]
    output = sys.argv[3]

    create_geographic_maps(master_line_list_path, shapefile_path, output)
