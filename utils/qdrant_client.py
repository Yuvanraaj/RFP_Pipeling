from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import uuid
import os

# ⚙️ Replace these with your actual values from Qdrant Cloud
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.JZHaC8ey7NaWyKJmWDkOdyvIhobFMhsNhQaQzU1MH7U"
QDRANT_HOST = "https://b08b781e-60b0-4f1e-a385-06a4e7c894bd.eu-west-1-0.aws.cloud.qdrant.io"
 # example: https://blue-shrimp-12345.cloud.qdrant.io
COLLECTION_NAME = "rfp_docs"

# Embedder model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize client
client = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY
)

def init_qdrant():
    collections = client.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        print(f"[Qdrant] Creating collection '{COLLECTION_NAME}'...")
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
    else:
        print(f"[Qdrant] Collection '{COLLECTION_NAME}' already exists.")

def upload_chunks_to_qdrant(chunks, batch_size=50):
    init_qdrant()

    print(f"[Qdrant] Embedding and uploading {len(chunks)} chunks...")

    embeddings = embedder.encode(chunks).tolist()
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=vec, payload={"text": chunk})
        for vec, chunk in zip(embeddings, chunks)
    ]

    # ✅ Upload in batches
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        try:
            client.upsert(collection_name=COLLECTION_NAME, points=batch)
            print(f"[Qdrant] ✅ Uploaded batch {i // batch_size + 1} ({len(batch)} points)")
        except Exception as e:
            print(f"[Qdrant] ❌ Failed to upload batch {i // batch_size + 1}: {e}")

    print("[Qdrant] ✅ Upload complete.")

    
if __name__ == "__main__":
    chunks = [
        "This is a test chunk.",
        "Here is another example chunk of text."
    ]
    upload_chunks_to_qdrant(chunks)