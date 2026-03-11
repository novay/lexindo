import json
import os

import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

RAW_DATA_PATH = (
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/01_raw_data"
)
CATEGORY_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/02_regulation_index/regulation_categories.json"

PERSIST_DIRECTORY = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/04_rag_corpus/chroma_db"

INDEX_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/02_regulation_index/regulation_index.json"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    reg_index = json.load(f)


reg_map = {r["regulation_id"]: r for r in reg_index}

# Load category map
with open(CATEGORY_PATH, "r", encoding="utf-8") as f:
    categories = json.load(f)

cat_map = {c["regulation_id"]: c["category"] for c in categories}

# Initialize embedding model (bge-m3)
# embedding_model = SentenceTransformer("BAAI/bge-m3")
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed_texts(texts):
    return embedding_model.encode(texts, normalize_embeddings=True).tolist()


# Setup Chroma
client = chromadb.Client(
    settings=chromadb.config.Settings(
        persist_directory=PERSIST_DIRECTORY, is_persistent=True
    )
)

collection = client.get_or_create_collection(
    name="lexindo_rag",
    embedding_function=None,  # we handle embedding manually
)

documents = []
metadatas = []
ids = []

chunk_counter = 0

for year_folder in sorted(os.listdir(RAW_DATA_PATH)):
    year_path = os.path.join(RAW_DATA_PATH, year_folder)

    if not os.path.isdir(year_path):
        continue

    for file_name in os.listdir(year_path):
        if not file_name.endswith(".json"):
            continue

        reg_id = file_name.replace(".json", "")
        category = cat_map.get(reg_id, "Unknown")

        file_path = os.path.join(year_path, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for chunk in data:
            pasal = chunk["metadata"].get("pasal")
            bab = chunk["metadata"].get("bab")

            if pasal is None:
                continue

            if bab == "Lampiran":
                continue

            if "-" in pasal:
                continue

            text = chunk["page_content"].strip()

            if len(text) < 50:
                continue

            chunk_id = f"{reg_id}_{pasal}_{chunk_counter}"

            documents.append(text)

            reg_info = reg_map[reg_id]
            metadatas.append(
                {
                    "regulation_id": reg_id,
                    "pasal": pasal,
                    "tahun": reg_info["tahun"],
                    "jenis": reg_info["jenis"],
                    "category": category,
                }
            )

            ids.append(chunk_id)

            chunk_counter += 1

# Embed in batches
batch_size = 64

for i in range(0, len(documents), batch_size):
    batch_docs = documents[i : i + batch_size]
    batch_meta = metadatas[i : i + batch_size]
    batch_ids = ids[i : i + batch_size]

    embeddings = embed_texts(batch_docs)
    collection.add(
        documents=batch_docs, embeddings=embeddings, metadatas=batch_meta, ids=batch_ids
    )

# client.persist()

print("RAG corpus built successfully!")
print(f"Total chunks indexed: {len(documents)}")
