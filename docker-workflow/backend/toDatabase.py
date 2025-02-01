from datasets import load_dataset
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from fastembed import SparseTextEmbedding
from typing import List
import time

def get_sparse_embedding(texts: List[str], model: SparseTextEmbedding):
    embeddings = list(model.embed(texts))
    vectors = [{f"sparse-text": models.SparseVector(indices=embeddings[i].indices, values=embeddings[i].values)} for i in range(len(embeddings))]
    return vectors

if __name__ == "__main__":
    dataset = load_dataset("FreedomIntelligence/medical-o1-reasoning-SFT", "en")
    questions = dataset["train"]["Question"]
    chain_of_thoughts = dataset["train"]["Complex_CoT"]
    response = dataset["train"]["Response"]
    dataset1 = load_dataset("FreedomIntelligence/medical-o1-verifiable-problem", split="train")
    ground_truths = dataset1["Ground-True Answer"]
    verifiable_questions = dataset1["Open-ended Verifiable Question"]

    print("Downloaded data!")

    dataset2dataset = []
    for i in range(len(questions)):
        base_dict = {}
        for j in range(len(verifiable_questions)):
            if questions[i] == verifiable_questions[j]:
                base_dict.update({"question": questions[i]})
                base_dict.update({"ground_truth": ground_truths[j]})
            else:
                continue
        if len(list(base_dict.keys())) > 0:
            base_dict.update({"context": chain_of_thoughts[i]})
            base_dict.update({"response": response[i]})
            dataset2dataset.append(base_dict)

    print("Mapped data!")

    texts = [d["question"] for d in dataset2dataset]
    qdrant_client = QdrantClient(host="host.docker.internal", port=6333)

    dense_encoder = SentenceTransformer("tomaarsen/static-retrieval-mrl-en-v1")
    dense_vectors = dense_encoder.encode(texts)
    dense_vectors_qd = [{f"dense-text": dense_vector.tolist()} for dense_vector in dense_vectors]
    print("Got dense vectors!")
    sparse_encoder = SparseTextEmbedding(model_name="Qdrant/bm25")
    sparse_vectors = get_sparse_embedding(texts, sparse_encoder)
    print("Got sparse vectors!")

    c = 0
    su = time.time()
    qdrant_client.upload_collection("med_cot_qa", sparse_vectors, dataset2dataset, batch_size=1400, parallel=10)
    print("Uploaded sparse vectors!")
    qdrant_client.upload_collection("med_cot_qa", dense_vectors_qd, dataset2dataset, batch_size=1400, parallel=10)
    print("Uploaded dense vectors!")
    eu = time.time()
    print("Done in", eu-su, "seconds")
    qdrant_client.update_collection(
        collection_name="med_cot_qa",
        optimizer_config=models.OptimizersConfigDiff(
            indexing_threshold=20000
        )
    )