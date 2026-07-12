import argparse
import json
import math
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from datasets import Dataset
from dotenv import load_dotenv
from scipy import stats

from ragas import evaluate
from ragas.metrics import answer_correctness
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI

try:
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from langchain_openai import OpenAIEmbeddings
    HAS_EMBEDDING_WRAPPER = True
except Exception:
    HAS_EMBEDDING_WRAPPER = False


load_dotenv()

# ==========================================
# GLOBAL CONFIGURATIONS / MODELS
# ==========================================
EMBEDDING_MODEL = "intfloat/multilingual-e5-large-instruct"
EVALUATOR_MODEL = "lexindo-latest"
# ==========================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Evaluate no-RAG answer_correctness and run paired statistical test against RAG."
    )

    parser.add_argument(
        "--input-no-rag",
        type=str,
        default="07_experiments/eval_ft_no_rag_100.jsonl",
        help="File jawaban LexIndoLLM tanpa RAG. Format JSONL/CSV, berisi question, answer/response, dan ground_truth/reference jika ada.",
    )

    parser.add_argument(
        "--rag-csv",
        type=str,
        default="06_evaluation_set/hasil_eval_rag_v2_final.csv",
        help="File hasil evaluasi RAG yang sudah memiliki kolom answer_correctness.",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="07_experiments/statistical_test_answer_correctness",
        help="Folder output hasil evaluasi dan uji statistik.",
    )

    parser.add_argument(
        "--evaluator-model",
        type=str,
        default=EVALUATOR_MODEL,
        help="Model LLM evaluator untuk RAGAS.",
    )

    parser.add_argument(
        "--llm-max-tokens",
        type=int,
        default=4096,
        help="Max output tokens untuk evaluator LLM.",
    )

    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Batasi jumlah data untuk uji coba. Kosongkan untuk full 100 data.",
    )

    parser.add_argument(
        "--skip-ragas",
        action="store_true",
        help="Lewati evaluasi RAGAS dan langsung lakukan uji statistik dari file no_rag_answer_correctness.csv yang sudah ada.",
    )

    parser.add_argument(
        "--align-by",
        type=str,
        default="order",
        choices=["order", "question"],
        help="Cara memasangkan skor tanpa RAG dan dengan RAG. Gunakan 'order' jika urutan pertanyaan sama.",
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
                raise ValueError(f"JSON tidak valid pada baris {line_number}: {path}") from exc

    return rows


def read_input_file(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    if path.suffix.lower() == ".csv":
        return pd.read_csv(path).to_dict(orient="records")

    return read_jsonl(path)


def normalize_text(text: Any) -> str:
    text = "" if text is None else str(text)
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def get_first_existing(row: Dict[str, Any], keys: List[str]) -> Optional[Any]:
    for key in keys:
        if key in row and row[key] is not None and not pd.isna(row[key]):
            return row[key]
    return None


def build_reference_lookup_from_rag(rag_csv: Path) -> Dict[str, str]:
    df = pd.read_csv(rag_csv)

    question_col = "question" if "question" in df.columns else "user_input"
    if question_col not in df.columns:
        raise ValueError("File RAG tidak memiliki kolom question atau user_input.")

    reference_col = "reference" if "reference" in df.columns else "ground_truth"
    if reference_col not in df.columns:
        raise ValueError("File RAG tidak memiliki kolom reference atau ground_truth.")

    lookup = {}

    for _, row in df.iterrows():
        q = normalize_text(row[question_col])
        ref = row[reference_col]

        if q and not pd.isna(ref):
            lookup[q] = str(ref).strip()

    return lookup


def normalize_no_rag_rows(
    raw_rows: List[Dict[str, Any]],
    reference_lookup: Dict[str, str],
    max_rows: Optional[int],
) -> pd.DataFrame:
    records = []

    for i, row in enumerate(raw_rows, start=1):
        question = get_first_existing(
            row,
            ["question", "user_input", "query", "input", "instruction"],
        )

        answer = get_first_existing(
            row,
            ["answer", "response", "output", "prediction", "model_answer"],
        )

        ground_truth = get_first_existing(
            row,
            ["ground_truth", "reference", "expected_answer", "ground_truths"],
        )

        if isinstance(ground_truth, list):
            ground_truth = ground_truth[0] if ground_truth else None

        if ground_truth is None and question is not None:
            ground_truth = reference_lookup.get(normalize_text(question))

        if question is None or answer is None or ground_truth is None:
            raise ValueError(
                f"Data baris {i} tidak lengkap. Butuh question, answer/response, dan ground_truth/reference.\n"
                f"Isi baris: {row}"
            )

        records.append(
            {
                "row_id": i,
                "question": str(question).strip(),
                "answer_no_rag": str(answer).strip(),
                "ground_truth": str(ground_truth).strip(),
                "question_key": normalize_text(question),
            }
        )

    df = pd.DataFrame(records)

    if max_rows is not None:
        df = df.head(max_rows).copy()

    return df


def evaluate_no_rag_answer_correctness(
    no_rag_df: pd.DataFrame,
    evaluator_model: str,
    llm_max_tokens: int,
) -> pd.DataFrame:
    dataset = Dataset.from_dict(
        {
            "question": no_rag_df["question"].tolist(),
            "answer": no_rag_df["answer_no_rag"].tolist(),
            "ground_truth": no_rag_df["ground_truth"].tolist(),
        }
    )

    evaluator_llm = LangchainLLMWrapper(
        ChatOpenAI(
            model=evaluator_model,
            temperature=0,
            max_tokens=llm_max_tokens,
        )
    )

    evaluate_kwargs = {
        "dataset": dataset,
        "metrics": [answer_correctness],
        "llm": evaluator_llm,
    }

    if HAS_EMBEDDING_WRAPPER:
        try:
            evaluator_embeddings = LangchainEmbeddingsWrapper(
                OpenAIEmbeddings(model=EMBEDDING_MODEL)
            )
            evaluate_kwargs["embeddings"] = evaluator_embeddings
        except Exception:
            pass

    result = evaluate(**evaluate_kwargs)
    result_df = result.to_pandas()

    if "answer_correctness" not in result_df.columns:
        raise ValueError(
            f"Kolom answer_correctness tidak ditemukan dari hasil RAGAS. "
            f"Kolom tersedia: {list(result_df.columns)}"
        )

    out_df = no_rag_df.copy()
    out_df["answer_correctness_no_rag"] = pd.to_numeric(
        result_df["answer_correctness"], errors="coerce"
    )

    return out_df


def load_rag_scores(rag_csv: Path, max_rows: Optional[int]) -> pd.DataFrame:
    df = pd.read_csv(rag_csv)

    if "answer_correctness" not in df.columns:
        raise ValueError(
            f"Kolom answer_correctness tidak ditemukan pada {rag_csv}. "
            f"Kolom tersedia: {list(df.columns)}"
        )

    question_col = "question" if "question" in df.columns else "user_input"
    if question_col not in df.columns:
        raise ValueError("File RAG tidak memiliki kolom question atau user_input.")

    out = pd.DataFrame(
        {
            "row_id": np.arange(1, len(df) + 1),
            "question_rag": df[question_col].astype(str),
            "question_key": df[question_col].apply(normalize_text),
            "answer_correctness_rag": pd.to_numeric(
                df["answer_correctness"], errors="coerce"
            ),
        }
    )

    if max_rows is not None:
        out = out.head(max_rows).copy()

    return out


def pair_scores(
    no_rag_scores: pd.DataFrame,
    rag_scores: pd.DataFrame,
    align_by: str,
) -> pd.DataFrame:
    if align_by == "question":
        paired = no_rag_scores.merge(
            rag_scores[["question_key", "answer_correctness_rag", "question_rag"]],
            on="question_key",
            how="inner",
        )
    else:
        paired = no_rag_scores.merge(
            rag_scores[["row_id", "answer_correctness_rag", "question_rag", "question_key"]],
            on="row_id",
            how="inner",
            suffixes=("_no_rag", "_rag"),
        )

        paired["question_match"] = (
            paired["question"].apply(normalize_text)
            == paired["question_rag"].apply(normalize_text)
        )

        mismatch_count = int((~paired["question_match"]).sum())
        if mismatch_count > 0:
            print(
                f"\nPERINGATAN: Ada {mismatch_count} pasangan pertanyaan yang tidak identik berdasarkan urutan."
            )
            print("Jika urutan file tidak sama, jalankan ulang dengan: --align-by question")

    paired = paired.dropna(
        subset=["answer_correctness_no_rag", "answer_correctness_rag"]
    ).copy()

    paired["difference_rag_minus_no_rag"] = (
        paired["answer_correctness_rag"] - paired["answer_correctness_no_rag"]
    )

    return paired


def run_statistical_tests(paired: pd.DataFrame) -> pd.DataFrame:
    no_rag = paired["answer_correctness_no_rag"].astype(float)
    rag = paired["answer_correctness_rag"].astype(float)
    diff = paired["difference_rag_minus_no_rag"].astype(float)

    n = len(paired)

    if n < 3:
        raise ValueError("Data paired kurang dari 3, tidak cukup untuk uji statistik.")

    shapiro_stat, shapiro_p = stats.shapiro(diff)

    t_stat, t_p_two_sided = stats.ttest_rel(rag, no_rag, nan_policy="omit")

    try:
        wilcoxon_two = stats.wilcoxon(
            rag,
            no_rag,
            alternative="two-sided",
            zero_method="wilcox",
        )
        wilcoxon_greater = stats.wilcoxon(
            rag,
            no_rag,
            alternative="greater",
            zero_method="wilcox",
        )
        wilcoxon_stat_two = wilcoxon_two.statistic
        wilcoxon_p_two = wilcoxon_two.pvalue
        wilcoxon_stat_greater = wilcoxon_greater.statistic
        wilcoxon_p_greater = wilcoxon_greater.pvalue
    except ValueError:
        wilcoxon_stat_two = math.nan
        wilcoxon_p_two = math.nan
        wilcoxon_stat_greater = math.nan
        wilcoxon_p_greater = math.nan

    diff_std = diff.std(ddof=1)
    cohens_dz = diff.mean() / diff_std if diff_std != 0 else math.nan

    if shapiro_p >= 0.05:
        recommended_test = "paired sample t-test"
        recommended_p = t_p_two_sided
    else:
        recommended_test = "Wilcoxon signed-rank test"
        recommended_p = wilcoxon_p_two

    interpretation = (
        "signifikan pada alpha 0,05"
        if recommended_p < 0.05
        else "tidak signifikan pada alpha 0,05"
    )

    result = pd.DataFrame(
        [
            {
                "n": n,
                "mean_no_rag": no_rag.mean(),
                "mean_rag": rag.mean(),
                "median_no_rag": no_rag.median(),
                "median_rag": rag.median(),
                "mean_difference_rag_minus_no_rag": diff.mean(),
                "median_difference_rag_minus_no_rag": diff.median(),
                "std_difference": diff_std,
                "shapiro_statistic": shapiro_stat,
                "shapiro_p_value": shapiro_p,
                "paired_t_statistic": t_stat,
                "paired_t_p_value_two_sided": t_p_two_sided,
                "wilcoxon_statistic_two_sided": wilcoxon_stat_two,
                "wilcoxon_p_value_two_sided": wilcoxon_p_two,
                "wilcoxon_statistic_rag_greater": wilcoxon_stat_greater,
                "wilcoxon_p_value_rag_greater": wilcoxon_p_greater,
                "cohens_dz": cohens_dz,
                "recommended_test": recommended_test,
                "recommended_p_value": recommended_p,
                "interpretation": interpretation,
            }
        ]
    )

    return result


def print_results(stats_df: pd.DataFrame):
    r = stats_df.iloc[0]

    print("\n=== HASIL UJI STATISTIK ANSWER CORRECTNESS ===")
    print(f"n paired                              : {int(r['n'])}")
    print(f"Mean tanpa RAG                        : {r['mean_no_rag']:.4f}")
    print(f"Mean dengan RAG                       : {r['mean_rag']:.4f}")
    print(f"Mean difference RAG - tanpa RAG       : {r['mean_difference_rag_minus_no_rag']:.4f}")
    print(f"Shapiro-Wilk p-value                  : {r['shapiro_p_value']:.6g}")
    print(f"Paired t-test p-value two-sided       : {r['paired_t_p_value_two_sided']:.6g}")
    print(f"Wilcoxon p-value two-sided            : {r['wilcoxon_p_value_two_sided']:.6g}")
    print(f"Wilcoxon p-value RAG > tanpa RAG      : {r['wilcoxon_p_value_rag_greater']:.6g}")
    print(f"Cohen's dz                            : {r['cohens_dz']:.4f}")
    print(f"Uji yang direkomendasikan             : {r['recommended_test']}")
    print(f"p-value yang dilaporkan               : {r['recommended_p_value']:.6g}")
    print(f"Interpretasi                          : {r['interpretation']}")


def main():
    args = parse_args()

    input_no_rag = Path(args.input_no_rag)
    rag_csv = Path(args.rag_csv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    no_rag_scores_path = output_dir / "no_rag_answer_correctness.csv"
    paired_path = output_dir / "paired_answer_correctness_no_rag_vs_rag.csv"
    stats_path = output_dir / "statistical_test_answer_correctness.csv"

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY belum terbaca. Simpan di .env atau export OPENAI_API_KEY."
        )

    if args.skip_ragas:
        if not no_rag_scores_path.exists():
            raise FileNotFoundError(
                f"--skip-ragas digunakan, tetapi file belum ada: {no_rag_scores_path}"
            )

        no_rag_scores = pd.read_csv(no_rag_scores_path)

    else:
        reference_lookup = build_reference_lookup_from_rag(rag_csv)
        raw_no_rag_rows = read_input_file(input_no_rag)

        no_rag_df = normalize_no_rag_rows(
            raw_no_rag_rows,
            reference_lookup=reference_lookup,
            max_rows=args.max_rows,
        )

        print(f"Loaded no-RAG rows: {len(no_rag_df)}")
        print("\nSample no-RAG questions:")
        for q in no_rag_df["question"].head(5):
            print(f"- {q}")

        no_rag_scores = evaluate_no_rag_answer_correctness(
            no_rag_df,
            evaluator_model=args.evaluator_model,
            llm_max_tokens=args.llm_max_tokens,
        )

        no_rag_scores.to_csv(no_rag_scores_path, index=False, encoding="utf-8-sig")
        print(f"\nSaved no-RAG answer correctness: {no_rag_scores_path}")

    rag_scores = load_rag_scores(rag_csv, max_rows=args.max_rows)

    paired = pair_scores(
        no_rag_scores=no_rag_scores,
        rag_scores=rag_scores,
        align_by=args.align_by,
    )

    paired.to_csv(paired_path, index=False, encoding="utf-8-sig")
    print(f"Saved paired scores: {paired_path}")

    stats_df = run_statistical_tests(paired)
    stats_df.to_csv(stats_path, index=False, encoding="utf-8-sig")
    print(f"Saved statistical test result: {stats_path}")

    print_results(stats_df)


if __name__ == "__main__":
    main()