import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sys

def read_files(master_line_list_path):
    master = pd.read_csv(master_line_list_path, low_memory=False)
    return master

def grab_data(master):
    master['Sample_Collection_Date'] = pd.to_datetime(master['Sample_Collection_Date'], errors='coerce')
    data_2024 = master.loc[(master['Sample_Collection_Date'].dt.year >= 2024) & (master['Sample_Collection_Date'].dt.year <= 2025)]
    weeks_2024 = pd.date_range(start='2024-01-01', end='2025-12-31', freq='W-MON')
    week_labels = [date.strftime('%Y-W%U') for date in weeks_2024]
    data_2024['Week'] = data_2024['Sample_Collection_Date'].dt.strftime('%Y-W%U')
    return data_2024, week_labels

def earliest_detection(data_2024):
    detection_span = data_2024.groupby(['variant', 'hex_code'])['Week'].agg(['min', 'max']).reset_index()
    detection_span.columns = ['Variant', 'Hex_Code', 'First_Week', 'Last_Week']
    return detection_span

def plot_timeline(detection_span, week_labels, output):
    detection_span['Start_Week_Index'] = detection_span['First_Week'].map(lambda x: week_labels.index(x))
    detection_span['End_Week_Index'] = detection_span['Last_Week'].map(lambda x: week_labels.index(x))
    plt.figure(figsize=(10, 8))
    for _, row in detection_span.iterrows():
        plt.barh(
            row['Variant'],
            row['End_Week_Index'] - row['Start_Week_Index'] + 1,  # Add 1 to include the last week
            left=row['Start_Week_Index'],
            color=row['Hex_Code']
            )
    plt.grid(axis='x', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.xticks(range(len(week_labels)), week_labels, rotation=90)
    plt.xlabel('Weeks in 2024')
    plt.ylabel('Variant')
    plt.title('Detection of Variants in 2024-2025')
    plt.tight_layout()
    plt.savefig(output)
    plt.close()

def main(master_line_list_path, output):
    master = read_files(master_line_list_path)
    data_2024, week_labels = grab_data(master)
    detection_span = earliest_detection(data_2024)
    plot_timeline(detection_span, week_labels, output)
    print("Timeline Generated")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 <script> <master> results/timeline.jpg")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
