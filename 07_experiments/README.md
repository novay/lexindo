# Evaluation (Final)

Folder ini digunakan untuk menyimpan **semua hasil eksperimen**, logging, dan analisis tambahan selama pengembangan LexIndoLLM.

## 📁 Struktur Folder

```bash
07_experiments/
├── scripts/                  # Script pendukung eksperimen
├── evaluasi.ipynb
├── merge_evaluation_set.ipynb
├── eval_*.jsonl              # (base, ft_no_rag, ft_with_rag)
├── ragas_eval_merged.jsonl
├── ollama.log
└── README.md
```

## 📋 Isi Utama

- Log training & inference Ollama
- Hasil evaluasi per model
- Notebook untuk merging dan analisis
- Ablation study (epoch 2 vs epoch 3, RAG vs non-RAG)

Folder ini bersifat internal untuk tracking dan debugging.

## 🔗 Referensi Tesis

- Bagian 4.1 – Analisis Eksperimen (halaman 55–59 tesis)
- Bagian 4.3 – Dampak RAG terhadap performa

File referensi lengkap: `../docs/3-tesis.pdf`