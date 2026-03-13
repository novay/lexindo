from datasets import load_dataset
import json
import os
import random

# 1. Konfigurasi Folder Output (Sesuaikan path jika perlu)
output_dir = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_02/data"
os.makedirs(output_dir, exist_ok=True)

print("Mengunduh dataset dari Hugging Face...")

# 2. Ambil dataset langsung dari Hugging Face
dataset = load_dataset("FreedomIntelligence/alpaca-gpt4-indonesian", split="train")

print("\n[INFO] Struktur kolom dataset pertama:", dataset[0].keys())

# 3. Format ke JSONL (Chat Template)
formatted_data = []
for row in dataset:
    conversations = row.get("conversations", [])
    
    messages = []
    for turn in conversations:
        # Ambil identitas pengirim dan isi pesannya
        role_awal = turn.get("from", "").lower()
        content = turn.get("value", "").strip()
        
        # Lewati jika pesannya kosong
        if not content:
            continue
            
        # Konversi nama 'from' menjadi format LLaMA ('user' dan 'assistant')
        if role_awal == "human":
            messages.append({"role": "user", "content": content})
        elif role_awal == "gpt":
            messages.append({"role": "assistant", "content": content})
            
    # Pastikan dalam 1 baris percakapan minimal ada tanya dan jawab
    if len(messages) >= 2:
        percakapan = {"messages": messages}
        formatted_data.append(percakapan)

print(f"[INFO] Total data valid yang berhasil diformat: {len(formatted_data)}")

# Hentikan program jika datanya kosong
if len(formatted_data) == 0:
    print("\n[ERROR] Data gagal diproses! Format tidak cocok.")
    exit()

# 4. Acak dan Split Dataset (Ambil 10.000 data agar training optimal & tidak terlalu lama)
random.shuffle(formatted_data)

# Jika ingin menggunakan SEMUA data, hapus bagian [:10000] di bawah
sample_data = formatted_data[:10000] 

total = len(sample_data)
train_end = int(total * 0.9)  # 90% untuk Train
valid_end = train_end + int(total * 0.05) # 5% untuk Valid, 5% untuk Test

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
print("Selesai! Data siap digunakan untuk MLX Tahap 2.")