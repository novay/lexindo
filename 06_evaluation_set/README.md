# Evaluation Set Preparation

Folder ini berisi **evaluation set** dan seluruh script/notebook untuk menghasilkan jawaban model serta menjalankan evaluasi otomatis (RAGAS).

Digunakan untuk membandingkan tiga kondisi:
- Base model
- Fine-tuned model (tanpa RAG)
- Fine-tuned model + RAG

## 📁 Struktur Folder

```bash
06_evaluation_set/
├── 01_beautify_jsonl.py
├── 02_minify_jsonl.py
├── 03_generate_base.ipynb
├── generate_answer_base.ipynb
├── generate_answer_finetuned.ipynb
├── generate_answer_finetuned_rag.ipynb
├── hasil_eval_rag_v2_final.csv
├── hasil_lexindo_rag_*.jsonl
├── ragas_eval_*.jsonl
├── ragas_eval_result_*.jsonl
└── README.md
```

## 🚀 Fungsi Utama

- Generate jawaban model secara batch
- Beautify & minify JSONL
- Hitung metrik RAGAS (Faithfulness, Answer Correctness, Context Precision, dll.)
- Simpan hasil evaluasi dalam CSV dan JSONL

## 🔗 Referensi Tesis

Bagian 4.2 – Evaluasi Otomatis (halaman 60–65 tesis)
Tabel 7 & Tabel 8 – Hasil metrik RAGAS

File referensi lengkap: `../docs/3-tesis.pdf`