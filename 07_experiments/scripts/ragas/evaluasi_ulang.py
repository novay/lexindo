import os
import argparse
import json
import re
import numpy as np
import pandas as pd

from datasets import Dataset
from dotenv import load_dotenv
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from rank_bm25 import BM25Okapi
from ragas import evaluate
from ragas.metrics import context_recall, context_precision
from openai import OpenAI
from ragas.llms import llm_factory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


load_dotenv()

# ==========================================
# GLOBAL CONFIGURATIONS / MODELS
# ==========================================
EMBEDDING_MODEL = "intfloat/multilingual-e5-large-instruct"
EVALUATOR_MODEL = "lexindo-latest"
# ==========================================

@dataclass
class RetrievalConfig:
    name: str
    search_type: str
    k: int
    fetch_k: Optional[int] = None
    lambda_mult: Optional[float] = None


def parse_args():
    parser = argparse.ArgumentParser(
        description="RAGAS Context Recall and Context Precision Grid Evaluation"
    )

    parser.add_argument(
        "--eval-file",
        type=str,
        default="06_evaluation_set/eval_questions_reference_from_rag_final.jsonl",
        help="Evaluation file in JSONL or CSV format. Must contain question and ground_truth/reference.",
    )

    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Max rows to evaluate. Use 5 for quick test. Omit for full evaluation.",
    )

    parser.add_argument(
        "--device",
        type=str,
        default="mps",
        help="Device for embeddings: cpu, cuda, or mps.",
    )

    parser.add_argument(
        "--faiss-path",
        type=str,
        default="05_rag_corpus/faiss_index_lexindo",
        help="Path to FAISS index.",
    )

    parser.add_argument(
        "--embedding-model",
        type=str,
        default=EMBEDDING_MODEL,
        help="Embedding model name.",
    )

    parser.add_argument(
        "--only-config",
        type=str,
        default=None,
        help="Run only one config, for example: similarity_k5, similarity_k10, mmr_k10_fetch40_lambda0.5",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="07_experiments/ragas_context_recall_grid",
        help="Output directory.",
    )

    parser.add_argument(
        "--evaluator-model",
        type=str,
        default=EVALUATOR_MODEL,
        help="LLM model used by RAGAS evaluator.",
    )

    parser.add_argument(
        "--llm-max-tokens",
        type=int,
        default=4096,
        help="Max output tokens for RAGAS evaluator LLM.",
    )

    return parser.parse_args()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows = []

    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON at line {line_number} in {path}"
                ) from exc

    return rows


def normalize_row(row: Dict[str, Any], index: int) -> Dict[str, str]:
    question = (
        row.get("question")
        or row.get("user_input")
        or row.get("query")
        or row.get("input")
    )

    ground_truth = (
        row.get("ground_truth")
        or row.get("reference")
        or row.get("ground_truths")
        or row.get("expected_answer")
    )

    if isinstance(ground_truth, list):
        ground_truth = ground_truth[0] if ground_truth else ""

    if question is None or ground_truth is None:
        raise ValueError(
            f"Row {index} tidak memiliki field question/user_input "
            f"atau ground_truth/reference. Isi row: {row}"
        )

    return {
        "id": str(index),
        "question": str(question).strip(),
        "ground_truth": str(ground_truth).strip(),
    }


def load_evaluation_data(eval_file: str, max_rows: Optional[int]) -> List[Dict[str, str]]:
    path = Path(eval_file)

    if not path.exists():
        raise FileNotFoundError(f"Evaluation file not found: {path}")

    print(f"Using eval file: {path}")

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
        raw_rows = df.to_dict(orient="records")
    else:
        raw_rows = read_jsonl(path)

    rows = []

    for i, row in enumerate(raw_rows, start=1):
        normalized = normalize_row(row, i)

        if not normalized["question"] or not normalized["ground_truth"]:
            continue

        rows.append(normalized)

    if max_rows is not None:
        rows = rows[:max_rows]

    print(f"Loaded eval rows: {len(rows)}")

    print("\nSample questions:")
    for row in rows[:5]:
        print(f"- {row['question']}")

    return rows

def tokenize_for_bm25(text: str) -> List[str]:
    text = str(text).lower()
    return re.findall(r"[a-zA-Z0-9]+", text)


def build_bm25_index(db: FAISS):
    """
    Membuat BM25 index dari seluruh dokumen yang ada di FAISS docstore.
    """
    docs = list(db.docstore._dict.values())
    corpus_tokens = [tokenize_for_bm25(doc.page_content) for doc in docs]
    bm25 = BM25Okapi(corpus_tokens)
    return docs, bm25


def bm25_search(query: str, bm25_docs, bm25, k: int):
    query_tokens = tokenize_for_bm25(query)
    scores = bm25.get_scores(query_tokens)

    top_indices = np.argsort(scores)[::-1][:k]
    return [bm25_docs[i] for i in top_indices if scores[i] > 0]


def merge_documents_unique(docs, max_docs: int):
    """
    Menggabungkan dokumen hasil vector search dan BM25 tanpa duplikasi isi.
    """
    seen = set()
    merged = []

    for doc in docs:
        key = doc.page_content.strip()

        if key in seen:
            continue

        seen.add(key)
        merged.append(doc)

        if len(merged) >= max_docs:
            break

    return merged

def build_configs() -> List[RetrievalConfig]:
    return [
        RetrievalConfig(name="similarity_k5", search_type="similarity", k=5),
        RetrievalConfig(name="similarity_k8", search_type="similarity", k=8),
        RetrievalConfig(name="similarity_k10", search_type="similarity", k=10),
        RetrievalConfig(name="similarity_k12", search_type="similarity", k=12),
        RetrievalConfig(name="similarity_k15", search_type="similarity", k=15),

        RetrievalConfig(
            name="mmr_k8_fetch30_lambda0.5",
            search_type="mmr",
            k=8,
            fetch_k=30,
            lambda_mult=0.5,
        ),
        RetrievalConfig(
            name="mmr_k10_fetch40_lambda0.5",
            search_type="mmr",
            k=10,
            fetch_k=40,
            lambda_mult=0.5,
        ),
        RetrievalConfig(
            name="mmr_k10_fetch40_lambda0.3",
            search_type="mmr",
            k=10,
            fetch_k=40,
            lambda_mult=0.3,
        ),
        RetrievalConfig(
            name="mmr_k12_fetch50_lambda0.5",
            search_type="mmr",
            k=12,
            fetch_k=50,
            lambda_mult=0.5,
        ),
        RetrievalConfig(
            name="mmr_k12_fetch50_lambda0.3",
            search_type="mmr",
            k=12,
            fetch_k=50,
            lambda_mult=0.3,
        ),
        RetrievalConfig(
            name="hybrid_vec8_kw8_k10",
            search_type="hybrid",
            k=10,
            fetch_k=8,
            lambda_mult=8,
        ),
        RetrievalConfig(
            name="hybrid_vec8_kw10_k12",
            search_type="hybrid",
            k=12,
            fetch_k=8,
            lambda_mult=10,
        ),
        RetrievalConfig(
            name="hybrid_vec10_kw10_k12",
            search_type="hybrid",
            k=12,
            fetch_k=10,
            lambda_mult=10,
        ),
    ]


def retrieve_contexts(
    db: FAISS,
    question: str,
    config: RetrievalConfig,
    bm25_docs=None,
    bm25=None,
) -> List[str]:

    if config.search_type == "similarity":
        docs = db.similarity_search(question, k=config.k)

    elif config.search_type == "mmr":
        docs = db.max_marginal_relevance_search(
            question,
            k=config.k,
            fetch_k=config.fetch_k or max(config.k * 4, 20),
            lambda_mult=config.lambda_mult if config.lambda_mult is not None else 0.5,
        )

    elif config.search_type == "hybrid":
        vector_k = config.fetch_k or config.k
        keyword_k = int(config.lambda_mult or config.k)

        vector_docs = db.similarity_search(question, k=vector_k)
        keyword_docs = bm25_search(question, bm25_docs, bm25, k=keyword_k)

        docs = merge_documents_unique(
            vector_docs + keyword_docs,
            max_docs=config.k,
        )

    else:
        raise ValueError(f"Unknown search type: {config.search_type}")

    return [doc.page_content for doc in docs]


def make_ragas_dataset(rows: List[Dict[str, Any]]) -> Dataset:
    dataset_dict = {
        "question": [row["question"] for row in rows],
        "contexts": [row["contexts"] for row in rows],
        "ground_truth": [row["ground_truth"] for row in rows],
    }

    return Dataset.from_dict(dataset_dict)


def run_ragas(
    rows: List[Dict[str, Any]],
    evaluator_model: str = EVALUATOR_MODEL,
    llm_max_tokens: int = 4096,
) -> pd.DataFrame:
    dataset = make_ragas_dataset(rows)

    evaluator_llm = llm_factory(
        model=evaluator_model,
        client=OpenAI(),
        temperature=0,
        max_tokens=llm_max_tokens,
    )

    metrics = [
        context_recall,
        context_precision,
    ]

    result = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=evaluator_llm,
    )

    return result.to_pandas()

def summarize_result(config: RetrievalConfig, detail_df: pd.DataFrame) -> Dict[str, Any]:
    context_recall = pd.to_numeric(detail_df["context_recall"], errors="coerce")
    context_precision = pd.to_numeric(detail_df["context_precision"], errors="coerce")

    return {
        "config_name": config.name,
        "search_type": config.search_type,
        "k": config.k,
        "fetch_k": config.fetch_k,
        "lambda_mult": config.lambda_mult,
        "n": len(detail_df),
        "context_recall_mean": context_recall.mean(),
        "context_recall_median": context_recall.median(),
        "context_recall_std": context_recall.std(),
        "context_precision_mean": context_precision.mean(),
        "context_precision_median": context_precision.median(),
        "context_precision_std": context_precision.std(),
    }


def save_retrieval_jsonl(rows: List[Dict[str, Any]], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            item = {
                "id": row["id"],
                "question": row["question"],
                "ground_truth": row["ground_truth"],
                "contexts": row["contexts"],
            }
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def main():
    args = parse_args()

    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    rows = load_evaluation_data(
        eval_file=args.eval_file,
        max_rows=args.max_rows,
    )

    model_name = args.embedding_model
    print(f"\nLoading embeddings: {model_name}")

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": args.device},
        encode_kwargs={"normalize_embeddings": True},
    )

    faiss_path = args.faiss_path
    print(f"Loading FAISS index: {faiss_path}")

    db = FAISS.load_local(
        faiss_path,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    print("Building BM25 index from FAISS docstore...")
    bm25_docs, bm25 = build_bm25_index(db)
    print(f"BM25 documents: {len(bm25_docs)}")

    configs = build_configs()

    if args.only_config:
        configs = [cfg for cfg in configs if cfg.name == args.only_config]

        if not configs:
            valid = ", ".join(cfg.name for cfg in build_configs())
            raise ValueError(
                f"Config tidak ditemukan: {args.only_config}\n"
                f"Config valid: {valid}"
            )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_rows = []
    all_detail_rows = []

    for config in configs:
        print(f"\n=== Evaluating config: {config.name} ===")

        eval_rows = []

        for row in rows:
            contexts = retrieve_contexts(
                db,
                row["question"],
                config,
                bm25_docs=bm25_docs,
                bm25=bm25,
            )

            eval_rows.append(
                {
                    "id": row["id"],
                    "question": row["question"],
                    "ground_truth": row["ground_truth"],
                    "contexts": contexts,
                }
            )

        retrieval_path = output_dir / f"retrieval_{config.name}.jsonl"
        save_retrieval_jsonl(eval_rows, retrieval_path)
        print(f"Saved retrieval dataset: {retrieval_path}")

        detail_df = run_ragas(
            eval_rows,
            evaluator_model=args.evaluator_model,
            llm_max_tokens=args.llm_max_tokens,
        )

        detail_df.insert(0, "config_name", config.name)
        detail_df.insert(1, "search_type", config.search_type)
        detail_df.insert(2, "k", config.k)
        detail_df.insert(3, "fetch_k", config.fetch_k)
        detail_df.insert(4, "lambda_mult", config.lambda_mult)

        detail_path = output_dir / f"ragas_detail_{config.name}.csv"
        detail_df.to_csv(detail_path, index=False, encoding="utf-8-sig")
        print(f"Saved detail result: {detail_path}")

        summary = summarize_result(config, detail_df)
        summary_rows.append(summary)
        all_detail_rows.append(detail_df)

        print("\nSummary:")
        print(pd.DataFrame([summary]).to_string(index=False))

    summary_df = pd.DataFrame(summary_rows)
    summary_path = output_dir / "ragas_context_recall_grid_summary.csv"
    summary_df.to_csv(summary_path, index=False, encoding="utf-8-sig")

    all_detail_df = pd.concat(all_detail_rows, ignore_index=True)
    all_detail_path = output_dir / "ragas_context_recall_grid_detail.csv"
    all_detail_df.to_csv(all_detail_path, index=False, encoding="utf-8-sig")

    print("\n=== Final Summary Sorted by Context Recall ===")
    sort_cols = ["context_recall_mean", "context_precision_mean"]
    print(
        summary_df
        .sort_values(sort_cols, ascending=[False, False])
        .to_string(index=False)
    )

    print(f"\nSaved summary: {summary_path}")
    print(f"Saved all detail: {all_detail_path}")


if __name__ == "__main__":
    main()