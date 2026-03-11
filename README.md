# LexIndoLLM Repository

**Large Language Model Khusus Regulasi Daerah Indonesia**  
*Studi Kasus: Pemerintah Kabupaten Kutai Kartanegara*

Repository resmi proyek **tesis S2 Teknik Informatika** Universitas Amikom Yogyakarta  
**NIM: 22.55.2293** – Novianto Rahmadi

**Paper terkait**:  
- LexIndoLLM: Large Language Model untuk Konsultasi Regulasi Daerah di Indonesia

## ✨ Fitur Utama
- Model ringan **Llama 3.2-1B** (1 miliar parameter)
- Fine-tuning bertahap + RAG (FAISS)
- Latency rata-rata **< 3.4 detik** di MacBook M1 Pro
- Faithfulness **0.77** (RAGAS)
- 100% offline & bisa dijalankan di laptop biasa

## 📁 Struktur Repository
```bash
lexindo/
├── LICENSE
├── README.md
├── requirements.txt
├── CITATION.cff
├── .gitignore
├── docs/                          # tesis full + JOISM + Turnitin
│
├── 01_raw_data/
│   ├── 00-list-pebup-perda.csv
│   ├── 2020/ ... 2026/
│   └── README.md
│
├── 02_dataset_preparation/
│   ├── 2020/ ... 2025/
│   └── README.md
│
├── 03_base_model/
│   ├── evaluation.ipynb
│   └── README.md
│
├── 04_finetune/
│   ├── adapters_lexindo/
│   ├── base_model/
│   ├── models/
│   │   ├── lexindo_lora/
│   │   ├── lexindo_e2/
│   │   └── lexindo_e3/
│   ├── 01_check_jsonl.py
│   ├── 02_convert_to_chat_format.py
│   ├── 03_train.py
│   ├── config.yaml
│   ├── lexindo-modelfile
│   └── README.md
│
├── 05_rag_corpus/
│   ├── faiss_index_lexindo/
│   ├── build.py
│   └── README.md
│
├── 06_evaluation_set/
│   ├── outputs/
│   │   ├── eval_result_base.jsonl
│   │   ├── eval_result_finetuned_no_rag.jsonl
│   │   └── eval_result_finetuned_rag.jsonl
│   ├── 01_beautify_jsonl.py
│   ├── 02_minify.py
│   ├── 03_generate_answer_base_model.py
│   ├── 04_generate_answer_finetuned_no_rag.py
│   ├── 05_generate_answer_finetuned_rag.py
│   └── README.md
│
├── 07_experiments/
│   └── logs/
│
├── 08_streamlit/
│   ├── app.py                     # ← script yang kamu kasih
│   ├── chat_history.json
│   └── README.md
│
└── 09_human_evaluation/
    └── README.md
```

## 🚀 Quick Start
```bash
git clone https://github.com/novay/lexindo.git
cd lexindo
pip install -r requirements.txt
streamlit run 08_streamlit/app.py

## 📄 Citation
```bibtex
@article{rahmadi2026lexindollm,
  title={LexIndoLLM: Large Language Model untuk Konsultasi Regulasi Daerah di Indonesia},
  author={Rahmadi, Novianto and Setyanto, Arief},
  journal={...},
  year={2026}
}
```

**License**: MIT  
**Disclaimer**: Dataset regulasi hanya untuk keperluan akademik & riset.