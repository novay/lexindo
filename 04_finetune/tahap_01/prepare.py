import csv
import json
import random
import os

# 1. Konfigurasi
input_csv = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_01/dataset.csv"
output_dir = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_01/data"

# Pastikan folder output tersedia
os.makedirs(output_dir, exist_ok=True)

# 2. Baca file CSV
dataset = []
with open(input_csv, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        istilah = row['Istilah'].strip()
        definisi = row['Definisi'].strip()
        
        # Buat format percakapan (chat template)
        percakapan = {
            "messages": [
                {"role": "user", "content": f"Apa definisi dari istilah: {istilah}?"},
                {"role": "assistant", "content": definisi}
            ]
        }
        dataset.append(percakapan)

# 3. Acak data agar distribusinya merata
random.shuffle(dataset)

# 4. Tentukan proporsi split (80% Train, 10% Valid, 10% Test)
total_data = len(dataset)
train_end = int(total_data * 0.8)
valid_end = train_end + int(total_data * 0.1)

train_data = dataset[:train_end]
valid_data = dataset[train_end:valid_end]
test_data = dataset[valid_end:]

# 5. Fungsi untuk menyimpan ke JSONL
def save_jsonl(data, filename):
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"Berhasil menyimpan {len(data)} baris ke {filepath}")

# 6. Simpan file
save_jsonl(train_data, "train.jsonl")
save_jsonl(valid_data, "valid.jsonl")
save_jsonl(test_data, "test.jsonl")

print("Selesai! Data siap digunakan untuk mlx_lm.lora")

# OUTPUT
# Berhasil menyimpan 1408 baris ke ./data/train.jsonl
# Berhasil menyimpan 176 baris ke ./data/valid.jsonl
# Berhasil menyimpan 177 baris ke ./data/test.jsonl
# Selesai! Data siap digunakan untuk mlx_lm.lora