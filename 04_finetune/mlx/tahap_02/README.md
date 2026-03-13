## Tahap 2 - Instruction Tuning (Bahasa Indonesia)

Setelah model mengerti istilah-istilah khusus (*domain adaptation*) di tahap sebelumnya, sekarang **saya** melatihnya agar lebih pintar menangkap instruksi dan menjawab dengan luwes dalam bahasa Indonesia. Untuk tahap ini, **saya** menggunakan dataset `alpaca-gpt4-indonesian` dari Hugging Face yang akan di-*fine-tune* menumpuk di atas model hasil Tahap 1 (`lexindo-llm-final`). Mari kita mulai prosesnya!

### 1. Download & Format Dataset

Pertama-tama, **saya** menyiapkan datanya. **Saya** menjalankan script `prepare.py` untuk mengunduh dataset secara otomatis dari Hugging Face dan mengubahnya ke format JSONL agar siap dibaca oleh MLX.

```bash
python prepare.py

```

> **Catatan Penting:** Di sini **saya** sengaja hanya mengambil sebagian data (sampling). Tujuannya murni untuk memoles pemahaman instruksi bahasa Indonesia model, sekaligus mencegah fenomena *catastrophic forgetting*—yaitu kondisi di mana model malah "amnesia" atau melupakan pengetahuan istilah-istilah khusus dari Tahap 1 karena ditimpa oleh terlalu banyak data instruksi umum.

### 2. Training Instruction Tuning

Setelah data siap, **saya** langsung memulai proses *training*-nya. Fondasi yang **saya** gunakan kali ini adalah model final dari Tahap 1 (`--model`). Mengingat kapasitas RAM **saya** yang terbatas di 8GB, parameter LoRA sudah disesuaikan agar prosesnya tetap berjalan lancar dan aman, meski iterasinya sedikit **saya** perbanyak menjadi 1000 iterasi.

```bash
mlx_lm.lora \
  --model ./../tahap_01/models/lexindo-llm-final \
  --train \
  --data ./data \
  --batch-size 4 \
  --num-layers 12 \
  --learning-rate 1e-5 \
  --iters 1000 \
  --save-every 200 \
  --test \
  --adapter-path ./models/alpaca-adapter \
  -c ./../tahap_01/lora_config.yaml

```

### 3. Uji Coba Model (Inference)

Proses *training* selesai! Sekarang saatnya **saya** mengetes kepintaran model ini. **Saya** mencoba memberikan perintah umum (*prompt*) dalam bahasa Indonesia untuk melihat apakah gaya bahasanya sudah sesuai harapan.

*(Catatan: Nilai `--temp` sengaja **saya** naikkan sedikit menjadi 0.4 agar jawaban model terasa lebih luwes, kreatif, dan natural).*

```bash
mlx_lm.generate \
  --model ./../tahap_01/models/lexindo-llm-final \
  --adapter-path ./models/alpaca-adapter \
  --prompt "Tolong buatkan draf email singkat untuk meminta persetujuan anggaran ABT kepada atasan." \
  --max-tokens 200 \
  --temp 0.4

```

### 4. Merge Adapter

Hasil tesnya memuaskan! Model sekarang sukses memadukan pengetahuan aslinya (istilah khusus Tahap 1) dengan kepandaian berbahasa instruksional (Tahap 2). Sebagai langkah penutup, **saya** menggabungkan (*fuse*) model dasar dan adapternya menjadi satu model utuh berlabel `instruct`.

Model final inilah yang nantinya siap **saya** gunakan untuk **fase selanjutnya** *(Regulation-specific tuning)*!

```bash
mlx_lm.fuse \
  --model ./../tahap_01/models/lexindo-llm-final \
  --adapter-path ./models/alpaca-adapter \
  --save-path ./models/lexindo-llm-instruct

```