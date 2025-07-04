from utils.azure_downloader import download_pdfs_from_azure
from agents.loader_agent import run_loader_agent_for_folder
from agents.qa_agent import run_qa_pipeline

# Step 1: Download PDFs from Azure
download_pdfs_from_azure()

# Step 2: Upload them to Qdrant
run_loader_agent_for_folder("data/")

# Step 3: Run Q&A if needed
run_qa_pipeline("data/questions.txt")
