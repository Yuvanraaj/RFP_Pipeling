import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\i-yuvanraaj\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_with_pdfplumber(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[pdfplumber] Error: {e}")
    return text.strip()

def extract_with_fitz(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                page_text = page.get_text("text")
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[fitz fallback] Error: {e}")
    return text.strip()

def extract_with_ocr(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=300)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                page_text = pytesseract.image_to_string(img)
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[OCR fallback] Error: {e}")
    return text.strip()

def extract_text_from_pdf(pdf_path):
    print(f"[PDF Parser] Attempting to extract using pdfplumber: {pdf_path}")
    text = extract_with_pdfplumber(pdf_path)
    if len(text.strip()) < 100:
        print("[PDF Parser] ⛔ Low content from pdfplumber. Trying fitz fallback...")
        text = extract_with_fitz(pdf_path)
    if len(text.strip()) < 100:
        print("[PDF Parser] ⛔ Low content from fitz. Trying OCR fallback...")
        text = extract_with_ocr(pdf_path)
    if len(text.strip()) == 0:
        print("[PDF Parser] ❌ All extractors failed.")
    else:
        print("[PDF Parser] ✅ Extraction complete.")
    return text

__all__ = ["extract_text_from_pdf"]
