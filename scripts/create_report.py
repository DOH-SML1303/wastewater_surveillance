import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image

def read_files(input_file_1, input_file_2):
    im = input_file_1
    table = pd.read_csv(input_file_2)
    return im, table

pdf_filename = "results/latest_sc2_variants_ww.pdf"

def create_pdf_with_plot_and_table(pdf_filename, im, table):

    # Set up the canvas
    pdf_canvas = canvas.Canvas(pdf_filename, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Add a title
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(100, height - 50, "Latest SC2 Variant Proportions in the Wastewater")

    # Add the plot image to the PDF
    img = Image(im)
    img.drawHeight = 5 * 72  # 5 inches height
    img.drawWidth = 9 * 72   # 7 inches width
    img.wrapOn(pdf_canvas, 9 * 72, 5 * 72)
    img.drawOn(pdf_canvas, 50, height - 450)  # Position the image on the page

    table_data = [table.columns.tolist()] + table.values.tolist()

    num_columns = len(table.columns)
    col_width = (width - 100) / num_columns
    col_widths = [col_width] * num_columns

    table = Table(table_data, colWidths=col_widths)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0,0), (-1, -1), 5),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    table.wrapOn(pdf_canvas, 400, 200)
    table.drawOn(pdf_canvas, 50, height - 600)  # Position the table on the page

    # Save the PDF
    pdf_canvas.save()

def main(input_file_1, input_file_2, output_file):
    im, table = read_files(input_file_1, input_file_2)
    create_pdf_with_plot_and_table(pdf_filename, im, table)
    print("Report Generated")

if __name__ == "__main__":
    if len(sys.argv) !=4:
        print("Usage: python3 ./scripts/create_report.py results/proportions_plot.jpg results/latest_proportions.csv results/latest_sc2_variants_ww.pdf")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
