import json
import os
import random
from typing import Dict, List


def load_all_jsonl(root_dir: str) -> List[Dict]:
    all_data = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".jsonl"):
                file_path = os.path.join(subdir, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            all_data.append(entry)
                        except json.JSONDecodeError:
                            print(f"Warning: Invalid JSON in {file_path}")
    return all_data


def split_data(data: List[Dict], train_ratio=0.8, val_ratio=0.1) -> tuple:
    random.shuffle(data)
    total = len(data)
    train_end = int(total * train_ratio)
    val_end = int(total * (train_ratio + val_ratio))
    train = data[:train_end]
    val = data[train_end:val_end]
    test = data[val_end:]
    return train, val, test


def save_jsonl(data: List[Dict], output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def extract_for_ragas(test_data: List[Dict], output_path: str):
    ragas_data = []
    for entry in test_data:
        if "conversations" in entry and len(entry["conversations"]) >= 2:
            human = entry["conversations"][0]["value"]
            gpt = entry["conversations"][1]["value"]
            # Extract context: Asumsikan bagian setelah "Sumber:" adalah context
            if "(Sumber:" in gpt:
                answer_clean, context = gpt.split("(Sumber:", 1)
                context = "(Sumber:" + context.strip()
            else:
                answer_clean = gpt
                context = ""  # Jika tidak ada, kosongkan (nanti tambah manual)
            ragas_entry = {
                "question": human.strip(),
                "ground_truth": gpt.strip(),
                "answer": answer_clean.strip(),  # Untuk compare
                "contexts": [context.strip()] if context else [],
            }
            ragas_data.append(ragas_entry)
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in ragas_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# Jalankan
root_dir = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/03_finetune_dataset/dataset"  # Ganti jika beda
all_data = load_all_jsonl(root_dir)
print(f"Total entries: {len(all_data)}")

train, val, test = split_data(all_data)

save_jsonl(
    train,
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/03_finetune_dataset/mlx_data/train.jsonl",
)
save_jsonl(
    val,
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/03_finetune_dataset/mlx_data/val.jsonl",
)
save_jsonl(
    test,
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/03_finetune_dataset/mlx_data/test.jsonl",
)

# Untuk RAGAS: Generate eval set khusus
extract_for_ragas(
    test,
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/03_finetune_dataset/mlx_data/ragas_eval.jsonl",
)

print("Dataset siap: train.jsonl, val.jsonl, test.jsonl, ragas_eval.jsonl")
