import json
import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,  # kalau perlu re-chunk
)
from tqdm import tqdm  # progress bar

# Path root raw data
RAW_DATA_DIR = (
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/01_raw_data"
)


def load_all_raw_documents(root_dir):
    documents = []
    json_files = []

    # Cari semua .json di subfolder tahun
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(subdir, file))

    print(f"Found {len(json_files)} JSON files.")

    for file_path in tqdm(json_files, desc="Loading JSON files"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                print(f"Skipping non-list JSON: {file_path}")
                continue

            for chunk in data:
                if "page_content" in chunk and chunk["page_content"].strip():
                    doc = Document(
                        page_content=chunk["page_content"].strip(),
                        metadata=chunk.get("metadata", {}),
                    )
                    # Tambah source path kalau metadata tidak punya
                    if "source_path" not in doc.metadata:
                        doc.metadata["source_path"] = file_path
                    documents.append(doc)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    print(f"Loaded {len(documents)} document chunks.")
    return documents


# Load semua chunks
raw_docs = load_all_raw_documents(RAW_DATA_DIR)

# Opsional: Re-chunk kalau chunk terlalu panjang/pendek (skip kalau sudah optimal)
# splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
# split_docs = splitter.split_documents(raw_docs)

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large-instruct",
    model_kwargs={"device": "mps"},  # gunakan 'mps' untuk Apple Silicon acceleration
)

# Buat vector store
print("Building FAISS index...")
vectorstore = FAISS.from_documents(
    raw_docs, embeddings
)  # atau split_docs kalau re-chunk

# Simpan index untuk reuse (penting!)
vectorstore.save_local(
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/04_rag_corpus/faiss_index_lexindo"
)

print("Retriever siap! Index disimpan di folder 'faiss_index_lexindo'")


# OUTPUT
# Found 398 JSON files.
# Loading JSON files: 100%|███████████████████████████████████████████████████████████████████████████████████████████| 398/398 [00:00<00:00, 1952.97it/s]
# Loaded 6471 document chunks.
# /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/04_rag_corpus/build_rag_retriever.py:63: LangChainDeprecationWarning: The class `HuggingFaceEmbeddings` was deprecated in LangChain 0.2.2 and will be removed in 1.0. An updated version of the class exists in the `langchain-huggingface package and should be used instead. To use it run `pip install -U `langchain-huggingface` and import as `from `langchain_huggingface import HuggingFaceEmbeddings``. embeddings = HuggingFaceEmbeddings(
# modules.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████| 349/349 [00:00<00:00, 4.48MB/s]
# config_sentence_transformers.json: 100%|████████████████████████████████████████████████████████████████████████████████| 128/128 [00:00<00:00, 219kB/s]
# README.md: 140kB [00:00, 10.6MB/s]
# sentence_xlm-roberta_config.json: 100%|███████████████████████████████████████████████████████████████████████████████| 53.0/53.0 [00:00<00:00, 402kB/s]
# config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 690/690 [00:00<00:00, 11.1MB/s]
# model.safetensors: 100%|███████████████████████████████████████████████████████████████████████████████████████████| 1.12G/1.12G [05:38<00:00, 3.31MB/s]
# tokenizer_config.json: 1.18kB [00:00, 23.6kB/s]
# sentencepiece.bpe.model: 100%|█████████████████████████████████████████████████████████████████████████████████████| 5.07M/5.07M [00:03<00:00, 1.69MB/s]
# tokenizer.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████████| 17.1M/17.1M [00:05<00:00, 3.05MB/s]
# special_tokens_map.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 964/964 [00:00<00:00, 16.3MB/s]
# config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 271/271 [00:00<00:00, 2.24MB/s]
# Building FAISS index...
# Retriever siap! Index disimpan di folder 'faiss_index_lexindo'
