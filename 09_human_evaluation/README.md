# Human Evaluation Preparation

Folder ini berisi **proses human evaluation** oleh 5 pakar hukum daerah untuk menilai kualitas jawaban LexIndoLLM. Evaluasi ini menjadi bukti kualitatif bahwa model tidak hanya unggul secara metrik otomatis (RAGAS), tetapi juga **diterima dan dipercaya** oleh ahli hukum.

Proses dilakukan dengan metode **cherry picking** terhadap regulasi terkini, kemudian pertanyaan diujikan melalui aplikasi Streamlit. Hasilnya dicatat dalam Dokumen Survey menggunakan skala Likert (1–5).

## 📁 Struktur Folder

```bash
09_human_evaluation/
├── README.md                    # Dokumen metodologi dan daftar pertanyaan ini
├── survey_form.pdf              # Formulir survey Likert untuk 5 pakar
├── results/                     # Hasil penilaian pakar + analisis
```

## 🎯 Metodologi Human Evaluation

1. **Cherry Picking**  
   Dipilih 20 pertanyaan dari regulasi aktual 2023–2025 (Perda & Perbup) yang paling relevan dengan kebutuhan masyarakat.

2. **Jumlah Pakar**  
   5 orang pakar hukum daerah (dari Bagian Hukum Sekda, Akademisi, dan Praktisi Hukum).

3. **Skala Penilaian**  
   Skala Likert 1–5 untuk 4 aspek utama.

**Catatan Penting (Proses Survey Saat Ini):**  
Daftar pertanyaan di bawah ini masih dalam tahap pengumpulan data survey. Nomor urut, isi pertanyaan, atau kategori kemungkinan akan bergeser, diubah formulasi, ditambah, atau dikurangi berdasarkan masukan dari para pakar hukum selama proses survey berlangsung. Versi final akan dicatat setelah semua pakar memberikan feedback dan validasi selesai.

## 📋 20 Pertanyaan Final (Cherry-Picked)

### Kategori 1: UMKM, Retribusi dan Pajak Daerah (4 pertanyaan)
1. Saya punya warung makan kecil di pasar Tenggarong, omset Rp 50 juta/bulan. Berapa persen pajak yang harus dibayar dan pasal mana yang mengatur tarif lengkap beserta cara penghitungannya?
2. Apakah saya wajib menyediakan tempat khusus untuk produk lokal di etalase? Sanksi apa yang berlaku?
3. Berapa tarif Pajak Reklame untuk spanduk kecil di toko kelontong dan apakah ada keringanan untuk usaha mikro?
4. Apakah ada insentif/subsidi untuk produk UMKM lokal (madu, kerajinan) dan wajib label berbahasa Indonesia?

### Kategori 2: Tata Ruang dan Perizinan (4 pertanyaan)
5. Tanah warisan 1.000 m² di Loa Duri mau dibangun rumah + warung. Masuk kawasan apa menurut RTRW dan boleh dibangun apa saja?
6. Untuk buka toko material di Muara Badak, apakah wajib KKPR/PKKPR dulu? Apa bedanya?
7. Lahan sawah dekat sungai di Marang Kayu termasuk kawasan lindung gambut/mangrove? Apa yang dilarang dan sanksinya?
8. Mau buka homestay di tepi Mahakam. Ketentuan RTRW untuk pariwisata di kawasan tersebut?

### Kategori 3: Keuangan Daerah dan APBD (4 pertanyaan)
9. Total APBD 2025 berapa triliun? Pendapatan dari mana saja dan berapa defisitnya?
10. Desa 2.500 jiwa, angka kemiskinan sedang. Berapa ADD yang diterima dan hitungannya pakai asas merata/keadilan?
11. Dana desa boleh dipakai untuk apa saja dan berapa persen maksimal untuk honorarium?
12. Belanja modal dan transfer ke desa tahun 2025 berapa besarnya dan prioritasnya ke mana?

### Kategori 4: Ketertiban Umum dan Ketentraman Masyarakat (4 pertanyaan)
13. Masih boleh kasih kantong plastik gratis di toko modern? Strategi pengganti dan lokasi yang dilarang?
14. Sanksi kalau masih kasih kantong plastik di pasar tradisional?
15. Program BERSINAR di desa: kegiatan pencegahan narkoba apa yang wajib dan siapa yang bentuk tim terpadu?
16. Tes urine sebagai syarat masuk sekolah negeri? Program antisipasi dini di sekolah?

### Kategori 5: Pendidikan (PPDB & Beasiswa Kukar Idaman) (4 pertanyaan)
17. Anak usia 6 tahun 8 bulan mau masuk SD. Boleh? Jalur mana yang paling mudah dan dokumen apa saja?
18. Keluarga prasejahtera, anak mau masuk SMP. Jalur afirmasi pakai KIP/surat tidak mampu?
19. Anak yatim piatu mau dapat Beasiswa Kukar Idaman + jalur afirmasi SMP. Jenis beasiswa apa dan syaratnya?
20. Guru honorer mau kuliah S1 sambil anak daftar SMP lewat jalur prestasi. Cara hitung nilai prestasi dan kuota?

## 🔗 Referensi Tesis

- **Bagian 4.4** – Hasil Human Evaluation oleh Pakar Hukum (halaman 66–68 tesis)
- **Tabel hasil Likert** dan analisis kesimpulan akan dimasukkan di Bab 4.4
- **Lampiran** – Formulir Survey dan hasil mentah

**File referensi lengkap:** [`../docs/3-tesis.pdf`](../docs/3-tesis.pdf)

---

