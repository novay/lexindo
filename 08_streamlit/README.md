# Streamlit Implementation

Folder ini berisi **antarmuka pengguna (UI)** berbasis Streamlit untuk LexIndoLLM. Ini adalah prototipe aplikasi konsultasi regulasi daerah yang siap digunakan secara lokal oleh warga atau pegawai pemerintahan.

Aplikasi ini mengintegrasikan model *fine-tuned* (`lexindo_2e`) dengan sistem RAG (FAISS) dan menyediakan pengalaman *chat* interaktif yang ramah, responsif, dan 100% offline.

## 🎯 Fitur Utama

- Multi-session chat (bisa buat chat baru, switch antar sesi)
- Riwayat chat disimpan permanen di `chat_history.json` (auto-save)
- Toggle RAG ON/OFF dengan expander referensi dokumen
- Pemilihan model Ollama (default LexIndoLLM + alternatif lain)
- Pengaturan temperature
- Tampilan metadata regulasi (jenis, nomor, tahun, judul) saat RAG aktif

## 📁 Struktur Folder

```bash
08_streamlit/
├── app.py                    # Aplikasi utama Streamlit
├── chat_history.json         # File JSON penyimpanan riwayat chat (auto-generated)
└── README.md
```

## 🚀 Cara Menjalankan

1. Pastikan FAISS index sudah ada di folder `05_rag_corpus/faiss_index_lexindo`
2. Pastikan Ollama sudah running dan model `hf.co/nxvay/lexindo_2e:q4_k_m` atau `lexindo-custom` sudah dibuat
3. Jalankan perintah berikut:

```bash
cd 08_streamlit
streamlit run app.py
```

Atau dari root repo:
```bash
streamlit run 08_streamlit/app.py
```

## ⚙️ Catatan Penting di app.py

- `DEFAULT_MODEL` = `"hf.co/nxvay/lexindo_2e:q4_k_m"`
- `FAISS_INDEX_PATH` → masih hard-coded (perlu penyesuaian relative path)
- `EMBEDDING_MODEL` = `"intfloat/multilingual-e5-large-instruct"`
- Riwayat chat disimpan otomatis setiap ada pesan baru

## 🔗 Referensi Tesis

- **Bagian 3.5** – Antarmuka Pengguna (halaman 27–28 tesis)
- **Gambar 2** – Tampilan antarmuka Streamlit (halaman 28 tesis)
- **Bagian 4.3** – Dampak Integrasi RAG terhadap user experience

**File referensi lengkap:** [`../docs/3-tesis.pdf`](../docs/3-tesis.pdf)

---