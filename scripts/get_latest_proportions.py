import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def read_files(input_file_1, master_file):
    data = pd.read_csv(input_file_1, index_col=['variant'])
    data = data.T
    master_line_list = pd.read_csv(master_file, low_memory=False)
    return data, master_line_list

def get_last_8_weeks(data):
    last_8_weeks = data.tail(7)
    return last_8_weeks

def drop_old_variants(last_8_weeks):
    cleaned = last_8_weeks.loc[:, (last_8_weeks !=0).any(axis=0)]
    cleaned = cleaned * 100
    cleaned = cleaned.round(3)
    cleaned.to_csv("results/latest_proportions.csv")
    return cleaned

def get_top_variants(cleaned, top_n=3):
    # Compute the mean proportion for each variant and sort
    mean_proportions = cleaned.mean(axis=0).sort_values(ascending=False)
    top_variants = mean_proportions.head(top_n).index
    return cleaned[top_variants], top_variants

def transform_data(cleaned):
    heatmap_data = cleaned.T
    heatmap_data.to_csv("results/heatmap_data.csv")
    return heatmap_data

def create_heatmap(heatmap_data, output_1):
    plt.figure(figsize=(12,8))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="Blues", cbar_kws={'label': 'Proportion (%)'})
    plt.title('Heatmap of Variant Proportions in Wastewater from Last 8 Weeks')
    plt.xlabel('Sample Collection Date by Week')
    plt.ylabel('Variant')
    plt.tight_layout()
    plt.savefig(output_1)
    plt.close()

def create_line_graph(cleaned, top_variants, master_line_list, output_2):
    hex_codes = dict(zip(master_line_list['variant'], master_line_list['hex_code']))
    plt.figure(figsize=(12,8))
    for variant in top_variants:
        plt.plot(cleaned.index, cleaned[variant], label=variant, color=hex_codes.get(variant, 'black'))
        last_x = cleaned.index[-1]
        last_y = cleaned[variant].iloc[-1]
        plt.text(last_x, last_y, f"{variant}", fontsize=8, ha='left', va='center')
    plt.title('Line Graph of Top Variant Proportions in Wastewater from Last 8 Weeks')
    plt.ylabel('Proportion (%)')
    plt.xlabel('Sample Collection Date by Week')
    plt.xticks(rotation=45)
    plt.legend(title='Variant', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(output_2)
    plt.close()

def main(input_file_1, master_file, output_1, output_2):
    data, master_line_list = read_files(input_file_1, master_file)
    last_8_weeks = get_last_8_weeks(data)
    cleaned = drop_old_variants(last_8_weeks)
    top_variants_data, top_variants = get_top_variants(cleaned, top_n=3)
    heatmap_data = transform_data(cleaned)
    create_heatmap(heatmap_data, output_1)
    create_line_graph(cleaned, top_variants, master_line_list, output_2)
    print("proportions table and graphs generated")

if __name__ == "__main__":
    if len(sys.argv) !=5:
        print("Usage: python3 ./scripts/get_latest_proportions.py results/proportions_table.csv <master_line_list> results/heatmap_latest_proportions.jpg results/line_graph_latest_proportions.jpg")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
