## Tahap 1 - Language & glossary adaptation

1. Konversi CSV → Format Pretraining

Mulai dengan persiapan data. Script `prepare.py` akan mengubah data CSV mentah menjadi format JSONL yang siap pakai. Script ini juga otomatis menyusun data ke bentuk percakapan (tanya-jawab) dan membaginya jadi data *train*, *valid*, dan *test*.
```bash
python prepare.py

```

2. Install MLX

Pasang *library* `mlx-lm` dari Apple. 
Ini adalah kunci supaya *fine-tuning* bisa dilakukan langsung di Mac (berbasis Apple Silicon).

```bash
pip install mlx-lm

```

3. Convert Model Llama 3.2-1B-Instruct ke Format MLX (4-bit)

Unduh model **Llama 3.2-1B-Instruct** dan mengubah formatnya biar cocok dengan MLX. Tambahan `-q` di sini berfungsi untuk mengecilkan ukuran model (kuantisasi 4-bit) supaya lebih hemat RAM.

```bash
mlx_lm.convert --hf-path meta-llama/Llama-3.2-1B-Instruct --mlx-path ./models/llama-3.2-1b-instruct-mlx -q

```

4. Training Continued Pretraining (Dioptimalkan untuk 8GB RAM)

Latih model! **Saya** memakai metode LoRA dengan setelan yang pas untuk Mac dengan RAM 8GB. Model akan belajar selama 800 iterasi dan otomatis menyimpan progres (*checkpoint*) setiap 200 iterasi supaya aman.

```bash
mlx_lm.lora \
  --model ./models/llama-3.2-1b-instruct-mlx \
  --train \
  --batch-size 4 \
  --num-layers 12 \
  --learning-rate 8e-6 \
  --iters 800 \
  --save-every 200 \
  --test \
  --adapter-path ./models/lexindo-llm-pretrain \
  -c ./lora_config.yaml

```

5. Inference
Tesing hasilnya! Perintah ini menjalankan model asli bersamaan dengan *adapter* yang baru saja dilatih untuk menjawab pertanyaan. **Saya** mengatur `--temp 0.1` biar modelnya menjawab dengan akurat, sesuai fakta, dan nggak gampang ngawur atau halusinasi.

```bash
mlx_lm.generate \
  --model ./models/llama-3.2-1b-instruct-mlx \
  --adapter-path ./models/lexindo-llm-pretrain \
  --prompt "Apa definisi dari istilah: ABT?" \
  --max-tokens 100 \
  --temp 0.1

```

6. Merge Adapter

Kalau sudah oke, dilakukan penggabungan (*fuse*) model asli dengan *adapter*-nya. Hasil akhirnya adalah satu model utuh (`lexindo-llm-final`) yang sudah mengerti istilah-istilah khusus **saya** dan siap dipakai atau di-*deploy*!

```bash
mlx_lm.fuse \
  --model ./models/llama-3.2-1b-instruct-mlx \
  --adapter-path ./models/lexindo-llm-pretrain \
  --save-path ./models/lexindo-llm-final
```

