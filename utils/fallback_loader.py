import pdfplumber
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.docstore.document import Document
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

class FallbackPDFLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        print(f"[PDF Parser] Attempting to extract using pdfplumber: {self.file_path}")
        try:
            with pdfplumber.open(self.file_path) as pdf:
                all_text = ""
                for i, page in enumerate(pdf.pages):
                    page_output = f"\n--- Page {i+1} ---\n"

                    # ✅ Step 1: Extract and format tables
                    tables = page.extract_tables()
                    if tables:
                        for t_index, table in enumerate(tables):
                            page_output += f"\n--- Table {t_index+1} ---\n"
                            for row in table:
                                row_text = "\t".join((cell or "").strip() for cell in row)
                                page_output += row_text + "\n"

                    # ✅ Step 2: Extract full page text (even if tables were found)
                    page_text = page.extract_text()
                    if page_text:
                        page_output += "\n" + page_text.strip() + "\n"

                    all_text += page_output

                if all_text.strip():
                    print("[PDF Parser] ✅ Extraction with pdfplumber succeeded")
                    return [Document(page_content=all_text)]

        except Exception as e:
            print(f"[PDF Parser] ❌ pdfplumber failed: {e}")

        # Fallback 1: LangChain Unstructured
        try:
            print("[PDF Parser] Trying UnstructuredPDFLoader fallback...")
            loader = UnstructuredPDFLoader(self.file_path)
            return loader.load()
        except Exception as e:
            print(f"[PDF Parser] ❌ Unstructured fallback failed: {e}")

        # Fallback 2: OCR
        try:
            print("[PDF Parser] Trying OCR fallback with PyMuPDF and pytesseract...")
            text = ""
            pdf_file = fitz.open(self.file_path)
            for i in range(len(pdf_file)):
                page = pdf_file[i]
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                text += pytesseract.image_to_string(img)

            if text.strip():
                print("[PDF Parser] ✅ OCR fallback succeeded")
                return [Document(page_content=text)]

        except Exception as e:
            print(f"[PDF Parser] ❌ OCR fallback failed: {e}")

        return [Document(page_content="")]
