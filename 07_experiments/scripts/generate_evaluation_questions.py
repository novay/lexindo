import json
import os
import random

random.seed(42)

RAW_DATA_PATH = (
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/01_raw_data"
)
EVAL_IDS_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/05_evaluation_set/evaluation_regulation_ids.json"
INDEX_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/02_regulation_index/regulation_index.json"
CATEGORY_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/02_regulation_index/regulation_categories.json"

OUTPUT_QUESTIONS_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/05_evaluation_set/evaluation_questions.json"
OUTPUT_GT_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/05_evaluation_set/evaluation_ground_truth.json"

# Load evaluation IDs
with open(EVAL_IDS_PATH, "r", encoding="utf-8") as f:
    eval_ids = json.load(f)

# Load regulation index
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    reg_index = json.load(f)

reg_map = {r["regulation_id"]: r for r in reg_index}

# Load categories
with open(CATEGORY_PATH, "r", encoding="utf-8") as f:
    categories = json.load(f)

cat_map = {c["regulation_id"]: c["category"] for c in categories}

questions = []
ground_truth = []

question_counter = 1


def generate_question_template(pasal):
    templates = [
        f"Apa ketentuan yang diatur dalam {pasal} peraturan ini?",
        f"Apa isi atau substansi yang diatur dalam {pasal}?",
        f"Apa yang dijelaskan dalam {pasal} peraturan tersebut?",
        f"Apa yang menjadi pengaturan utama dalam {pasal}?",
    ]
    return random.choice(templates)


for reg_id in eval_ids:
    tahun = reg_map[reg_id]["tahun"]
    jenis = reg_map[reg_id]["jenis"]
    category = cat_map.get(reg_id, "Unknown")

    # Determine year folder
    year_folder = str(tahun)
    file_path = os.path.join(RAW_DATA_PATH, year_folder, f"{reg_id}.json")

    if not os.path.exists(file_path):
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    valid_chunks = []

    for chunk in data:
        pasal = chunk["metadata"].get("pasal")
        bab = chunk["metadata"].get("bab")

        if pasal is None:
            continue

        if bab == "Lampiran":
            continue

        if "-" in pasal:
            continue

        valid_chunks.append(chunk)

    if not valid_chunks:
        continue

    chosen_chunk = random.choice(valid_chunks)
    pasal_target = chosen_chunk["metadata"]["pasal"]
    context_text = chosen_chunk["page_content"]

    question_text = generate_question_template(pasal_target)

    question_id = f"Q{str(question_counter).zfill(3)}"

    questions.append(
        {
            "question_id": question_id,
            "regulation_id": reg_id,
            "tahun": tahun,
            "jenis": jenis,
            "category": category,
            "pasal_target": pasal_target,
            "question": question_text,
        }
    )

    ground_truth.append(
        {
            "question_id": question_id,
            "ground_truth_reference": f"{reg_id} {pasal_target}",
            "ground_truth_context": context_text,
        }
    )

    question_counter += 1

# Save outputs
os.makedirs(
    "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/05_evaluation_set",
    exist_ok=True,
)

with open(OUTPUT_QUESTIONS_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

with open(OUTPUT_GT_PATH, "w", encoding="utf-8") as f:
    json.dump(ground_truth, f, indent=2, ensure_ascii=False)

print("Evaluation question generation completed!")
print(f"Total questions generated: {len(questions)}")

# OUTPUT
# Evaluation question generation completed!
# Total questions generated: 100
