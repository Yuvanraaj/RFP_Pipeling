
# 📄 RFP Document Intelligence Pipeline

This project is an end-to-end intelligent document processing pipeline designed to parse multiple **RFP (Request for Proposal)** PDFs, store them as vector embeddings in **Qdrant**, and answer natural language questions using **LLMs** via **Together.ai**. It supports fallbacks for parsing and integrates with **Azure Blob Storage** for cloud-based PDF ingestion.

---

## 📚 Table of Contents

- [🚀 Features](#-features)
- [📁 Folder Structure](#-folder-structure)
- [⚙️ Setup Instructions](#️-setup-instructions)
- [🧪 Run the Pipeline](#-run-the-pipeline)
- [✍️ Sample Questions](#-sample-questions)
- [📦 Dependencies](#-dependencies)
- [🔁 Extending the Project](#-extending-the-project)
- [🧠 Credits](#-credits)
- [📜 License](#-license)

---

## 🚀 Features

✅ Batch processing of multiple RFP PDFs  
✅ Smart PDF parsing with layered fallbacks:
- `pdfplumber` → `unstructured` → `OCR (Tesseract)`  
✅ Text chunking & semantic embedding with `sentence-transformers`  
✅ Vector storage in **Qdrant Cloud**  
✅ Natural language Q&A using **Together.ai LLMs**  
✅ Output saved to a **Word document**  
✅ Cloud ingestion via **Azure Blob Storage**  
✅ All parsed data is also stored in a `parsed_output.txt` file

---

## 📁 Folder Structure

```
.
├── agents/
│   ├── loader_agent.py          # Handles PDF ingestion and parsing
│   └── qa_agent.py              # Runs QA pipeline and generates answers
│
├── data/
│   ├── input1.pdf               # Drop your RFP PDFs here
│   └── questions.txt            # Add your custom questions
│
├── utils/
│   ├── fallback_loader.py       # PDF parsing with fallback mechanisms
│   ├── qdrant_client.py         # Uploads embeddings to Qdrant
│   ├── azure_downloader.py      # Downloads files from Azure Blob
│   └── save_text.py             # Saves parsed content to text file
│
├── .env                         # API keys and secrets
├── main.py                      # Main orchestration script
└── requirements.txt             # Required packages
```

---

## ⚙️ Setup Instructions

### 1. 🧠 Clone the Repository

```bash
git clone https://github.com/your-username/rfp-pipeline.git
cd rfp-pipeline
```

### 2. 🐍 Create a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. 🛠️ Configure `.env` File

Create a `.env` file in the root directory with the following content:

```env
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_HOST=https://your-qdrant-url
TOGETHER_API_KEY=your-together-api-key

AZURE_STORAGE_ACCOUNT_NAME=your-account
AZURE_STORAGE_ACCOUNT_KEY=your-key
AZURE_CONTAINER_NAME=your-container
```

### 5. ✅ Install Tesseract (Required for OCR Fallback)

- [Tesseract Installation Guide](https://github.com/tesseract-ocr/tesseract/wiki)
- Ensure `tesseract` is added to your system PATH

---

## 🧪 Run the Pipeline

```bash
python main.py
```

This will:
- Download PDFs from Azure Blob (if configured)
- Parse all PDFs using layered fallbacks
- Upload embeddings to Qdrant
- Run LLM-powered Q&A using questions from `questions.txt`
- Save final answers to a `output.docx` Word file

---

## ✍️ Sample Questions

Add your custom questions in `data/questions.txt`. For example:

```
What are the chronic conditions listed?
What is the total number of clinic visits?
Who authored the RFP?
What are the evaluation criteria?
```

---

## 📦 Dependencies

- `pdfplumber`, `fitz`, `pytesseract`, `unstructured`
- `sentence-transformers`, `torch`, `qdrant-client`
- `langchain`, `python-docx`, `together`, `python-dotenv`
- `azure-storage-blob`

Install them via:

```bash
pip install -r requirements.txt
```

---

## 🔁 Extending the Project

- 💬 Replace **Together.ai** with **OpenAI**, **Anthropic (Claude)**, or **Mistral**
- ☁️ Swap **Azure Blob Storage** with **AWS S3** or **GCP**
- 🖼️ Add visual extraction like tables/images using **PaddleOCR** or **LayoutLM**
- 📄 Include RAG citations or answer traceability using LangChain's tools

---

## 🧠 Credits

Built with 💡 by Yuvanraaj & Varuna  
Inspired by real-world document automation and RFP processing use-cases.

---

## 📜 License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and distribute with attribution.
