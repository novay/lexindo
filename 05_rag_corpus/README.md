# RAG Corpus Implementation

Folder ini berisi **corpus RAG (Retrieval-Augmented Generation)** yang digunakan untuk grounding jawaban LexIndoLLM agar tidak halusinasi dan selalu bisa dilacak ke regulasi asli.

Corpus dibangun dari semua file JSON hasil *pre-processing* di folder `02_dataset_preparation` dan `01_raw_data`.

## 🎯 Tujuan

- Membuat *vector database* lokal (FAISS) untuk *retrieval* cepat
- Menggunakan *embedding multilingual* yang kuat untuk bahasa Indonesia + hukum daerah
- Memastikan setiap jawaban selalu disertai referensi pasal regulasi asli

## 📁 Struktur Folder

```bash
05_rag_corpus/
├── faiss_index_lexindo/     # Folder index FAISS yang sudah dibuild
├── build.py                 # Script pembuatan corpus & index
└── README.md
```

## 🔧 Script Utama: build.py

Script ini melakukan:
1. Load semua file `.json` dari `01_raw_data` (semua tahun)
2. Konversi menjadi `Document` LangChain
3. Embedding dengan `intfloat/multilingual-e5-large-instruct` (*accelerate* pakai MPS di Apple Silicon)
4. Build FAISS index
5. Simpan index ke `faiss_index_lexindo/`

**Hasil eksekusi terakhir:**
- Found 398 JSON files
- Loaded 6471 document chunks
- Index berhasil disimpan di `faiss_index_lexindo`

## 🚀 Cara Menjalankan Ulang

```bash
cd 05_rag_corpus
python build.py
```

Setelah selesai, folder `faiss_index_lexindo` akan otomatis digunakan oleh `08_streamlit/app.py`.

## 🔗 Referensi Tesis

- **Bagian 3.4** – RAG & Evaluation Phase (halaman 25–27 tesis)
- **Bagian 4.3** – Dampak Integrasi RAG (halaman 63–65 tesis)
- Embedding model: `intfloat/multilingual-e5-large-instruct`

**File referensi lengkap:** [`../docs/3-tesis.pdf`](../docs/3-tesis.pdf)