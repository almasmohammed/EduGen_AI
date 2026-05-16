import io
from pathlib import Path


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes. Falls back gracefully."""
    text = ""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                pages.append(t.strip())
        text = "\n\n".join(pages)
    except ImportError:
        raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")
    except Exception as e:
        raise ValueError(f"Could not read PDF: {e}")

    if not text.strip():
        raise ValueError("PDF appears to be empty or image-based (no extractable text).")
    return text
