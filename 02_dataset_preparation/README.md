# Dataset Preparation

Folder ini berisi **tahap persiapan dataset regulasi daerah** yang digunakan pada **Tahap 3 Fine-tuning** *(Regulation-specific Tuning)* dari LexIndoLLM.

Dataset ini merupakan hasil akhir dari proses persiapan dan kurasi dari regulasi Kutai Kartanegara (2020–2025) yang telah di-upload ke Hugging Face untuk kemudahan reprodusibilitas.

## 🎯 Tujuan

- Membersihkan teks regulasi daerah dari PDF → JSON
- Membuat pasangan Question-Answer synthetic berkualitas tinggi
- Split dataset menjadi train/valid/test (80/10/10)
- Konversi ke format ShareGPT / Alpaca yang kompatibel dengan Llama-3.2-1B

**Dataset akhir ini digunakan khusus untuk Tahap 3 Regulation-specific Tuning.**

## 📁 Struktur Folder

```bash
02_dataset_preparation/
├── split/                    # Folder sementara hasil splitting
├── train.jsonl               # Dataset training (utama)
├── valid.jsonl               # Dataset validasi
├── test.jsonl                # Dataset test
├── convert_to_chat_format.py # Script konversi ke format chat
├── dataset_preparation.py    # Script utama preprocessing
└── README.md
```

## 🔧 Metode Generasi Synthetic Data

Proses pembuatan QA synthetic menggunakan **system prompt khusus** yang dirancang untuk menjaga akurasi hukum dan menghindari halusinasi.

**Karakteristik utama:**
- **3 Mode Wajib** per entry regulasi:
  1. **Full Grounding Mode** → Jawaban dimulai dengan “Berdasarkan {jenis} {nomor} tentang {judul}, {pasal} menyatakan bahwa:” lalu salin pasal **utuh** tanpa meringkas.
  2. **Ekstraksi Spesifik Mode** → Hanya kutip bagian relevan dengan tetap menyebut dasar hukum.
  3. **Terstruktur Mode** (jika ada daftar) → Sajikan dalam bentuk list bernomor tanpa mengubah redaksi asli.

- **Aturan Ketat**:
  - Tidak boleh halusinasi atau parafrase isi hukum
  - Tidak boleh menggabungkan regulasi berbeda
  - Selalu preserve teks asli (normatif & formal)
  - Minimal 3–5 percakapan per entry regulasi
  - Output murni JSONL (ShareGPT format)

Prompt ini dikembangkan dengan bantuan Gemini Pro dan ChatGPT-4 untuk memastikan presisi, konsistensi, dan kualitas normatif yang tinggi.

## 🔧 Hubungan dengan 3 Tahap Fine-tuning

1. **Tahap 1** – Language & Glossary Adaptation  
   (menggunakan kamus hukum BPK + Black’s Law Dictionary)

2. **Tahap 2** – Instruction Tuning  
   (menggunakan dataset open-source FreedomIntelligence)

3. **Tahap 3** – Regulation-specific Tuning ← **Dataset dari folder ini**  
   → Di-upload ke Hugging Face:  
   **https://huggingface.co/datasets/nxvay/lexindo-kukarkab-alpaca**

## 🚀 Cara Kerja

1. Ambil JSON regulasi dari tahun 2020–2025
2. Generate QA synthetic (berbasis regulasi asli)
3. Split 80/10/10
4. Convert ke format ShareGPT/Alpaca
5. Upload ke Hugging Face (dataset final)

**Output utama** (`train.jsonl`) digunakan langsung di folder `04_finetune/data/` untuk training tahap ketiga.

## 🔗 Referensi Tesis

- **Bagian 3.2.2** – Persiapan Dataset (halaman 21–23 tesis)
- **Bagian 3.3** – Tahap 3 Regulation-specific Tuning (halaman 23–25 tesis)
- **Tabel 3** – Sebaran regulasi daerah 2020–2025

**File referensi lengkap:** [`../docs/3-tesis.pdf`](../docs/3-tesis.pdf)

**Dataset publik:** [nxvay/lexindo-kukarkab-alpaca](https://huggingface.co/datasets/nxvay/lexindo-kukarkab-alpaca)
```

---