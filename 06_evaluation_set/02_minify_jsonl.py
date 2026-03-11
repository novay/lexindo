import json

input_file = '/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/05_evaluation_set/ragas_eval_beautified.jsonl'
output_file = '/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/05_evaluation_set/ragas_eval_minified.jsonl'

# List untuk menampung data
minified_data = []

# 1. Membaca data
# Jika file kamu berisi beberapa objek JSON yang terpisah (multi-line)
# Kita perlu membacanya dengan hati-hati
with open(input_file, 'r', encoding='utf-8') as f:
    # Jika file tersebut adalah format JSON murni (list of dicts)
    # Gunakan data = json.load(f)
    # Tapi jika file tersebut adalah kumpulan JSON yang dipisah newline:
    content = f.read()
    
    # Teknik sederhana: memisahkan berdasarkan '}\n{' untuk mendeteksi batas objek
    # Atau jika file kamu valid JSONL, kita bisa menggunakan loop standar
    try:
        # Mencoba membaca jika formatnya adalah list [{}, {}]
        data = json.loads(content)
    except json.JSONDecodeError:
        # Jika bukan list, kita asumsikan ini adalah kumpulan blok JSON
        # Kita parse per blok (menggunakan pemisah yang dihasilkan script sebelumnya)
        import re
        # Mencari pola objek JSON { ... }
        blocks = re.findall(r'\{.*?\}(?=\n\{|\n$|$)', content, re.DOTALL)
        data = [json.loads(b) for b in blocks]

# 2. Menyimpan kembali ke format MINIFIED (satu baris satu JSON)
with open(output_file, 'w', encoding='utf-8') as f:
    for entry in data:
        # Hilangkan indent dan separators default untuk hasil paling ringkas
        json_line = json.dumps(entry, ensure_ascii=False, separators=(',', ':'))
        f.write(json_line + '\n')

print(f"Berhasil! File terminify disimpan di: {output_file}")