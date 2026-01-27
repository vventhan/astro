"""File processing module for birth chart files."""

import fitz  # PyMuPDF

# Supported file types
SUPPORTED_TYPES = {
    "pdf": "application/pdf",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
}

# Image types (require multimodal processing)
IMAGE_TYPES = {"png", "jpg", "jpeg", "webp"}

# Minimum text length to consider extraction successful
MIN_TEXT_LENGTH = 100


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file using PyMuPDF.

    Args:
        file_bytes: Raw bytes of the PDF file

    Returns:
        Extracted text, or empty string if extraction fails
    """
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = []

        for page in doc:
            text = page.get_text()
            if text:
                text_parts.append(text)

        doc.close()
        return "\n\n".join(text_parts)

    except Exception:
        return ""


def process_uploaded_file(uploaded_file) -> tuple[bytes, str, str]:
    """
    Process an uploaded file and return bytes, mime type, and extracted text.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        Tuple of (file_bytes, mime_type, extracted_text)
        - extracted_text will be empty string for images or if PDF extraction fails

    Raises:
        ValueError: If file type is not supported
    """
    # Get file extension
    filename = uploaded_file.name.lower()
    ext = filename.rsplit(".", 1)[-1] if "." in filename else ""

    if ext not in SUPPORTED_TYPES:
        raise ValueError(f"Unsupported file type: {ext}. Supported: PDF, PNG, JPG, WEBP")

    mime_type = SUPPORTED_TYPES[ext]
    file_bytes = uploaded_file.read()

    if not file_bytes:
        raise ValueError("File is empty")

    # Extract text only for PDFs
    extracted_text = ""
    if ext == "pdf":
        extracted_text = extract_text_from_pdf(file_bytes)
        # If extraction returned very little text, it's likely an image-based PDF
        if len(extracted_text.strip()) < MIN_TEXT_LENGTH:
            extracted_text = ""

    return file_bytes, mime_type, extracted_text


def is_text_extraction_available(extracted_text: str) -> bool:
    """Check if we have usable extracted text."""
    return len(extracted_text.strip()) >= MIN_TEXT_LENGTH
