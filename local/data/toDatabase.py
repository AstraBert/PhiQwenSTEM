from datasets import load_dataset
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from fastembed import SparseTextEmbedding
from typing import List

dataset = load_dataset("FreedomIntelligence/medical-o1-reasoning-SFT", "en")
questions = dataset["train"]["Question"]
chain_of_thoughts = dataset["train"]["Complex_CoT"]
response = dataset["train"]["Response"]

qdrant_client = QdrantClient("http://localhost:6333")


payloads = [{"question": questions[i], "context": chain_of_thoughts[i], "response": response[i]} for i in range(len(questions))]

dense_encoder = SentenceTransformer("tomaarsen/static-retrieval-mrl-en-v1")
sparse_encoder = SparseTextEmbedding(model_name="Qdrant/bm25")
reranlking_encoder = SentenceTransformer("nomic-ai/modernbert-embed-base")

def reranking(docs: List[str], query: str, dense_encoder: SentenceTransformer):
    query_vector = dense_encoder.encode(query)
    docs_vector = dense_encoder.encode(docs)
    similarities = dense_encoder.similarity(docs_vector, query_vector)
    sims = [float(sim[0]) for sim in similarities]
    text2sims = {docs[i]: sims[i] for i in range(len(sims))}
    sorted_items = sorted(text2sims.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[0][0]

def get_sparse_embedding(text: str, model: SparseTextEmbedding):
    embeddings = list(model.embed(text))
    vector = {f"sparse-text": models.SparseVector(indices=embeddings[0].indices, values=embeddings[0].values)}
    return vector

def upload_text_to_qdrant(client: QdrantClient, collection_name: str, context: str, question: str, response: str, point_id_dense: int, point_id_sparse: int):
    try:
        docs = {"context": context, "question": question, "response": response}
        client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=point_id_dense,
                    vector={f"dense-text": dense_encoder.encode(docs["question"]).tolist()},
                    payload=docs,
                )
            ],
        )
        client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=point_id_sparse,
                    vector=get_sparse_embedding(docs["question"], sparse_encoder),
                    payload=docs,
                )
            ],
        )
        return True
    except Exception as e:
        return False


qdrant_client.recreate_collection(
    collection_name="medical_cot_qa",
    vectors_config={"dense-text": models.VectorParams(
        size=1024,  # Vector size is defined by used model
        distance=models.Distance.COSINE,
    )},
    sparse_vectors_config={"sparse-text": models.SparseVectorParams(
        index=models.SparseIndexParams(
            on_disk=False
        )
    )}
)

c = 0
for payload in payloads:
    i = c+1
    j = c+2
    upload_text_to_qdrant(qdrant_client, "medical_cot_qa", payload["context"], payload["question"], payload["response"], i, j)
    c=j