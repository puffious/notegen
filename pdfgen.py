from fpdf import FPDF

def create_pdf_from_string(text, pdf_filename):
    # Create an instance of FPDF class
    pdf = FPDF()
    
    # Add a page
    pdf.add_page()
    
    # Set font (Arial, bold, size 12)
    pdf.set_font("Arial", size=12)
    
    # Add the text (auto-wraps lines)
    pdf.multi_cell(0, 10, text)
    
    # Save the PDF to a file
    pdf.output(pdf_filename)

# Example usage
if __name__ == "__main__":
    text = "This is a sample string that will be written to the PDF."
    pdf_filename = "output.pdf"
    create_pdf_from_string(text, pdf_filename)
