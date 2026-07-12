# Evaluasi Ulang Retrieval RAGAS

Direktori ini berisi script dan hasil evaluasi ulang retrieval yang digunakan untuk menindaklanjuti nilai `context_recall` pada LexIndoLLM yang masih rendah dan perlu peningkatan.

Evaluasi dilakukan dengan membandingkan beberapa konfigurasi retrieval, yaitu:

- vector similarity dengan variasi nilai top-k;
- Maximal Marginal Relevance (MMR);
- hybrid retrieval yang menggabungkan vector similarity dan BM25 keyword search.

Fokus evaluasi pada direktori ini adalah dua metrik RAGAS:

- `context_recall`
- `context_precision`

## Struktur Direktori

```text
ragas/
├── summary/
│   ├── summary_hybrid_vec8_kw8_k10.csv
│   ├── summary_hybrid_vec8_kw10_k12.csv
│   ├── summary_mmr_k10_fetch40_lambda0.5.csv
│   ├── summary_similarity_k5.csv
│   ├── summary_similarity_k8.csv
│   ├── summary_similarity_k10.csv
│   └── summary_similarity_k12.csv
├── evaluasi_ulang.py
└── README.md
````

## Tujuan Evaluasi

Evaluasi ulang ini bertujuan untuk mengetahui apakah perubahan strategi retrieval dapat meningkatkan kelengkapan konteks yang diberikan kepada model.

Pada evaluasi awal, nilai `context_recall` masih menunjukkan bahwa sistem belum selalu mengambil seluruh konteks yang diperlukan untuk menjawab pertanyaan regulasi. Oleh karena itu, dilakukan evaluasi ulang terhadap beberapa konfigurasi retrieval untuk mencari konfigurasi yang lebih baik.

## Dataset Evaluasi

Evaluasi dilakukan menggunakan dataset pertanyaan evaluasi yang sama dengan evaluasi RAGAS sebelumnya. Dataset berisi pertanyaan, jawaban model, konteks hasil retrieval, dan jawaban referensi.

## Konfigurasi yang Dievaluasi

| File Summary                            | Strategi Retrieval   | Keterangan                                          |
| --------------------------------------- | -------------------- | --------------------------------------------------- |
| `summary_similarity_k5.csv`             | Vector similarity    | Baseline retrieval dengan top-k = 5                 |
| `summary_similarity_k8.csv`             | Vector similarity    | Retrieval dengan top-k = 8                          |
| `summary_similarity_k10.csv`            | Vector similarity    | Retrieval dengan top-k = 10                         |
| `summary_similarity_k12.csv`            | Vector similarity    | Retrieval dengan top-k = 12                         |
| `summary_mmr_k10_fetch40_lambda0.5.csv` | MMR                  | Retrieval dengan k = 10, fetch-k = 40, lambda = 0,5 |
| `summary_hybrid_vec8_kw8_k10.csv`       | Hybrid vector + BM25 | Vector top-8, BM25 keyword top-8, final-k = 10      |
| `summary_hybrid_vec8_kw10_k12.csv`      | Hybrid vector + BM25 | Vector top-8, BM25 keyword top-10, final-k = 12     |

## Ringkasan Hasil Evaluasi

| Konfigurasi Retrieval       | Context Recall | Context Precision |
| --------------------------- | -------------: | ----------------: |
| `similarity_k5`             |         0,4359 |            0,7787 |
| `similarity_k8`             |         0,5286 |            0,7258 |
| `similarity_k10`            |         0,5248 |            0,6987 |
| `similarity_k12`            |         0,5257 |            0,6815 |
| `mmr_k10_fetch40_lambda0.5` |         0,4366 |            0,6385 |
| `hybrid_vec8_kw8_k10`       |         0,5971 |            0,6921 |
| `hybrid_vec8_kw10_k12`      |         0,6162 |            0,6756 |

## Hasil Terbaik

Konfigurasi terbaik diperoleh pada:

```text
hybrid_vec8_kw10_k12
```

Dengan konfigurasi:

```text
Vector similarity top-8
BM25 keyword top-10
Final context top-12
```

Konfigurasi ini menghasilkan:

```text
context_recall    = 0,6162
context_precision = 0,6756
```

Hasil tersebut menunjukkan bahwa `context_recall` berhasil ditingkatkan hingga melewati target minimal 0,60.

## Interpretasi Hasil

Peningkatan nilai top-k pada vector similarity dari 5 menjadi 8 mampu meningkatkan `context_recall` dari 0,4359 menjadi 0,5286. Namun, peningkatan lebih lanjut ke top-k 10 dan top-k 12 tidak memberikan peningkatan yang signifikan.

Strategi MMR pada konfigurasi yang diuji belum mampu meningkatkan `context_recall` dibandingkan baseline vector similarity.

Hasil terbaik diperoleh melalui hybrid retrieval yang menggabungkan vector similarity dan BM25. Pendekatan ini lebih efektif karena dokumen regulasi sering memuat istilah hukum, nomor pasal, ayat, dan frasa normatif yang bersifat spesifik. BM25 membantu menangkap kecocokan literal, sedangkan vector similarity membantu menangkap kemiripan semantik.