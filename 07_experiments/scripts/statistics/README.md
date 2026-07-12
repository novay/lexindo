# Uji Statistik Answer Correctness

Direktori ini berisi script dan dokumentasi uji statistik yang digunakan untuk memperkuat evaluasi kinerja LexIndoLLM. Fokus pengujian pada direktori ini adalah membandingkan skor `answer_correctness` antara dua konfigurasi:

- LexIndoLLM tanpa RAG
- LexIndoLLM dengan RAG

Pengujian dilakukan untuk mengetahui apakah peningkatan `answer_correctness` setelah integrasi Retrieval-Augmented Generation (RAG) tidak hanya terlihat dari perbedaan rata-rata, tetapi juga signifikan secara statistik.

## Struktur Direktori

```text
statistics/
├── README.md
└── test.py
````

## Tujuan Pengujian

Uji statistik ini bertujuan untuk:

* membandingkan performa LexIndoLLM tanpa RAG dan dengan RAG pada metrik `answer_correctness`;
* mengetahui apakah peningkatan skor setelah integrasi RAG signifikan secara statistik;
* melengkapi evaluasi deskriptif dengan pengujian inferensial;

## Data yang Digunakan

Pengujian dilakukan menggunakan data evaluasi yang memuat pasangan skor `answer_correctness` untuk pertanyaan yang sama. Setiap pasangan data terdiri dari:

* pertanyaan evaluasi;
* jawaban LexIndoLLM tanpa RAG;
* jawaban LexIndoLLM dengan RAG;
* jawaban referensi;
* skor `answer_correctness` tanpa RAG;
* skor `answer_correctness` dengan RAG.

## Alur Pengujian

Secara umum, proses pengujian dilakukan melalui tahapan berikut:

1. Membaca data hasil evaluasi LexIndoLLM tanpa RAG.
2. Membaca data hasil evaluasi LexIndoLLM dengan RAG.
3. Memasangkan skor `answer_correctness` berdasarkan pertanyaan yang sama.
4. Menghitung rata-rata skor tanpa RAG dan dengan RAG.
5. Menghitung selisih skor antara konfigurasi dengan RAG dan tanpa RAG.
6. Melakukan uji normalitas Shapiro-Wilk terhadap selisih skor.
7. Menentukan uji statistik utama:
   * `paired sample t-test` jika selisih skor berdistribusi normal;
   * `Wilcoxon signed-rank test` jika selisih skor tidak berdistribusi normal.
8. Menghitung effect size menggunakan Cohen's dz.
9. Menyimpan hasil uji statistik.

## Metode Statistik

### Shapiro-Wilk Test

Uji Shapiro-Wilk digunakan untuk mengevaluasi apakah selisih skor `answer_correctness` antara konfigurasi tanpa RAG dan dengan RAG memenuhi asumsi normalitas.

Jika p-value Shapiro-Wilk lebih besar dari 0,05, maka data selisih skor dianggap tidak menunjukkan pelanggaran asumsi normalitas.

### Paired Sample t-test

Paired sample t-test digunakan untuk menguji apakah terdapat perbedaan rata-rata yang signifikan antara dua konfigurasi yang diuji pada pasangan data yang sama.

Dalam penelitian ini, paired sample t-test digunakan apabila selisih skor `answer_correctness` memenuhi asumsi normalitas.

### Wilcoxon Signed-Rank Test

Wilcoxon signed-rank test digunakan sebagai uji non-parametrik untuk data berpasangan apabila asumsi normalitas tidak terpenuhi.

Dalam pengujian ini, Wilcoxon tetap dihitung sebagai pembanding, meskipun uji utama yang digunakan adalah paired sample t-test.

### Cohen's dz

Cohen's dz digunakan sebagai ukuran efek untuk data berpasangan. Ukuran efek ini menunjukkan seberapa besar peningkatan performa secara praktis, bukan hanya apakah peningkatan tersebut signifikan secara statistik.

## Ringkasan Hasil

Hasil uji statistik yang diperoleh adalah sebagai berikut:

| Komponen                     |                    Nilai |
| ---------------------------- | -----------------------: |
| Jumlah data evaluasi         |           100 pertanyaan |
| Jumlah pasangan skor valid   |              96 pasangan |
| Mean tanpa RAG               |                   0,3738 |
| Mean dengan RAG              |                   0,6603 |
| Selisih rata-rata            |                   0,2865 |
| Shapiro-Wilk p-value         |                   0,0724 |
| Paired sample t-test p-value |          4,42724 × 10⁻¹⁴ |
| Wilcoxon signed-rank p-value |          4,83624 × 10⁻¹² |
| Cohen's dz                   |                   0,9047 |
| Interpretasi                 | Signifikan pada α = 0,05 |

## Interpretasi Hasil

Hasil uji normalitas Shapiro-Wilk menunjukkan p-value sebesar 0,0724. Karena nilai tersebut lebih besar dari 0,05, selisih skor `answer_correctness` tidak menunjukkan pelanggaran asumsi normalitas. Oleh karena itu, paired sample t-test digunakan sebagai uji utama.

Hasil paired sample t-test menunjukkan p-value sebesar 4,42724 × 10⁻¹⁴. Nilai tersebut lebih kecil dari 0,05, sehingga peningkatan `answer_correctness` setelah integrasi RAG dinyatakan signifikan secara statistik.

Nilai Cohen's dz sebesar 0,9047 menunjukkan ukuran efek yang besar. Dengan demikian, peningkatan performa LexIndoLLM dengan RAG tidak hanya terlihat dari kenaikan rata-rata, tetapi juga didukung oleh signifikansi statistik dan ukuran efek yang kuat.