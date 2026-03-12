# 📂 Raw Dataset (01_raw_data)

Direktori ini ("SEHARUSNYA") berisi **data mentah (*raw data*)** regulasi daerah Kabupaten Kutai Kartanegara yang menjadi fondasi utama pengembangan **LexIndoLLM**. 

Data diperoleh langsung dari **Bagian Hukum Sekretariat Daerah Kabupaten Kutai Kartanegara** dan telah melalui proses kurasi yang ketat sesuai dengan kebutuhan penelitian tesis S2.

## 📊 Ringkasan Data

- **Sumber**: Bagian Hukum Sekda Kukar & JDIH Kabupaten Kutai Kartanegara
- **Periode Asli**: 2001–2026
- **Periode yang Digunakan**: **2020–2025** (Total 393 regulasi final untuk tesis)
- **Jenis Regulasi**: Peraturan Daerah (Perda) dan Peraturan Bupati (Perbup)
- **Total Entri Metadata**: 393+ dokumen

## 📁 Struktur Folder

Direktori ini secara eksklusif hanya memuat dua berkas:

1. **`00-list-perbup-perda.csv`** → Merupakan dataset metadata lengkap dari semua regulasi yang telah dikurasi.
2. **`README.md`** → Dokumen yang sedang Anda baca ini.

## 🗃️ Proses Kurasi Dokumen

Untuk memastikan kualitas dan relevansi dataset yang dihasilkan, data di dalam daftar CSV ini telah melalui tahapan penyaringan sebagai berikut:

1. **Pengecualian Dokumen (*Filtering*)** Kurasi ini membatasi ruang lingkup dengan **tidak** memasukkan:
   - Dokumen Kerjasama & Kajian Hukum
   - Surat Edaran
   - Draf/rancangan aturan (Rancangan Perbup dan Rancangan Perda)
   - Hierarki peraturan tertentu (Peraturan Desa, Peraturan Menteri, Peraturan Pemerintah, dan Peraturan Presiden)

2. **Kriteria Data Utama** Pemilihan dokumen diprioritaskan pada regulasi yang **status hukumnya masih aktif (berlaku)** serta memiliki relevansi atau nilai akademik yang tinggi untuk kebutuhan pemrosesan bahasa (NLP).

3. **Pengarsipan Historis (*Archiving*)** Meskipun tidak menjadi dataset prioritas utama, dokumen regulasi yang telah **dicabut atau diperbarui** tetap dipertahankan di dalam metadata. Hal ini bertujuan untuk memfasilitasi kebutuhan perbandingan dan analisis historis (kesejarahan hukum).

## 📋 Struktur Kolom Data (`00-list-perbup-perda.csv`)

| Kolom       | Keterangan                                      |
|-------------|-------------------------------------------------|
| `id`        | ID unik internal                                |
| `nomor`     | Nomor regulasi                                  |
| `tahun`     | Tahun penerbitan                                |
| `judul`     | Judul lengkap regulasi                          |
| `kategori`  | Peraturan Daerah / Peraturan Bupati             |
| `status`    | Berlaku / Perubahan / Dicabut / dll.            |
| `keterangan`| Catatan tambahan (informasi pencabutan/perubahan)|

## ⚠️ Catatan Penting

1. **Tidak Ada File PDF** - File PDF asli **tidak diunggah** ke dalam repositori GitHub ini karena ukuran file yang terlalu besar serta untuk menghormati kebijakan hak cipta dan distribusi internal pemerintah daerah.  
   - Semua PDF asli dapat diunduh secara legal dan publik melalui situs resmi: **[JDIH Kutai Kartanegara](https://jdih.kukarkab.go.id)**.

2. **Penggunaan Alur Kerja (*Pipeline*)** - File PDF di direktori ini akan digunakan pada tahap selanjutnya (`02_dataset_preparation`) untuk ekstraksi teks, proses OCR, dan pembuatan format instruksi *ShareGPT*.

## 🔗 Referensi Tesis

Bagian ini langsung mengacu pada dokumen tesis lengkap yang tersimpan di folder induk [`docs/`](https://github.com/novay/lexindo/tree/main/docs):

- **Tabel 2** – Atribut dokumen regulasi daerah (halaman 20 tesis)
- **Tabel 3** – Sebaran regulasi daerah tahun 2020–2025 (halaman 21 tesis)