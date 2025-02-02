from datasets import load_dataset
from qdrant_client import QdrantClient, models
from qdrant_client.conversions import common_types as types
from sentence_transformers import SentenceTransformer
from fastembed import SparseTextEmbedding
from typing import List
import pandas as pd
import time

def get_sparse_embedding(texts: List[str], model: SparseTextEmbedding):
    embeddings = list(model.embed(texts))
    vectors = [{f"sparse-text": models.SparseVector(indices=embeddings[i].indices, values=embeddings[i].values)} for i in range(len(embeddings))]
    return vectors

if __name__ == "__main__":
    dataset = load_dataset("EricLu/SCP-116K", split="train")
    df = pd.DataFrame(dataset)
    df = df.drop(columns=["o1_solution", "is_o1_solution_same_with_matched_solution"])
    df = df[df["is_qwq_solution_same_with_matched_solution"] == True]
    subjects = ['Chemistry', 'Physics', 'Physical Chemistry', 'Quantum Mechanics', 'Biochemistry', 'Differential Equations', 'Linear Algebra', 'Electromagnetism', 'Mathematics', 'Organic Chemistry', 'Engineering', 'Chemistry (General, Organic, and Biochemistry for Health Sciences)', 'Classical Mechanics']
    df = df[df["domain"].isin(subjects)]
    questions = df["problem"].to_list()
    chain_of_thoughts = df["qwq_solution"].to_list()
    domains = df["domain"].to_list()

    print("Downloaded data!")

    dataset2dataset = [{"question": questions[i], "context": chain_of_thoughts[i], "domain": domains[i]} for i in range(len(questions))]
    print(len(dataset2dataset))
    print("Mapped data!")

    texts = [d["question"] for d in dataset2dataset]
    qdrant_client = QdrantClient("http://localhost:6333")

    dense_encoder = SentenceTransformer("tomaarsen/static-retrieval-mrl-en-v1", truncate_dim=384)
    dense_vectors = dense_encoder.encode(texts)
    dense_vectors_qd = [{f"dense-text": dense_vector.tolist()} for dense_vector in dense_vectors]
    print("Got dense vectors!")
    sparse_encoder = SparseTextEmbedding(model_name="Qdrant/bm25")
    sparse_vectors = get_sparse_embedding(texts, sparse_encoder)
    print("Got sparse vectors!")

    su = time.time()
    qdrant_client.upload_collection("stem_cot_qa", sparse_vectors, dataset2dataset, ids = range(len(sparse_vectors)), batch_size=1500, parallel=10)
    print("Uploaded sparse vectors!")
    qdrant_client.upload_collection("stem_cot_qa", dense_vectors_qd, dataset2dataset, ids=range(len(sparse_vectors), len(sparse_vectors)+len(dense_vectors_qd)), batch_size=1500, parallel=10)
    print("Uploaded dense vectors!")
    eu = time.time()
    print("Done in", eu-su, "seconds")
    qdrant_client.update_collection(
        collection_name="stem_cot_qa",
        optimizer_config=models.OptimizersConfigDiff(
            indexing_threshold=20000
        )
    )
    