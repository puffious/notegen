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
    text = """तुम कैसे हो? आशा है कि तुम मस्त हो और तुम्हारी तबियत भी अच्छी हो।
    CS50 Final Lecture Notes: Cybersecurity & Wrap-Up
    This lecture focused on cybersecurity and provided practical tips for students leaving CS50 and entering the real world.
    Key Takeaways:
    - Cybersecurity is about protecting systems, data, and accounts from attacks.
    - Humans are bad at choosing passwords, leading to easily compromised accounts.
    - Brute-force attacks exploit weak passwords, especially those with simple patterns.
    - Longer and more random passwords are essential, but remembering them can be challenging.
    - Password managers are valuable tools for generating and storing strong passwords, but rely on a single master password.
    - Two-Factor Authentication (2FA) adds an extra layer of security by requiring a second factor (phone, app, or biometric) in addition to a password.
    - Hashing is a one-way function that transforms passwords into seemingly random strings, making them difficult to reverse engineer.
    - Rainbow tables pre-compute hashes to try and reverse engineer passwords, but become impractical with long and complex passwords.
    - Salting adds a random value to passwords before hashing, making it harder for attackers to find duplicates.
    - Cryptography scrambles information in a reversible way, unlike hashing.
    - Symmetric cryptography uses the same key for encryption and decryption.
    - Asymmetric cryptography (Public Key Cryptography) uses a key pair (public and private), allowing communication without prior secret sharing.
    - Passkeys are a new passwordless login system that relies on public and private key pairs and digital signatures.
    - End-to-end encryption protects communication from even the service provider, ensuring privacy.
    - Securely deleting files involves overwriting the original data with random values to prevent recovery.
    - Full disk encryption scrambles all data on a device, requiring a password to access.
    Actionable Takeaways:
    1. Use a password manager or passkeys for sensitive accounts.
    2. Enable two-factor authentication whenever possible.
    3. Use end-to-end encryption for communication and data storage.
    Final Quiz Show:
    - Participants answered multiple choice questions on cybersecurity and CS50 concepts.
    - The winning guest user online scored a perfect 16,000 points.
    - A human volunteer from the audience won with the highest score (17,292).
    The lecture ended with a celebration of CS50's success, thanking the staff and volunteers.
    Final Message:
    CS50 equips students with the knowledge and skills to solve problems and navigate the evolving world of technology. The course emphasizes critical thinking, algorithmic problem-solving, and practical application of coding skills. Students are encouraged to stay connected with the CS50 community, seek out further learning opportunities, and continue to explore the exciting possibilities of computer science."""
    
    pdf_filename = "downloads/output_reportlab.pdf"
    language = "hindi"
    create_pdf(text, pdf_filename, language)
