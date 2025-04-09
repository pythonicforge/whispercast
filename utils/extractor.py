import os
import re
import requests
import mimetypes
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from docx import Document
import fitz
from utils import logger


def is_url(string: str) -> bool:
    return string.startswith("http://") or string.startswith("https://")


def extract_text_from_url(url: str) -> str:
    logger.info(f"Detected URL. Fetching content from: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = "\n".join(p.get_text() for p in paragraphs)
        return content.strip()
    except Exception as e:
        logger.error(f"Failed to fetch content from URL: {e}")
        return ""


def extract_text_from_pdf(file_path: str) -> str:
    logger.info(f"Reading PDF file: {file_path}")
    try:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
        return ""


def extract_text_from_docx(file_path: str) -> str:
    logger.info(f"Reading DOCX file: {file_path}")
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
    except Exception as e:
        logger.error(f"Failed to extract text from DOCX: {e}")
        return ""


def extract_text_from_txt(file_path: str) -> str:
    logger.info(f"📄 Reading TXT file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        logger.error(f"Failed to extract text from TXT file: {e}")
        return ""


def extract_content(source: str) -> str:
    """
    Auto-detect and extract clean text from a URL, file, or plain text.
    """
    source = source.strip()

    if is_url(source):
        return extract_text_from_url(source)

    if os.path.isfile(source):
        ext = os.path.splitext(source)[-1].lower()
        if ext == ".pdf":
            return extract_text_from_pdf(source)
        elif ext == ".docx":
            return extract_text_from_docx(source)
        elif ext == ".txt":
            return extract_text_from_txt(source)
        else:
            logger.warning("Unsupported file type. Only .txt, .pdf, .docx are supported.")
            return ""

    logger.info("Treating input as raw text.")
    return source
