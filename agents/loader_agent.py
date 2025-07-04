from utils.fallback_loader import FallbackPDFLoader
from utils.qdrant_client import upload_chunks_to_qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
from utils.save_text import append_parsed_text

def run_loader_agent_for_folder(folder_path="data/"):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    total_chunks = 0

    for pdf_file in pdf_files:
        full_path = os.path.join(folder_path, pdf_file)
        print(f"\n[LoaderAgent] Processing: {pdf_file}")

        # 📄 Load and fallback-parse the PDF
        loader = FallbackPDFLoader(full_path)
        docs = loader.load()

        # 💾 Save to a single text file
        append_parsed_text(docs, pdf_file)

        # 🔍 Preview parsed content
        preview = docs[0].page_content if docs else ""
        print("\n[Parsed Text Preview]\n", preview[:2000], "\n...")

        # 🧩 Smart chunking
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        split_docs = splitter.split_documents(docs)
        chunk_texts = [doc.page_content for doc in split_docs]

        # ☁️ Upload to Qdrant
        upload_chunks_to_qdrant(chunk_texts)
        print(f"[LoaderAgent] Uploaded {len(chunk_texts)} chunks.")
        total_chunks += len(chunk_texts)

    print(f"\n✅ All PDFs uploaded. Total chunks: {total_chunks}")
