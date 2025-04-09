import os
import requests
from bs4 import BeautifulSoup
from docx import Document
import fitz
from utils import logger

def is_url(string: str) -> bool:
    """
    Check if the given string is a URL.
    """
    return string.startswith("http://") or string.startswith("https://")

def extract_text_from_url(url: str) -> str:
    """
    Extract text content from a URL.
    """
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
    """
    Extract text content from a PDF file.
    """
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
    """
    Extract text content from a DOCX file.
    """
    logger.info(f"Reading DOCX file: {file_path}")
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
    except Exception as e:
        logger.error(f"Failed to extract text from DOCX: {e}")
        return ""

def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text content from a TXT file.
    """
    logger.info(f"📄 Reading TXT file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        logger.error(f"Failed to extract text from TXT file: {e}")
        return ""

def trim_text(text: str, max_words: int = 6000) -> str:
    """
    Trim the text to a maximum number of words.
    """
    words = text.split()
    return ' '.join(words[:max_words])

def extract_content(source: str, max_words: int = 6000) -> str:
    """
    Auto-detect and extract clean text from a URL, file, or plain text.
    Trim the extracted content to the specified maximum number of words.
    """
    source = source.strip()

    if is_url(source):
        content = extract_text_from_url(source)
    elif os.path.isfile(source):
        ext = os.path.splitext(source)[-1].lower()
        if ext == ".pdf":
            content = extract_text_from_pdf(source)
        elif ext == ".docx":
            content = extract_text_from_docx(source)
        elif ext == ".txt":
            content = extract_text_from_txt(source)
        else:
            logger.warning("Unsupported file type. Only .txt, .pdf, .docx are supported.")
            return ""
    else:
        logger.info("Treating input as raw text.")
        content = source

    # Trim the content to the maximum number of words
    return trim_text(content, max_words)
