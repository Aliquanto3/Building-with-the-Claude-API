from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path

from pydantic import Field

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(
        description="Absolute or relative path to a PDF or DOCX file to convert."
    ),
) -> str:
    """Convert a PDF or DOCX file on disk to markdown-formatted text.

    Reads the file at the given path and returns its contents as markdown.

    When to use:
    - When the user provides a file path to a PDF or DOCX document
    - When you need to extract readable text from a document on the filesystem

    When NOT to use:
    - When you already have the file contents as bytes (use binary_document_to_markdown)
    - For file types other than .pdf and .docx

    Examples:
    >>> document_path_to_markdown("/docs/report.pdf")
    "# Report Title\\n\\nContent..."
    >>> document_path_to_markdown("notes.docx")
    "# Notes\\n\\n- Item one..."
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(
            f"Unsupported file type '{ext}'. Supported types: {supported}"
        )

    return binary_document_to_markdown(path.read_bytes(), ext.lstrip("."))
