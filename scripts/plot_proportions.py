import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

def read_files(input_file_1):
    data_hexcodes = pd.read_csv(input_file_1, parse_dates=['Sample_Collection_Date'], low_memory=False)
    return data_hexcodes

def convert_dates(data_hexcodes):
    new_df = data_hexcodes.copy()
    new_df['Sample_Collection_Date'] = pd.to_datetime(new_df['Sample_Collection_Date'])
    new_df['ISO_Year'] = new_df['Sample_Collection_Date'].dt.isocalendar().year
    new_df['ISO_Month'] = new_df['Sample_Collection_Date'].dt.month
    new_df['ISO_Week'] = new_df['Sample_Collection_Date'].dt.isocalendar().week
    new_df['Date'] = new_df['ISO_Year'].astype(str) + '-' + new_df['ISO_Month'].astype(str).str.zfill(2) + '-W' + new_df['ISO_Week'].astype(str).str.zfill(2)
    return new_df

def aggregate_proportions(new_df):
    proportions = new_df.groupby(['Date', 'variant']).agg(
    {'Variant_proportion': 'sum', 'hex_code': 'first'}).reset_index()
    return proportions

def normalize_proportions(proportions):
    new_proportions_df = proportions.copy()
    new_proportions_df['Normalized_Proportion'] = new_proportions_df.groupby('Date')['Variant_proportion'].transform(lambda x: x /x.sum())
    return new_proportions_df

def pivot_to_table(new_proportions_df):
    pivot_table = new_proportions_df.pivot_table(index='Date', columns='variant', values='Normalized_Proportion', fill_value=0)
    transpose = pivot_table.T
    transpose.to_csv('results/proportions.csv')
    return pivot_table

def plot_figure(pivot_table, data_hexcodes):
    fig, ax = plt.subplots(figsize=(18,10))
    pivot_table.plot(kind='bar', stacked=True, ax=ax, width=0.8, color=[data_hexcodes[data_hexcodes['variant']== v]['hex_code'].unique()[0] for v in pivot_table.columns])
    plt.xlabel('Date')
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel('Normalized Proportion')
    plt.legend(title='Variant', bbox_to_anchor=(0.5, -0.3), loc='upper center', ncol=5, fontsize=8)
    plt.tight_layout(pad=2.0)
    plt.savefig('results/proportions_plot.jpg', bbox_inches='tight')

def main(input_file_1, output_file_1, output_file_2):
    data_hexcodes = read_files(input_file_1)
    new_df = convert_dates(data_hexcodes)
    proportions = aggregate_proportions(new_df)
    new_proportions_df = normalize_proportions(proportions)
    pivot_table = pivot_to_table(new_proportions_df)
    plot_figure(pivot_table, data_hexcodes)

if __name__ == "__main__":
    if len(sys.argv) !=4:
        print("Usage: python3 ./scripts/plot_proportions.py data/WW_data_hexcodes.csv results/proportions.csv results/proportions_plot.jpg")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])