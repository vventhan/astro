"""File processing module for birth chart files."""

# Supported file types
SUPPORTED_TYPES = {
    "pdf": "application/pdf",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
}


def process_uploaded_file(uploaded_file) -> tuple[bytes, str]:
    """
    Process an uploaded file and return bytes and mime type.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        Tuple of (file_bytes, mime_type)

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

    return file_bytes, mime_type
