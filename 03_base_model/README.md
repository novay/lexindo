# Pra Seleksi Base Model

Folder ini berisi **tahap pra-seleksi base model** sebelum melakukan fine-tuning domain.

Tujuannya adalah memilih model LLM open-source berukuran kecil (≤3B parameter) yang paling optimal untuk deployment **lokal** di perangkat terbatas (MacBook M1 8GB RAM) sesuai dengan eksperimen tesis.

## 🎯 Tujuan Evaluasi

- Membandingkan performa inferensi (kecepatan & efisiensi)
- Mengukur metrik kunci:  
  **TTFT** (Time To First Token)  
  **Latency** (Total Latency)  
  **Throughput** (Tokens per Second)  
  **Perplexity** (kualitas bahasa)

Semua pengujian dilakukan dengan Unsloth + 4-bit quantization pada perangkat yang sama.

## 📊 Hasil Pra-Seleksi Base Model

Berikut hasil lengkap dari `evaluation.ipynb` (diurutkan berdasarkan throughput terbaik):

| Model                    | Params   | TTFT (s) | Total Latency (s) | Throughput (TPS) | Perplexity |
|--------------------------|----------|----------|-------------------|------------------|------------|
| **Llama-3.2-1B-Instruct** | 1B      | **0.0650** | 6.9158           | **41.35**       | 1.4051    |
| Llama-3.2-3B-Instruct    | 3B      | 3.9978  | 10.0218          | 26.54           | **1.1627** |
| Nusantara-1.8B           | 1.8B    | 0.0939  | 12.8387          | 29.83           | 1.5457    |
| Qwen3-1.7B               | 1.7B    | 0.1105  | 23.5289          | 21.76           | 1.2872    |
| Qwen3-0.6B               | 0.6B    | 0.1112  | 10.9340          | 21.40           | 1.4925    |
| Phi-3.5-mini             | 3.8B    | 3.3025  | 20.6504          | 24.79           | 1.2631    |
| Gemma-3-1B-it            | 1B      | 0.1810  | 58.8699          | 8.70            | 2.1759    |

> **Catatan**: Semua pengujian menggunakan prompt yang sama, max_new_tokens=512, dan 4-bit quantization.

## 🏆 Kesimpulan & Alasan Pemilihan

**Base model terpilih: `unsloth/Llama-3.2-1B-Instruct`**

Alasan utama:
- **Throughput tertinggi** di kelas 1B (41.35 TPS)
- **TTFT tercepat** (0.065 detik)
- **Latency rendah** (6.92 detik untuk 286 token)
- Perplexity kompetitif (1.4051)
- Paling ringan & stabil di perangkat lokal Mac M1 Pro

Model ini kemudian digunakan sebagai fondasi LexIndoLLM di tahap fine-tuning (folder `04_finetune`).

## 📁 File Pendukung

- `evaluation.ipynb` → Notebook lengkap pra-seleksi (sudah dijalankan)
- Hasil lengkap dapat dilihat langsung di output cell notebook

## 🔗 Referensi Tesis

- **Tabel 6** – Hasil pra-seleksi base model (tesis)
- **Bagian 4.1** – Pra-seleksi Base Model (tesis)
- File tesis lengkap: [`../docs/3-tesis.pdf`](../docs/3-tesis.pdf)