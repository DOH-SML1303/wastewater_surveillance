import sys
import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from datetime import datetime

def read_text(file_path):
    """Read a text file and return its content."""
    if not os.path.exists(file_path):
        print(f"Warning: Text file {file_path} not found. Skipping.")
        return "(Text description not available)"

    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading text file {file_path}: {e}")
        return "(Error loading text)"

def add_header_page(pdf_canvas, title, author):
    """Add a header page with title, timestamp, and author."""
    width, height = landscape(letter)
    pdf_canvas.setFont("Helvetica-Bold", 24)
    pdf_canvas.drawString(50, height - 150, title)

    pdf_canvas.setFont("Helvetica", 14)
    pdf_canvas.drawString(50, height - 200, f"Author: {author}")

    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(50, height - 220, f"Generated on: {datetime.now().strftime('%Y-%m-%d')}")

    pdf_canvas.showPage()

def add_text_and_plot(pdf_canvas, title, text, image_path, page_number):
    """Add a page with a title, plot, and text."""
    width, height = landscape(letter)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(50, height - 50, title)

    if os.path.exists(image_path):
        try:
            pdf_canvas.drawImage(image_path, 50, 200, width=700, height=400)
        except Exception as e:
            print(f"Error adding image {image_path}: {e}")
            pdf_canvas.drawString(50, 200, "(Image not available)")
    else:
        pdf_canvas.drawString(50, 200, "(Image not found)")

    # Add text below the image
    pdf_canvas.setFont("Helvetica", 10)
    text_y = 180  # Position text below the image
    for line in text.split("\n"):
        pdf_canvas.drawString(50, text_y, line)
        text_y -= 15

    pdf_canvas.setFont("Helvetica", 8)
    pdf_canvas.drawString(width - 100, 20, f"Page {page_number}")
    pdf_canvas.showPage()

def create_pdf(output, plots_texts, author):
    pdf_canvas = canvas.Canvas(output, pagesize=landscape(letter))

    # Add Header Page
    add_header_page(pdf_canvas, "SARS-CoV-2 Wastewater Sequencing Report", author)

    # Add each plot and corresponding text
    for i, (title, image_path, text) in enumerate(plots_texts, start=1):
        add_text_and_plot(pdf_canvas, title, text, image_path, i)

    pdf_canvas.save()
    print(f"PDF report generated successfully: {output}")

def main(output, input_files):
    plots_texts = [
        ("SC2 Variant Proportions Over Time", input_files["proportions_plot"], read_text(input_files["proportions_text"])) ,
        ("Heatmap of SC2 Variant Proportions", input_files["heatmap"], read_text(input_files["heatmap_text"])) ,
        ("Top SC2 Variant Trends", input_files["line_graph"], read_text(input_files["line_graph_text"])) ,
        ("SC2 Variant Detection Timeline", input_files["timeline"], read_text(input_files["timeline_text"])) ,
        ("Geographic Gradient Map of SC2 Variants", input_files["gradient_map"], read_text(input_files["gradient_map_text"])) ,
        ("Dominant SC2 Variants by County (Last 3 Months)", input_files["geographic_maps"], read_text(input_files["geographic_maps_text"])) ,
    ]

    create_pdf(output, plots_texts, author="Steph Lunn, MPH, MS")

if __name__ == "__main__":
    if len(sys.argv) != 14:
        print("Usage: python3 create_report.py <output_pdf> <proportions_plot> <proportions_text> <heatmap_plot> <heatmap_text> <line_graph_plot> <line_graph_text> <timeline_plot> <timeline_text> <gradient_map> <gradient_map_text> <dominant_variant_map> <dominant_variant_map_text>")
        sys.exit(1)

    output = sys.argv[1]
    input_files = {
        "proportions_plot": sys.argv[2],
        "proportions_text": sys.argv[3],
        "heatmap": sys.argv[4],
        "heatmap_text": sys.argv[5],
        "line_graph": sys.argv[6],
        "line_graph_text": sys.argv[7],
        "timeline": sys.argv[8],
        "timeline_text": sys.argv[9],
        "gradient_map": sys.argv[10],
        "gradient_map_text": sys.argv[11],
        "geographic_maps": sys.argv[12],
        "geographic_maps_text": sys.argv[13],
    }

    main(output, input_files)
