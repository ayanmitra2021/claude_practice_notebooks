from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path
from pydantic import Field

SUPPORTED_EXTENSIONS = {".docx", ".pdf"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(
        description="Absolute or relative path to a .docx or .pdf file to convert"
    ),
) -> str:
    """Convert a DOCX or PDF file on disk to markdown-formatted text.

    Reads the file at the given path and returns its contents as markdown.
    Delegates conversion to the markitdown library.

    When to use:
    - When you have a filesystem path to a Word document or PDF
    - When you need to extract readable text from a binary document format

    When NOT to use:
    - When you already have the file contents in memory as bytes (use binary_document_to_markdown instead)
    - For file types other than .docx and .pdf

    Examples:
    >>> document_path_to_markdown("/reports/summary.pdf")
    "# Summary\\n\\nThis report covers..."
    >>> document_path_to_markdown("./docs/spec.docx")
    "# Specification\\n\\n## Overview\\n..."
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"No file found at: {file_path}")

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{path.suffix}'. Must be one of: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    return binary_document_to_markdown(path.read_bytes(), path.suffix.lstrip("."))
