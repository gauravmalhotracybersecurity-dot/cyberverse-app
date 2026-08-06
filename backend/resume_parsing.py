"""Extract plain text from an uploaded resume file (PDF, DOCX, or TXT)."""
import io

import docx
import pdfplumber
from fastapi import HTTPException, UploadFile

MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB


async def extract_resume_text(file: UploadFile) -> str:
    raw = await file.read()
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="File too large (5MB max).")

    filename = (file.filename or "").lower()

    if filename.endswith(".pdf"):
        text = _extract_pdf(raw)
    elif filename.endswith(".docx"):
        text = _extract_docx(raw)
    elif filename.endswith(".txt"):
        text = raw.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Upload a .pdf, .docx, or .txt file.",
        )

    text = text.strip()
    if len(text) < 50:
        raise HTTPException(
            status_code=400,
            detail="Couldn't extract enough text from this file. Try pasting the text instead.",
        )
    return text


def _extract_pdf(raw: bytes) -> str:
    try:
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(pages)
    except Exception:
        raise HTTPException(
            status_code=400, detail="Couldn't read that PDF - it may be scanned or corrupted."
        )


def _extract_docx(raw: bytes) -> str:
    try:
        document = docx.Document(io.BytesIO(raw))
        return "\n".join(p.text for p in document.paragraphs)
    except Exception:
        raise HTTPException(status_code=400, detail="Couldn't read that .docx file.")
