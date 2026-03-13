from datasets import load_dataset
import json
import os
import random

# 1. Konfigurasi Folder Output untuk Tahap 3
output_dir = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_03/data"
os.makedirs(output_dir, exist_ok=True)

print("Mengunduh dataset regulasi dari Hugging Face...")

# 2. Ambil dataset langsung dari Hugging Face
dataset = load_dataset("nxvay/lexindo-kukarkab-alpaca", split="train")

# Intip struktur datanya untuk memastikan nama kolom (keys)
print("\n[INFO] Struktur kolom dataset pertama:", dataset[0].keys())

# 3. Format ke JSONL (Chat Template LLaMA 3)
formatted_data = []
for row in dataset:
    # Mengambil data sesuai format standar Alpaca
    instruction = row.get("instruction", "").strip()
    input_text = row.get("input", "").strip()
    output_text = row.get("output", "").strip()
    
    # Jika instruksi dan output kosong, lewati baris ini agar tidak error
    if not instruction and not output_text:
        continue
        
    # Gabungkan instruksi dan input jika input tersedia (misalnya nama pasal/bab)
    if input_text:
        user_content = f"{instruction}\n\n{input_text}"
    else:
        user_content = instruction
        
    percakapan = {
        "messages": [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": output_text}
        ]
    }
    formatted_data.append(percakapan)

print(f"[INFO] Total data regulasi yang berhasil diformat: {len(formatted_data)}")

# Hentikan program jika ternyata datanya kosong
if len(formatted_data) == 0:
    print("\n[ERROR] Data gagal diproses! Format kolom mungkin berbeda. Cek print struktur di atas.")
    exit()

# 4. Acak dan Split Dataset 
random.shuffle(formatted_data)

# Jika datasetnya besar, saya batasi dulu (misal 10.000) agar training di RAM 8GB tidak meledak.
# Kalau datanya sedikit (misal di bawah 5.000), biarkan saja script ini mengambil semuanya.
sample_data = formatted_data[:10000] 

total = len(sample_data)
train_end = int(total * 0.9)  # 90% Train
valid_end = train_end + int(total * 0.05) # 5% Valid, sisanya 5% Test

train_data = sample_data[:train_end]
valid_data = sample_data[train_end:valid_end]
test_data = sample_data[valid_end:]

def save_jsonl(data, filename):
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

# 5. Simpan file
print("\nMenyimpan file train.jsonl, valid.jsonl, dan test.jsonl...")
save_jsonl(train_data, "train.jsonl")
save_jsonl(valid_data, "valid.jsonl")
save_jsonl(test_data, "test.jsonl")
print("Selesai! Data regulasi siap di-training di MLX Tahap 3.")