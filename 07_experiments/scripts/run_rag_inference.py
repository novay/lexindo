import json
import os

import chromadb
from sentence_transformers import SentenceTransformer

# =========================
# CONFIG
# =========================

MODE = "rag"  # options: "no_rag", "rag"
MODEL_NAME = "your-model-name"
PERSIST_DIRECTORY = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/04_rag_corpus/chroma_db"

EVAL_QUESTIONS_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/05_evaluation_set/evaluation_questions.json"
INDEX_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/02_regulation_index/regulation_index.json"

OUTPUT_PATH = f"/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/07_experiments/{MODE}_results.json"

# =========================
# LOAD DATA
# =========================

with open(EVAL_QUESTIONS_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    reg_index = json.load(f)

reg_map = {r["regulation_id"]: r for r in reg_index}

# =========================
# LOAD CHROMA (for RAG)
# =========================

if MODE == "rag":
    client = chromadb.Client(
        settings=chromadb.config.Settings(
            persist_directory=PERSIST_DIRECTORY, is_persistent=True
        )
    )
    collection = client.get_collection("lexindo_rag")

# =========================
# MODEL WRAPPER
# =========================


def generate_answer(prompt: str) -> str:
    """
    Replace this function with your actual LLM call.
    Example: OpenAI, Ollama, vLLM, etc.
    """
    # Placeholder
    return "MODEL_OUTPUT_PLACEHOLDER"


# =========================
# RUN INFERENCE
# =========================

results = []

for item in questions:
    question_id = item["question_id"]
    reg_id = item["regulation_id"]
    pasal_target = item["pasal_target"]
    question_text = item["question"]

    reg_info = reg_map[reg_id]

    retrieved_context = None

    if MODE == "rag":
        retrieval = collection.get(
            where={"$and": [{"regulation_id": reg_id}, {"pasal": pasal_target}]}
        )

        if retrieval["documents"]:
            retrieved_context = retrieval["documents"][0]
        else:
            retrieved_context = ""

        prompt = f"""
Gunakan konteks berikut untuk menjawab pertanyaan secara akurat dan sesuai isi regulasi.

KONTEKS:
{retrieved_context}

PERTANYAAN:
{question_text}
"""
    else:
        prompt = f"""
Jawab pertanyaan berikut secara lengkap dan jelas.

PERTANYAAN:
{question_text}
"""

    model_answer = generate_answer(prompt)

    results.append(
        {
            "question_id": question_id,
            "regulation_id": reg_id,
            "pasal_target": pasal_target,
            "question": question_text,
            "retrieved_context": retrieved_context,
            "model_answer": model_answer,
        }
    )

# =========================
# SAVE RESULTS
# =========================

os.makedirs(
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/07_experiments",
    exist_ok=True,
)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Inference completed in mode: {MODE}")
print(f"Results saved to: {OUTPUT_PATH}")

# OUTPUT
# Inference completed in mode: no_rag
# Results saved to: /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/07_experiments/no_rag_results.json
#
# Inference completed in mode: rag
# esults saved to: /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/07_experiments/rag_results.json
