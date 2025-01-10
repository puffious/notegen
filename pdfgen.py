from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
import requests
import re

def download_font(font_name):
    # Create fonts directory if it doesn't exist
    os.makedirs('fonts', exist_ok=True)
    font_path = f'fonts/{font_name}-Regular.ttf'
    
    # Only download if font doesn't exist
    if not os.path.exists(font_path):
        font_url = f"https://cdn.jsdelivr.net/gh/googlefonts/noto-fonts@main/unhinted/ttf/Noto{font_name}/Noto{font_name}-Regular.ttf"
        try:
            response = requests.get(font_url)
            response.raise_for_status()
            with open(font_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded font: {font_name}")
        except Exception as e:
            print(f"Error downloading font {font_name}: {e}")
            return None
    return font_path

def clean_text(text):
    # First handle HTML-style bold and italic formatting
    text = re.sub(r'<b>(.*?)</b>', r'<b>\1</b>', text)  # Keep HTML bold tags
    text = re.sub(r'<i>(.*?)</i>', r'<i>\1</i>', text)  # Keep HTML italic tags
    
    # Then handle markdown-style formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Convert markdown bold to HTML
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)      # Convert markdown italic to HTML
    
    # Handle special characters (but not inside HTML tags)
    parts = re.split(r'(<[^>]*>)', text)
    for i in range(0, len(parts), 2):  # Only process text outside of tags
        parts[i] = parts[i].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = ''.join(parts)
    
    # Split into paragraphs first
    paragraphs = text.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    # Process bullet points
    processed_paragraphs = []
    for p in paragraphs:
        if p.startswith('* '):
            # Handle bullet point paragraphs
            lines = p.split('\n')
            bullet_points = []
            for line in lines:
                if line.strip().startswith('* '):
                    # Remove the asterisk and add bullet point
                    point = line.strip()[2:]
                    bullet_points.append(point)
            # Join bullet points with proper formatting
            bullet_list = '<br/>'.join(f'• {point}' for point in bullet_points)
            processed_paragraphs.append(bullet_list)
        elif p.startswith('•'):
            # Already formatted bullet points
            processed_paragraphs.append(p)
        else:
            processed_paragraphs.append(p)
    
    return processed_paragraphs

def create_pdf(text, pdf_filename, language):
    # Create a PDF document
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Set up styles
    styles = getSampleStyleSheet()
    
    # Select font based on language
    if language.lower() == "gujarati":
        FONT = "SansGujarati"
    elif language.lower() == "english":
        FONT = "Sans"
    else:  # Default to Hindi font
        FONT = "SansDevanagari"

    try:
        # Download and register the font
        font_path = download_font(FONT)
        if font_path:
            pdfmetrics.registerFont(TTFont(FONT, font_path))
        else:
            FONT = "Helvetica"
    except Exception as e:
        print(f"Error loading font: {e}")
        FONT = "Helvetica"

    # Define styles
    normal_style = ParagraphStyle(
        'normal',
        parent=styles['Normal'],
        fontName=FONT,
        fontSize=12,
        leading=16,
        spaceAfter=12,
        encoding='utf-8',
        wordWrap='CJK'
    )
    
    list_style = ParagraphStyle(
        'list',
        parent=normal_style,
        leftIndent=20,
        firstLineIndent=0,
        spaceBefore=10,
        spaceAfter=10
    )
    
    # Create a list to hold the content
    content = []
    
    # Process the text
    paragraphs = clean_text(text)
    
    # Add paragraphs to content
    for paragraph in paragraphs:
        try:
            if paragraph.startswith('•'):
                p = Paragraph(paragraph, list_style)
            else:
                p = Paragraph(paragraph, normal_style)
            content.append(p)
            content.append(Spacer(1, 12))  # Add space between paragraphs
        except Exception as e:
            print(f"Error processing paragraph: {e}")
            content.append(Paragraph(str(paragraph), styles['Normal']))
    
    # Build the PDF
    try:
        doc.build(content)
        print(f"PDF successfully created: {pdf_filename}")
    except Exception as e:
        print(f"Error building PDF: {e}")
        try:
            # Fallback to basic style
            doc.build([Paragraph(p, styles['Normal']) for p in paragraphs])
            print(f"PDF created with fallback style: {pdf_filename}")
        except Exception as e:
            print(f"Failed to create PDF even with fallback style: {e}")

if __name__ == "__main__":
    text = "Test"
    pdf_filename = "downloads/output_reportlab.pdf"
    language = "english"
    create_pdf(text, pdf_filename, language)