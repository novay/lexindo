import chromadb
from sentence_transformers import SentenceTransformer

PERSIST_DIRECTORY = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/04_rag_corpus/chroma_db"

# Load embedding model (harus sama dengan saat build)
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed_query(text):
    return embedding_model.encode([text], normalize_embeddings=True).tolist()


# Connect to Chroma
client = chromadb.Client(
    settings=chromadb.config.Settings(
        persist_directory=PERSIST_DIRECTORY, is_persistent=True
    )
)

collection = client.get_collection("lexindo_rag")

query = "Peraturan Bupati Nomor 4 Tahun 2022 tentang BADAN PENGELOLA MASJID AGUNG SULTAN AJI MUHAMMAD SULAIMAN TENGGARONG KABUPATEN KUTAI KARTANEGARA. Apa ketentuan yang diatur dalam Pasal 2?"

query_embedding = embed_query(query)

results = collection.query(
    query_embeddings=query_embedding,
    n_results=5,
    where={"regulation_id": "2022pb6402004"},
)

print("Top 5 Results:\n")

for i in range(len(results["documents"][0])):
    print("-----")
    print("Regulation:", results["metadatas"][0][i]["regulation_id"])
    print("Pasal:", results["metadatas"][0][i]["pasal"])
    print("Kategori:", results["metadatas"][0][i]["category"])
    print("Snippet:", results["documents"][0][i][:300])
