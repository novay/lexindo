## Tahap 3 - Regulation-specific Tuning (Peraturan Daerah)

Setelah model paham istilah khusus (Tahap 1) dan luwes mengikuti instruksi bahasa Indonesia (Tahap 2), tibalah **saya** di fase pemungkas. 

Di tahap ini, **saya** menyuntikkan pengetahuan spesifik mengenai peraturan daerah ke dalam "otak" model. **Saya** menggunakan dataset `nxvay/lexindo-kukarkab-alpaca` dari Hugging Face yang akan di-*fine-tune* di atas model hasil Tahap 2 (`lexindo-llm-instruct`).

### 1. Download & Format Dataset

Sama seperti fase sebelumnya, **saya** memulai dengan menjalankan script `prepare.py` (di folder `tahap_03`) untuk mengunduh dataset regulasi ini dari Hugging Face dan mengubahnya ke format JSONL yang siap dilahap oleh MLX.

```bash
python prepare.py

```

### 2. Training Regulation-specific Tuning

Sekarang **saya** mulai proses pelatihannya. Yang membedakan di sini adalah fondasi model yang **saya** gunakan: `--model` sekarang mengarah ke `lexindo-llm-instruct` (hasil akhir Tahap 2). **Saya** melatih model ini agar benar-benar menguasai konteks dan pasal-pasal peraturan daerah, tanpa menghilangkan kepandaian bahasa yang sudah dipelajari sebelumnya.

```bash
mlx_lm.lora \
  --model /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_02/models/lexindo-llm-instruct \
  --train \
  --data /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_03/data \
  --batch-size 4 \
  --num-layers 12 \
  --learning-rate 1e-5 \
  --iters 1000 \
  --save-every 200 \
  --test \
  --adapter-path /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_03/models/kukarkab-adapter \
  -c /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_01/lora_config.yaml

```

### 3. Uji Coba Model (Inference)

Proses *training* regulasi selesai! Mari **saya** tes pemahaman hukumnya. **Saya** mencoba memberikan pertanyaan yang sangat spesifik mengenai peraturan di Kutai Kartanegara. Di sini, **saya** menurunkan sedikit `--temp` ke 0.2 agar jawaban model lebih kaku, faktual, dan presisi sesuai dokumen hukum, bukan mengarang bebas.

```bash
mlx_lm.generate \
  --model /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_02/models/lexindo-llm-instruct \
  --adapter-path /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_03/models/kukarkab-adapter \
  --prompt "Berdasarkan Peraturan Daerah Kutai Kartanegara, apa saja wewenang dari Badan Permusyawaratan Desa?" \
  --max-tokens 250 \
  --temp 0.2

```

### 4. Merge Adapter (Model Rilis Final)

Langkah pamungkas! Karena jawabannya sudah sangat memuaskan, **saya** menggabungkan model Tahap 2 tadi dengan *adapter* regulasi dari Tahap 3. Hasil akhirnya adalah `lexindo-llm-kukar`—model *ultimate* yang paham istilah, pintar berbahasa Indonesia, dan ahli dalam regulasi daerah. Model inilah yang sepenuhnya siap untuk dirilis!

```bash
mlx_lm.fuse \
  --model /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_02/models/lexindo-llm-instruct \
  --adapter-path /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_03/models/kukarkab-adapter \
  --save-path /Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo/04_finetune/tahap_03/models/lexindo-llm-kukar

```