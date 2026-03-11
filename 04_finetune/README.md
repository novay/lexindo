# Finetuning

Folder ini berisi **proses fine-tuning domain bertahap** untuk menghasilkan model **LexIndoLLM** berbasis **Llama 3.2-1B-Instruct**.

Fine-tuning dilakukan menggunakan **framework MLX** (native Apple Silicon) agar optimal di MacBook M1 8GB RAM.

## 🎯 Tujuan Fine-tuning

Melatih model agar:
- Memahami bahasa hukum formal Indonesia
- Menguasai struktur dan terminologi regulasi daerah Kutai Kartanegara
- Memberikan jawaban yang ramah, mudah dipahami, dan selalu grounded ke sumber asli

Fine-tuning dilakukan secara **bertahap** (3 tahap) untuk hasil maksimal dengan komputasi terbatas.

## 📁 Struktur Folder

```bash
04_finetune/
├── adapters_lexindo/              # Folder adapter LoRA sementara selama training
├── base_model/                    # Copy base model (mlx format)
├── models/
│   ├── lexindo_lora/              # Adapter LoRA final
│   ├── lexindo_e2/                # Model setelah 2 epoch (lexindo_2e)
│   └── lexindo_e3/                # Model setelah 3 epoch (lexindo_3e – terbaik)
├── 01_check_jsonl.py              # Validasi dataset JSONL
├── 02_convert_to_chat_format.py   # Preprocessing ke format ShareGPT
├── 03_train.py                    # Script utama training (LoRA/QLoRA)
├── config.yaml                    # Konfigurasi training
├── lexindo-modelfile              # Template Ollama
└── README.md
```

### Penjelasan Singkat
| Script                        | Fungsi Utama                                                                 | Kapan Dijalankan                  |
|-------------------------------|------------------------------------------------------------------------------|-----------------------------------|
| `01_check_jsonl.py`           | Validasi dataset JSONL (cek error format, panjang konteks, duplikasi, dll.) | Sebelum training (wajib)          |
| `02_convert_to_chat_format.py`| Mengubah dataset mentah menjadi format ShareGPT yang kompatibel MLX         | Setelah validasi, sebelum train   |
| `03_train.py`                 | Proses fine-tuning bertahap (LoRA + QLoRA) dengan konfigurasi config.yaml   | Utama (dijalankan 2x untuk e2 & e3) |

## ⚙️ Config.yaml (Sudah Disesuaikan Epoch)

```yaml
model: mlx-community/Llama-3.2-1B-Instruct-4bit
train: true
data: ./data
iters: 2000
batch_size: 4
num_layers: 16
rank: 16
adapter_path: ./adapters_lexindo
save_every: 500
learning_rate: 1e-5
grad_checkpoint: true
seed: 42
```

**Cara menghasilkan lexindo_e2 & lexindo_e3:**
Jalankan `03_train.py` dua kali dengan parameter epoch:
```bash
python 03_train.py --epochs 2 --output_dir models/lexindo_e2
python 03_train.py --epochs 3 --output_dir models/lexindo_e3
```

## 🚀 Cara Menjalankan (Step by Step)

1. **Pastikan data sudah siap**  
   Folder `./data` berisi file JSONL format ShareGPT dari `02_dataset_preparation`.

2. **Training**
   ```bash
   python 03_train.py --epochs 2 --output_dir models/lexindo_e2
   python 03_train.py --epochs 3 --output_dir models/lexindo_e3
   ```

3. **Convert ke Ollama & Test**
   ```bash
   ollama create lexindo-custom -f lexindo-modelfile
   ollama run lexindo-custom
   ```

   Atau langsung pakai versi quantized:
   ```bash
   ollama run hf.co/nxvay/lexindo_2e:q4_k_m
   ```

## Unsloth vs MLX
- **Pra-seleksi** (folder 03_base_model) menggunakan **Unsloth** → karena sangat cepat untuk benchmarking banyak model di Colab/GPU.
- **Fine-tuning** menggunakan **MLX** (`mlx-community/Llama-3.2-1B-Instruct-4bit`) → karena framework ini **native Apple Silicon**, jauh lebih hemat RAM dan cepat di MacBook M1 Pro.

Base model yang digunakan **sama persis** (Llama-3.2-1B-Instruct). Hanya framework yang berbeda. Hasil akhir tetap kompatibel.

## 🔗 Referensi Tesis

- **Bagian 3.3** – Fine-tuning Phase (halaman 22–25 tesis)
- **Tabel 4 & Tabel 5** – Konfigurasi lingkungan & LoRA/QLoRA
- **Tabel 6** – Perbandingan base model (pra-seleksi)

**File referensi lengkap:** [`../docs/3-tesis.pdf`](../docs/3-tesis.pdf)

---


