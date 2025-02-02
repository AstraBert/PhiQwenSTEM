# IMPORTS
from qdrant_client import QdrantClient, models
from fastembed import SparseTextEmbedding
from sentence_transformers import SentenceTransformer
import uuid
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

qdrant_client = QdrantClient(url=os.getenv("qdrant_url"), api_key=os.getenv("qdrant_api_key"))
reranlking_encoder = SentenceTransformer("nomic-ai/modernbert-embed-base")
dense_encoder = SentenceTransformer("tomaarsen/static-retrieval-mrl-en-v1", truncate_dim=384)
sparse_encoder = SparseTextEmbedding(model_name="Qdrant/bm25")

## FUNCTIONS
def get_query_sparse_embedding(text: str, model: SparseTextEmbedding):
    embeddings = list(model.embed(text))
    query_vector = models.NamedSparseVector(
        name="sparse-text",
        vector=models.SparseVector(
            indices=embeddings[0].indices,
            values=embeddings[0].values,
        ),
    )
    return query_vector

## CLASSES
class Reranker:
    def __init__(self, reranking_encoder: SentenceTransformer):
        self.reranking_encoder = reranking_encoder
    def reranking(self, docs: List[str], query: str):
        query_vector = self.reranking_encoder.encode(query)
        docs_vector = self.reranking_encoder.encode(docs)
        similarities = self.reranking_encoder.similarity(docs_vector, query_vector)
        sims = [float(sim[0]) for sim in similarities]
        text2sims = {docs[i]: sims[i] for i in range(len(sims))}
        sorted_items = sorted(text2sims.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[0][0]

class SemanticCache:
    def __init__(self, client: QdrantClient, text_encoder: SentenceTransformer, collection_name: str, threshold: float = 0.75):
        self.client = client
        self.text_encoder = text_encoder
        self.collection_name = collection_name
        self.threshold = threshold
    def upload_to_cache(self, question: str, answer: str):
        docs = {"question": question, "answer": answer}
        point_id = str(uuid.uuid4())
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=self.text_encoder.encode(docs["question"]).tolist(),
                    payload=docs,
                )
            ],
        )
    def search_cache(self, question: str, limit: int = 5):
        vector = self.text_encoder.encode(question).tolist()
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=None,
            limit=limit,
        )
        payloads = [hit.payload["answer"] for hit in search_result if hit.score > self.threshold]
        if len(payloads) > 0:
            return payloads[0]
        else:
            return ""


class NeuralSearcher:
    def __init__(self, text_collection_name: str, client: QdrantClient, dense_encoder: SentenceTransformer , sparse_encoder: SparseTextEmbedding):
        self.text_collection_name = text_collection_name
        self.dense_encoder = dense_encoder
        self.qdrant_client = client
        self.sparse_encoder = sparse_encoder
    def search_text(self, text: str, limit: int = 5):
        vector = self.dense_encoder.encode(text).tolist()
        search_result_dense = self.qdrant_client.search(
            collection_name=self.text_collection_name,
            query_vector=models.NamedVector(name="dense-text", vector=vector),
            query_filter=None,
            limit=limit,
        )
        search_result_sparse = self.qdrant_client.search(
            collection_name=self.text_collection_name,
            query_vector=get_query_sparse_embedding(text, self.sparse_encoder),
            query_filter=None,
            limit=limit,
        )
        responses = [hit.payload["context"] for hit in search_result_dense]
        responses += [hit.payload["context"] for hit in search_result_sparse]
        return responses
    
    
    