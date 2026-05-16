import os
from dotenv import load_dotenv

load_dotenv()


def truncate_text(text: str, max_chars: int = 300) -> str:
    """Truncate text for preview display."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "…"


def detect_file_type(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "txt"
    return ext


def check_api_keys() -> dict:
    """Return dict showing which API keys are configured."""
    return {
        "groq": bool(os.getenv("GROQ_API_KEY")),
        "openai": bool(os.getenv("OPENAI_API_KEY")),
    }


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Route to correct parser based on file extension."""
    file_type = detect_file_type(filename)

    if file_type == "pdf":
        from utils.pdf_parser import extract_text_from_pdf
        return extract_text_from_pdf(file_bytes)
    elif file_type == "docx":
        from utils.docx_parser import extract_text_from_docx
        return extract_text_from_docx(file_bytes)
    elif file_type in ("txt", "md"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: .{file_type}. Please upload PDF, DOCX, or TXT files.")


def format_score_badge(score: int, total: int) -> str:
    pct = score / max(total, 1) * 100
    if pct >= 80:
        return f"🟢 {score}/{total} ({pct:.0f}%)"
    elif pct >= 50:
        return f"🟡 {score}/{total} ({pct:.0f}%)"
    else:
        return f"🔴 {score}/{total} ({pct:.0f}%)"
