import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

def read_files(input_file_1):
    line_list = pd.read_csv(input_file_1, parse_dates=['Sample_Collection_Date'], low_memory=False)
    return line_list

def aggregate_proportions(line_list):
    proportions = line_list.groupby(['Date', 'variant']).agg(
    {'normalize_proportions': 'sum', 'hex_code': 'first'}).reset_index()
    proportions = proportions.sort_values(by='Date').reset_index(drop=True)
    return proportions

def clean_proportions(proportions):
    proportions['Proportion_Percentages'] = (round(proportions['normalize_proportions'] * 100, 3))
    proportions.to_csv("results/proportions.csv")
    return proportions

def pivot_to_table(proportions):
    pivot_table = proportions.pivot_table(index='Date', columns='variant', values='normalize_proportions', fill_value=0)
    transpose = pivot_table.T
    transpose.to_csv('results/proportions_table.csv')
    return pivot_table

def plot_figure(pivot_table, line_list):
    fig, ax = plt.subplots(figsize=(18,10))
    pivot_table.plot(kind='bar', stacked=True, ax=ax, width=0.8, color=[line_list[line_list['variant']== v]['hex_code'].unique()[0] for v in pivot_table.columns])
    plt.xlabel('Week of Sample Collection Date')
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel('Normalized Proportion')
    plt.legend(title='Variant', bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=10, fontsize=8)
    plt.tight_layout(pad=2.0)
    plt.savefig('results/proportions_plot.jpg', bbox_inches='tight')

def main(input_file_1, output_file_1, output_file_2, output_file_3):
    line_list = read_files(input_file_1)
    proportions = aggregate_proportions(line_list)
    proportions = clean_proportions(proportions)
    pivot_table = pivot_to_table(proportions)
    plot_figure(pivot_table, line_list)

if __name__ == "__main__":
    if len(sys.argv) !=5:
        print("Usage: python3 ./scripts/plot_variant_props.py data/WW_data.csv results/proportions.csv results/proportions_table.csv results/proportions_plot.jpg")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
