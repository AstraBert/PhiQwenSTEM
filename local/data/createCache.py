from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
import os

load_dotenv()

qdrant_client = QdrantClient("http://localhost:6333")


qdrant_client.recreate_collection(
    collection_name="semantic_cache",
    vectors_config=models.VectorParams(
        size=768,  # Vector size is defined by used model
        distance=models.Distance.COSINE,
    ),
)