import json
import os

INPUT_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/02_regulation_index/regulation_index.json"
OUTPUT_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/02_regulation_index/regulation_categories.json"

CATEGORY_RULES = {
    "Administrasi & Tata Kelola Pemerintahan": [
        "perangkat",
        "organisasi",
        "kewenangan",
        "sekretariat",
        "pengawasan",
        "tim",
        "pembentukan",
        "pembubaran",
        "arsip",
        "tata kelola",
        "standar pelayanan",
    ],
    "Keuangan & Pengelolaan Anggaran": [
        "anggaran",
        "apbd",
        "akuntansi",
        "standar satuan harga",
        "ganti kerugian",
        "tambahan penghasilan",
        "bantuan operasional",
        "bos",
        "keuangan",
    ],
    "Perencanaan & RPJMD/RKPD": [
        "rpjmd",
        "rkpd",
        "rencana kerja",
        "renstra",
        "masterplan",
    ],
    "Pajak, Retribusi & Tarif": [
        "pajak",
        "retribusi",
        "tarif",
        "harga",
        "het",
    ],
    "Desa & Wilayah Administratif": [
        "desa",
        "kecamatan",
        "kelurahan",
    ],
    "Lingkungan & Tata Ruang": [
        "rtrw",
        "tata ruang",
        "lingkungan",
        "limbah",
    ],
    "Sosial, Pendidikan & Kesehatan": [
        "sosial",
        "kesejahteraan",
        "sekolah",
        "kesehatan",
        "rumah sakit",
    ],
    "Infrastruktur & Fasilitas Umum": [
        "jalan",
        "irigasi",
        "gedung",
        "perumahan",
        "smart city",
    ],
    "Investasi & BUMD": [
        "penyertaan modal",
        "bumd",
        "investasi",
    ],
    "Ketertiban & Regulasi Umum": [
        "ketertiban",
        "ketentraman",
        "sanksi",
    ],
}


def classify_title(title: str):
    title_lower = title.lower()
    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return "Administrasi & Tata Kelola Pemerintahan"


with open(INPUT_PATH, "r", encoding="utf-8") as f:
    regulations = json.load(f)

classified = []
category_count = {}

for reg in regulations:
    category = classify_title(reg["judul"])
    classified.append({"regulation_id": reg["regulation_id"], "category": category})
    category_count[category] = category_count.get(category, 0) + 1

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(classified, f, indent=2, ensure_ascii=False)

print("Classification completed!")
print("Category distribution:")

for cat, count in sorted(category_count.items(), key=lambda x: -x[1]):
    print(f"{cat}: {count}")


# OUTPUT
# Classification completed!
# Category distribution:
# Administrasi & Tata Kelola Pemerintahan: 179
# Keuangan & Pengelolaan Anggaran: 94
# Desa & Wilayah Administratif: 45
# Pajak, Retribusi & Tarif: 24
# Lingkungan & Tata Ruang: 22
# Sosial, Pendidikan & Kesehatan: 17
# Perencanaan & RPJMD/RKPD: 12
# Infrastruktur & Fasilitas Umum: 5
# Ketertiban & Regulasi Umum: 1
# Investasi & BUMD: 1
