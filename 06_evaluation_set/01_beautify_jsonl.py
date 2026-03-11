import json

input_file = '/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/05_evaluation_set/ragas_eval.jsonl'
output_file = '/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/05_evaluation_set/ragas_eval_beautified.jsonl'

# List untuk menampung data yang sudah diupdate
updated_data = []

# 1. Membaca dan Menambahkan Kolom Baru
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        # Load setiap baris sebagai dictionary
        item = json.loads(line)
        
        # Menambahkan kolom baru dengan nilai kosong
        item["answer_base"] = ""
        item["answer_finetuned_no_rag"] = ""
        item["answer_finetuned_rag"] = ""
        
        updated_data.append(item)

# 2. Menyimpan kembali ke format JSONL yang rapi (Beautified)
with open(output_file, 'w', encoding='utf-8') as f:
    for entry in updated_data:
        # indent=2 membuat format JSON menjadi "cantik" dan mudah dibaca
        json_record = json.dumps(entry, ensure_ascii=False, indent=2)
        f.write(json_record + '\n')

print(f"Selesai! File telah disimpan di: {output_file}")