import json
import os

RAW_DATA_PATH = "./../01_raw_data"
OUTPUT_PATH = "./../02_regulation_index/regulation_index.json"

ID_YEARS = [2020, 2021, 2022, 2023]
OOD_YEARS = [2024, 2025]

regulation_index = []


def determine_year_group(year: int):
    if year in ID_YEARS:
        return "ID"
    elif year in OOD_YEARS:
        return "OOD"
    else:
        return "UNKNOWN"


for year_folder in sorted(os.listdir(RAW_DATA_PATH)):
    year_path = os.path.join(RAW_DATA_PATH, year_folder)

    if not os.path.isdir(year_path):
        continue

    for file_name in sorted(os.listdir(year_path)):
        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(year_path, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data:
            continue

        metadata = data[0]["metadata"]

        regulation_id = file_name.replace(".json", "")

        tahun = int(metadata["tahun"])

        regulation_entry = {
            "regulation_id": regulation_id,
            "file_name": metadata["source"],
            "jenis": metadata["jenis"],
            "nomor": metadata["nomor"],
            "tahun": tahun,
            "judul": metadata["judul"],
            "status": metadata["status"],
            "year_group": determine_year_group(tahun),
            "evaluation_candidate": True,
        }

        regulation_index.append(regulation_entry)

# Validasi uniqueness
ids = [r["regulation_id"] for r in regulation_index]
assert len(ids) == len(set(ids)), "Duplicate regulation_id detected!"

# Simpan hasil
os.makedirs("02_regulation_index", exist_ok=True)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(regulation_index, f, indent=2, ensure_ascii=False)

print("Regulation index created successfully!")
print(f"Total regulations: {len(regulation_index)}")

# Statistik ringkas
perbup = sum(1 for r in regulation_index if r["jenis"] == "Peraturan Bupati")
perda = sum(1 for r in regulation_index if r["jenis"] == "Peraturan Daerah")

id_group = sum(1 for r in regulation_index if r["year_group"] == "ID")
ood_group = sum(1 for r in regulation_index if r["year_group"] == "OOD")

print(f"Perbup: {perbup}")
print(f"Perda: {perda}")
print(f"ID group: {id_group}")
print(f"OOD group: {ood_group}")
