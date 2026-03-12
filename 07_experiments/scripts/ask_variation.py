import json
import random

variasi_pertanyaan = [
    # --- Variasi Standar & Formal ---
    "Tolong jelaskan apa itu {}.",
    "Apa yang dimaksud dengan {}?",
    "Bisa berikan definisi dari {}?",
    "Jelaskan pengertian dari istilah {} menurut aturan yang berlaku.",
    "Apa pengertian dari {}?",
    "Mohon penjelasan mengenai makna istilah {}.",
    "Bisa tolong uraikan pengertian dari {}?",
    "Secara harfiah, apa yang dimaksud dengan {}?",
    "Sebutkan definisi lengkap dari {}.",
    "Berikan penjelasan singkat mengenai apa itu {}.",
    "Bisakah kamu mendefinisikan istilah {} untuk saya?",

    # --- Variasi Percakapan / Kasual ---
    "Saya kurang paham tentang {}. Itu maksudnya apa?",
    "{} itu artinya apa ya?",
    "Aku sering dengar istilah {}. Itu sebenarnya apa sih?",
    "Kasih tahu dong arti dari {}.",
    "Bisa bantu jelaskan konsep {} ke saya?",
    "Maksud dari kata {} itu apa, ya?",
    "Kalau {} itu definisinya apa?",
    "Tolong jabarkan dong apa itu {}.",
    "Apakah kamu tahu apa arti dari istilah {}?",
    "Saya butuh penjelasan tentang apa itu {}. Bisa bantu?",
    "Bisa tolong beri tahu saya apa makna dari {}?",
    "Bantu saya memahami istilah {}. Apa itu?",
    "Gimana sih penjelasan sederhana tentang {}?",
    "Apa sih yang dimaksud dengan {}? Tolong jelaskan.",
    "Kata {} ini merujuk pada apa ya?",
    "Tolong artikan istilah {} ini dong.",
    "Saya lagi belajar istilah ini, {} itu artinya apa?"
]

file_input = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_01/data/train.jsonl"
file_output = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_01/data/train_variasi.jsonl"

hasil_variasi = []

with open(file_input, 'r', encoding='utf-8') as f:
    for baris in f:
        if not baris.strip(): # Abaikan baris kosong jika ada
            continue
            
        data = json.loads(baris)
        pertanyaan_lama = data["messages"][0]["content"]
        
        if "Apa definisi dari istilah:" in pertanyaan_lama:
            istilah = pertanyaan_lama.replace("Apa definisi dari istilah:", "").replace("?", "").strip()
            
            # Pilih template pertanyaan secara acak dan masukkan istilahnya
            pertanyaan_baru = random.choice(variasi_pertanyaan).format(istilah)
            
            # Ganti pertanyaan lama dengan yang baru
            data["messages"][0]["content"] = pertanyaan_baru
            
        jawaban_lama = data["messages"][1]["content"]
        if jawaban_lama:
            # Kapitalisasi huruf pertama
            jawaban_baru = jawaban_lama[0].upper() + jawaban_lama[1:]
            # Tambahkan titik di akhir jika belum ada
            if not jawaban_baru.endswith('.'):
                jawaban_baru += '.'
            data["messages"][1]["content"] = jawaban_baru
            
        hasil_variasi.append(json.dumps(data, ensure_ascii=False))

with open(file_output, 'w', encoding='utf-8') as f:
    for hasil in hasil_variasi:
        f.write(hasil + '\n')

print(f"Selesai! {len(hasil_variasi)} baris data telah divariasikan dan disimpan ke:")
print(file_output)