import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
container_name = os.getenv("AZURE_CONTAINER_NAME")
blob_prefix = os.getenv("AZURE_BLOB_PREFIX", "data/")
download_dir = "data/"

def download_pdfs_from_azure():
    print("[Azure] Connecting to Azure Blob Storage...")
    service_client = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=account_key
    )
    container_client = service_client.get_container_client(container_name)

    os.makedirs(download_dir, exist_ok=True)

    print(f"[Azure] Downloading blobs with prefix '{blob_prefix}'...")
    for blob in container_client.list_blobs(name_starts_with=blob_prefix):
        if not blob.name.endswith(".pdf"):
            continue

        local_path = os.path.join(download_dir, os.path.basename(blob.name))
        with open(local_path, "wb") as file:
            data = container_client.download_blob(blob.name)
            file.write(data.readall())
            print(f"[Azure] Downloaded: {blob.name} → {local_path}")
