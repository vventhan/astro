"""File processing module for birth chart files."""

import io
import fitz  # PyMuPDF
import easyocr

# Supported file types
SUPPORTED_TYPES = {
    "pdf": "application/pdf",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
}

# Image types (require OCR)
IMAGE_TYPES = {"png", "jpg", "jpeg", "webp"}

# Minimum text length to consider extraction successful
MIN_TEXT_LENGTH = 100

# Lazy-loaded OCR reader (downloads models on first use)
_ocr_reader = None


def get_ocr_reader():
    """Get or create the OCR reader (lazy initialization)."""
    global _ocr_reader
    if _ocr_reader is None:
        _ocr_reader = easyocr.Reader(['en'], gpu=False)
    return _ocr_reader


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


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from an image using EasyOCR.

    Args:
        image_bytes: Raw bytes of the image

    Returns:
        Extracted text, or empty string if extraction fails
    """
    try:
        reader = get_ocr_reader()
        # EasyOCR can read from bytes directly
        results = reader.readtext(image_bytes, detail=0, paragraph=True)
        return "\n".join(results)
    except Exception:
        return ""


def extract_text_from_pdf_images(file_bytes: bytes) -> str:
    """
    Extract text from a PDF by converting pages to images and using OCR.
    Used for image-based PDFs where PyMuPDF text extraction fails.

    Args:
        file_bytes: Raw bytes of the PDF file

    Returns:
        Extracted text, or empty string if extraction fails
    """
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        all_text = []

        for page in doc:
            # Render page to image (higher DPI for better OCR)
            mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")

            # OCR the image
            page_text = extract_text_from_image(img_bytes)
            if page_text:
                all_text.append(page_text)

        doc.close()
        return "\n\n".join(all_text)

    except Exception:
        return ""


def process_uploaded_file(uploaded_file) -> tuple[bytes, str, str]:
    """
    Process an uploaded file and return bytes, mime type, and extracted text.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        Tuple of (file_bytes, mime_type, extracted_text)
        - extracted_text will be empty string if all extraction methods fail

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

    extracted_text = ""

    if ext == "pdf":
        # Try PyMuPDF text extraction first (fast)
        extracted_text = extract_text_from_pdf(file_bytes)

        # If insufficient text, try OCR on PDF pages
        if len(extracted_text.strip()) < MIN_TEXT_LENGTH:
            extracted_text = extract_text_from_pdf_images(file_bytes)

    elif ext in IMAGE_TYPES:
        # Use OCR for images
        extracted_text = extract_text_from_image(file_bytes)

    return file_bytes, mime_type, extracted_text


def is_text_extraction_available(extracted_text: str) -> bool:
    """Check if we have usable extracted text."""
    return bool(extracted_text) and len(extracted_text.strip()) >= MIN_TEXT_LENGTH
