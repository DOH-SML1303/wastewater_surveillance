import sys
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import glob

# Load data
def read_files(input_file):
    """
    Reads in the input tsv files
    """
    data = pd.read_csv(input_file, sep="\t")
    return data

# Check for missing data and unique identifiers, return report
def check_and_report(data, report):
    """
    Check the sample ID, sample collection date, sample site, variant name, and pipeline columns
    for unique number of counts and any missing data for those columns
    """
    columns_to_check = ['Sample_ID', 'Sample_Collection_Date', 'Sample_Site', 'Variant_name', 'Pipeline_date']
    summary = []
    # this for loop checks all of the specified columns for missing data and unique counts
    # both unique and missing data will be included in a report and the report is what is being returned in this function
    # to be used for the variant_summary function

    for col in columns_to_check:
        unique_count = data[col].nunique()
        missing_count = data[col].isnull().sum()
        summary.append({'Column': col, 'Unique Count': unique_count, 'Missing Count': missing_count})
    report['Unique Identifiers Summary'] = pd.DataFrame(summary)

    missing_data = data[columns_to_check].isnull().sum()
    report['Missing Data Summary'] = pd.DataFrame(missing_data, columns=['Missing Count']).reset_index().rename(columns={'index': 'Column'})

    return report

# Variant distribution summary
def variant_summary(data, report):
    """
    This function gets a count of all of the variants that are found in the data.
    Sometimes there are different number of variants for each run, so we need a multi-column format
    that is flexible for listing all of the variants in a table without taking up so many pages
    """

    variant_counts = data['Variant_name'].value_counts().reset_index()
    variant_counts.columns = ['Variant', 'Count']

    # Reshape for multi-column format (e.g., 3 columns)
    num_cols = 3
    values = variant_counts.values.flatten()

    padding_needed = (num_cols * 2) - (len(values) % (num_cols * 2))
    if padding_needed != (num_cols * 2):
        values = list(values) + [None] * padding_needed

    variant_distribution = pd.DataFrame(
        np.array(values).reshape(-1, num_cols * 2),
        columns=[f'Variant_{i//2+1}' if i % 2 == 0 else f'Count_{i//2+1}' for i in range(num_cols * 2)]
    )

    report['Variant Distribution Summary'] = variant_distribution
    return report

# Sample completeness summary
def sample_completeness(data, report):
    site_summary = data.groupby(['Sample_Site', 'Sample_ID']).agg(
        Total_Samples=('Sample_ID', 'count'),
        Missing_Data_Count=('Variant_proportion', lambda x: x.isnull().sum())
    )
    report['Sample Completeness by Site'] = site_summary.reset_index()
    return report

def list_unique_identifiers(data, report):
    unique_sample_ids = pd.DataFrame(data['Sample_ID'].unique(), columns=['Unique Sample IDs'])
    unique_collection_dates = pd.DataFrame(data['Sample_Collection_Date'].unique(), columns=['Unique Collection Dates'])

    report['Unique Sample IDs'] = unique_sample_ids
    report['Unique Collection Dates'] = unique_collection_dates
    return report

def sample_date_discrepancies(data, report):
    sample_date_table = data.groupby('Sample_ID')['Sample_Collection_Date'].unique().reset_index()
    sample_date_table.columns = ['Sample_ID', 'Unique Collection Dates']
    report['Sample Date Discrepancies'] = sample_date_table
    return report

def total_relative_abundance_for_sample(data, report):
    relative_abundance_total = data.groupby(['Sample_ID', "Sample_Site"]).agg(
    Total_Relative_Abundance=('Variant_proportion', lambda x: x.sum())
    )
    report['Total Relative Abundance for Sample'] = relative_abundance_total.reset_index()
    return report

# Export to PDF
def export(report, output_pdf, input_file):
    file_name = os.path.basename(input_file).replace('.tsv', '')
    title_text = f"QC Report for {file_name}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with PdfPages(output_pdf) as pdf:
        fig, ax = plt.subplots(figsize=(10, 2))
        ax.text(0.5, 0.6, title_text, fontsize=16, ha='center', weight='bold')
        ax.text(0.5, 0.3, f"Generated on {timestamp}", fontsize=12, ha='center')
        ax.axis('off')
        pdf.savefig(fig, bbox_inches="tight")
        plt.close()

        for section_name, df in report.items():
            fig, ax = plt.subplots(figsize=(10, min(1 + len(df) * 0.25, 10)))
            ax.axis('off')
            ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
            plt.title(section_name, fontsize=14, weight='bold')
            pdf.savefig(fig, bbox_inches="tight")
            plt.close()

# Main function to process multiple files
def main(input_dir, output_dir):
    tsv_files = glob.glob(os.path.join(input_dir, "*.tsv"))

    for input_file in tsv_files:
        data = read_files(input_file)
        report = {}
        report = check_and_report(data, report)
        report = variant_summary(data, report)
        report = sample_completeness(data, report)
        report = list_unique_identifiers(data, report)
        report = sample_date_discrepancies(data, report)
        report = total_relative_abundance_for_sample(data, report)

        file_name = os.path.basename(input_file).replace('.tsv', '_QC_Report.pdf')
        output_pdf = os.path.join(output_dir, file_name)
        export(report, output_pdf, input_file)
        print(f"QC report generated for {input_file}: {output_pdf}")

# Run the script with command-line arguments
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python qc_check.py <input_directory> <output_directory>")
        sys.exit(1)
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)
    main(input_dir, output_dir)
