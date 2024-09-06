from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

def create_pdf(text, pdf_filename, language):
    # Create a PDF document
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    
    # Set up styles
    styles = getSampleStyleSheet()
    
    # Select font based on language
    if language.lower() == "gujarati":
        FONT = "NotoSansGujarati"
    elif language.lower() == "english":
        FONT = "NotoSansGujarati"
    else:  # Default to Hindi font
        FONT = "NotoSansDevanagari"

    try:
        # Register the font
        pdfmetrics.registerFont(TTFont(FONT, f'fonts/{FONT}-Regular.ttf'))
    except Exception as e:
        print(f"Error loading font: {e}")
        return

    # Define custom style with the selected font
    custom_style = ParagraphStyle(
        'custom',
        parent=styles['Normal'],
        fontName=FONT,
        fontSize=14,
        leading=16,
        spaceAfter=12
    )
    
    # Create a list to hold the content
    content = []
    
    # Split the text into paragraphs and add each to the content list
    paragraphs = text.split("\n")
    for paragraph in paragraphs:
        p = Paragraph(paragraph, custom_style)
        content.append(p)
    
    # Build the PDF with the content
    doc.build(content)
    print(f"PDF successfully created: {pdf_filename}")

# Example usage
if __name__ == "__main__":
    text = "Test"
    pdf_filename = "downloads/output_reportlab.pdf"
    language = "english"
    create_pdf(text, pdf_filename, language)
2