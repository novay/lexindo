import json
import os
import random
from collections import defaultdict

random.seed(42)

INDEX_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/02_regulation_index/regulation_index.json"
CATEGORY_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/02_regulation_index/regulation_categories.json"

OUTPUT_SPLIT_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/02_regulation_index/regulation_split.json"
OUTPUT_EVAL_IDS_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/05_evaluation_set/evaluation_regulation_ids.json"

EVAL_TOTAL = 100
EVAL_ID_TOTAL = 70
EVAL_OOD_TOTAL = 30

# Load data
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    regulations = json.load(f)

with open(CATEGORY_PATH, "r", encoding="utf-8") as f:
    categories = json.load(f)

# Merge category into regulation index
category_map = {c["regulation_id"]: c["category"] for c in categories}

for reg in regulations:
    reg["category"] = category_map.get(reg["regulation_id"], "Unknown")

# Separate ID and OOD
id_regs = [r for r in regulations if r["year_group"] == "ID"]
ood_regs = [r for r in regulations if r["year_group"] == "OOD"]


def stratified_sample(reg_list, target_total):
    grouped = defaultdict(list)

    for r in reg_list:
        grouped[r["category"]].append(r)

    total = len(reg_list)
    sampled = []

    for category, items in grouped.items():
        proportion = len(items) / total
        n_sample = round(proportion * target_total)

        sampled.extend(random.sample(items, min(n_sample, len(items))))

    # Adjust if rounding mismatch
    if len(sampled) > target_total:
        sampled = random.sample(sampled, target_total)
    elif len(sampled) < target_total:
        remaining = [r for r in reg_list if r not in sampled]
        sampled.extend(random.sample(remaining, target_total - len(sampled)))

    return sampled


# Perform sampling
eval_id = stratified_sample(id_regs, EVAL_ID_TOTAL)
eval_ood = stratified_sample(ood_regs, EVAL_OOD_TOTAL)

evaluation_regs = eval_id + eval_ood

eval_ids = [r["regulation_id"] for r in evaluation_regs]

# Remaining for fine-tuning
finetune_regs = [
    r["regulation_id"] for r in regulations if r["regulation_id"] not in eval_ids
]

# Save split
os.makedirs(
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/02_regulation_index",
    exist_ok=True,
)
os.makedirs(
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/05_evaluation_set",
    exist_ok=True,
)

split_data = {
    "finetune": finetune_regs,
    "evaluation_id": [r["regulation_id"] for r in eval_id],
    "evaluation_ood": [r["regulation_id"] for r in eval_ood],
}

with open(OUTPUT_SPLIT_PATH, "w", encoding="utf-8") as f:
    json.dump(split_data, f, indent=2, ensure_ascii=False)

with open(OUTPUT_EVAL_IDS_PATH, "w", encoding="utf-8") as f:
    json.dump(eval_ids, f, indent=2, ensure_ascii=False)

print("Split completed!")
print(f"Fine-tuning set: {len(finetune_regs)}")
print(f"Evaluation ID: {len(eval_id)}")
print(f"Evaluation OOD: {len(eval_ood)}")


# OUTPUT
# Split completed!
# Fine-tuning set: 300
# Evaluation ID: 70
# Evaluation OOD: 30
