# 🏛️ LexIndoLLM: Finetuning Section

Folder ini berisi dokumentasi dan aset untuk **proses fine-tuning domain-spesifik secara bertahap**. Proyek ini bertujuan untuk menghasilkan **LexIndoLLM**, sebuah model bahasa besar berbasis **Llama 3.2-1B-Instruct** yang dioptimalkan untuk ranah hukum Indonesia.

Fine-tuning dilakukan menggunakan dua pendekatan utama:
* **Unsloth:** Digunakan untuk proses *training* skala besar yang efisien dan cepat di lingkungan Google Colab (GPU T4).
* **Framework MLX:** Digunakan untuk eksperimen lokal dan *fine-tuning* native pada arsitektur Apple Silicon (MacBook M1 Pro 16GB RAM).

## 🎯 Tujuan Fine-tuning
Melatih model agar mencapai kompetensi berikut:
- **Linguistic Precision:** Memahami gaya bahasa hukum formal Indonesia yang seringkali kompleks.
- **Domain Knowledge:** Menguasai struktur hukum dan terminologi regulasi daerah **Kutai Kartanegara**.
- **Helpfulness & Grounding:** Memberikan jawaban yang ramah (AI Assistant) namun tetap *grounded* (berbasis data) pada sumber regulasi asli untuk meminimalisir halusinasi.

Fine-tuning dilakukan secara **bertahap** (3 tahap) untuk hasil maksimal dengan komputasi terbatas.

## 📁 Struktur Folder

```bash
04_finetune/
├── mlx/              # Implementasi LoRA/QLoRA dengan MLX untuk Apple Silicon.
├── unsloth/          # Script training efisien dengan Unsloth (Xformers & Triton).
└── README.md         # Dokumentasi strategi finetuning.
```

## 🔧 Strategi 3 Tahap Fine-tuning (Metodologi Tesis)

Untuk mendapatkan hasil maksimal dengan sumber daya komputasi terbatas, proses *training* dibagi menjadi tiga fase berurutan (*Sequential Fine-tuning*):

### 1. Tahap 1 – Language & Glossary Adaptation

**Fokus:** Membangun fondasi terminologi.

* **Dataset:** Kamus hukum komprehensif yang dikurasi dari Database Glosarium BPK dan istilah kunci dari Black’s Law Dictionary (versi bahasa Indonesia).
* **Output:** Model mulai mengenali istilah teknis hukum (misal: *Kodifikasi*, *Wanprestasi*, *Asas Legalitas*).

### 2. Tahap 2 – Instruction Tuning

**Fokus:** Memperbaiki cara berkomunikasi dan pemahaman instruksi umum.

* **Dataset:** Sampel pilihan (10%) dari dataset instruksi bahasa Indonesia *open-source* (**FreedomIntelligence/alpaca-gpt4-indonesian**).
* **Output:** Model mampu mengikuti perintah pengguna dalam format percakapan natural tanpa kehilangan konteks hukumnya.

### 3. Tahap 3 – Regulation-specific Tuning

**Fokus:** Spesialisasi materi lokal.

* **Dataset:** Dataset regulasi daerah Kabupaten Kutai Kartanegara yang diproses dari dokumen PDF asli (Folder `02_dataset`).
* **Output:** Model akhir (**LexIndoLLM**) yang mampu menjawab pertanyaan spesifik mengenai peraturan perundang-undangan di Kutai Kartanegara.