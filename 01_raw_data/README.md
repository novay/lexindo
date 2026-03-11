# Raw Dataset

Folder ini berisi **data mentah (raw data)** regulasi daerah Kabupaten Kutai Kartanegara yang menjadi fondasi utama pengembangan **LexIndoLLM**.

Data ini diperoleh langsung dari **Bagian Hukum Sekretariat Daerah Kabupaten Kutai Kartanegara** dan telah dikurasi ketat sesuai kebutuhan tesis S2.

## 📊 Ringkasan Data

- **Sumber**: Bagian Hukum Sekda Kukar + JDIH Kabupaten Kutai Kartanegara  
- **Periode**: 2001–2026 (PDF asli lengkap)  
- **Periode yang digunakan di tesis**: **2020–2025** (393 regulasi final)  
- **Jenis regulasi**: Peraturan Daerah (Perda) dan Peraturan Bupati (Perbup)  
- **Total entri metadata**: 393+ (lihat CSV)

## 📁 Isi Folder

- **`00-list-pebup-perda.csv`** → Metadata lengkap semua regulasi (id, nomor, tahun, judul, kategori, status, keterangan)
- **`2020/` sampai `2026/`** → Folder tahun untuk menyimpan file PDF asli (placeholder)
- **`README.md`** → Dokumen ini

## 📋 Kolom di 00-list-pebup-perda.csv

| Kolom       | Keterangan                                      |
|-------------|-------------------------------------------------|
| id          | ID unik internal                                |
| nomor       | Nomor regulasi                                  |
| tahun       | Tahun penerbitan                                |
| judul       | Judul lengkap regulasi                          |
| kategori    | Peraturan Daerah / Peraturan Bupati             |
| status      | Berlaku / Perubahan / Dicabut / dll.            |
| keterangan  | Catatan tambahan (mencabut/mengubah regulasi)   |

## ⚠️ Catatan Penting

1. **PDF asli TIDAK di-upload ke GitHub**  
   - Ukuran file terlalu besar  
   - Menghormati hak cipta & kebijakan internal pemerintah daerah  
   - Semua PDF dapat diunduh secara legal dari situs resmi:  
     **https://jdih.kukarkab.go.id**

2. **Proses Kurasi**  
   - Hanya regulasi yang masih aktif atau memiliki nilai akademik tinggi yang dipertahankan  
   - Dokumen yang dicabut/diperbarui tetap disimpan untuk analisis historis

3. **Penggunaan**  
   - File ini digunakan di tahap `02_dataset_preparation` untuk ekstraksi teks, OCR, dan pembuatan dataset ShareGPT.

## 🔗 Referensi Tesis
Bagian ini langsung mengacu pada dokumen tesis lengkap yang tersimpan di folder [`docs/`](https://github.com/novay/lexindo/tree/main/docs):

- **Tabel 2** – Atribut dokumen regulasi daerah (halaman 20 tesis)
- **Tabel 3** – Sebaran regulasi daerah tahun 2020–2025 (halaman 21 tesis)
- **Bagian 3.2.1** – Akuisisi Data (halaman 19–22 tesis)

---