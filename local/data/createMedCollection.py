from qdrant_client import QdrantClient, models

qdrant_client = QdrantClient("http://localhost:6333")

qdrant_client.create_collection(
    collection_name="med_cot_qa",
    vectors_config={"dense-text": models.VectorParams(
        size=1024,  # Vector size is defined by used model
        distance=models.Distance.COSINE,
    )},
    sparse_vectors_config={"sparse-text": models.SparseVectorParams(
        index=models.SparseIndexParams(
            on_disk=False
        )
    )},
    optimizers_config=models.OptimizersConfigDiff(
        default_segment_number=5,
        indexing_threshold=0,
    ),
    quantization_config=models.BinaryQuantization(
        binary=models.BinaryQuantizationConfig(always_ram=True),
    ),
)
print("Created collection!")