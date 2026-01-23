"""PDF parsing module for extracting text from astrology chart PDFs."""

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract all text content from an uploaded PDF file.

    Args:
        pdf_file: Streamlit UploadedFile object

    Returns:
        Extracted text content as a string

    Raises:
        ValueError: If PDF is empty or cannot be read
    """
    try:
        # Read PDF bytes from uploaded file
        pdf_bytes = pdf_file.read()

        # Open PDF with PyMuPDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        # Extract text from all pages
        text_content = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_content.append(f"--- Page {page_num + 1} ---\n{text}")

        doc.close()

        if not text_content:
            raise ValueError("No text content found in PDF. The file may be image-based or empty.")

        return "\n\n".join(text_content)

    except fitz.fitz.FileDataError:
        raise ValueError("Unable to read PDF file. Please ensure it's a valid PDF.")
    except Exception as e:
        if "No text content" in str(e):
            raise
        raise ValueError(f"Error processing PDF: {str(e)}")
