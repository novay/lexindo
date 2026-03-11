# Dataset Preparation

Folder ini berisi **tahap persiapan dataset** setelah data mentah dari `01_raw_data`. Proses ini mengubah regulasi daerah menjadi format ShareGPT (JSONL) yang siap untuk fine-tuning MLX.

## 🎯 Tujuan
- Membersihkan teks regulasi
- Membuat pasangan Question-Answer synthetic
- Split dataset menjadi train/valid/test
- Konversi ke format chat yang kompatibel dengan Llama-3.2-1B

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

## 🔧 Cara Kerja

1. Ambil JSON dari tahun 2020–2025
2. Generate QA synthetic
3. Split 80/10/10
4. Convert ke ShareGPT format

**Output utama** digunakan langsung di folder `04_finetune/data/`.

🔗 Referensi Tesis

- Bagian 3.2.2 – Persiapan Dataset (halaman 21–23 tesis)
- Tabel 3 – Sebaran regulasi daerah 2020–2025

File referensi lengkap: `../docs/3-tesis.pdf`

---