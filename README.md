# LexIndoLLM Repository

**Large Language Model Khusus Regulasi Daerah Indonesia**  
*Studi Kasus: Kabupaten Kutai Kartanegara*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Llama](https://img.shields.io/badge/Llama-3.2-FF9900)](https://llama.meta.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Repository resmi **tesis S2 Teknik Informatika** Universitas Amikom Yogyakarta  
**NIM: 22.55.2293** — Novianto Rahmadi

**Paper terkait**:  
- LexIndoLLM: Large Language Model untuk Konsultasi Regulasi Daerah di Indonesia

## ✨ Fitur Utama
- Model ringan **Llama 3.2-1B** (1 miliar parameter)
- Fine-tuning bertahap domain-spesifik + RAG berbasis FAISS
- **Faithfulness 0.77** & **Answer Correctness 0.66** (RAGAS)
- Latency rata-rata **< 3.4 detik** (bisa jalan di laptop biasa)
- 100% *offline* & lokal *deployment*
- Antarmuka **Streamlit** yang *user-friendly* dengan riwayat chat

## 🎥 Demo Video
...Menyusul...

## 📁 Struktur Repository
```bash
lexindo/
├── 01_raw_data/              # Data mentah Perda & Perbup
├── 02_dataset_preparation/   # JSONL ShareGPT (11.190 pasang)
├── 03_base_model/            # Pengujian pra-seleksi base model (evaluation.ipynb)
├── 04_finetune/              # 3 tahap fine-tuning (Unsloth)
├── 05_rag_corpus/            # FAISS index + embedding
├── 06_evaluation_set/        # Hasil RAGAS & human eval
├── 07_experiments/               # Log eksperimen & notebook tambahan
├── 08_streamlit/             # Chat UI
├── docs/                     # Tesis lengkap + Jurnal PDF
├── CITATION.cff
├── LICENSE
└── README.md
```

## 🚀 Quick Start

```bash
git clone https://github.com/novay/lexindo.git
cd lexindo

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run 08_streamlit/app.py
```

## 📊 Hasil Utama
- **Perplexity**: 9.13 → **1.74** (↓80.9%)
- **ROUGE-L**: 0.2058 → **0.4429**
- **Faithfulness**: 0.4783 → **0.7739** (setelah fine-tuning)
- **Answer Correctness** (dengan RAG): **0.6603**
- **Human Evaluation** (5 pakar hukum): rata-rata **4.40 / 5.00**

## 📄 Citation

```bibtex
@article{rahmadi2026lexindollm,
  title={LexIndoLLM: Large Language Model untuk Konsultasi Regulasi Daerah di Indonesia},
  author={Rahmadi, Novianto and Setyanto, Arief},
  journal={...},
  year={2026},
  doi={...}
}
```

**License**: MIT  
**Disclaimer**: Dataset regulasi hanya untuk keperluan akademik dan riset non-komersial.

**Terima kasih** kepada dosen pembimbing, pengelola dokumen Kutai Kartanegara, dan semua pihak yang mendukung proyek ini.

**Made with ❤️ for better public service in Indonesia**