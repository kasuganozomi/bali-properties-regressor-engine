# Bali Smart Pricing Engine

**Sistem Prediksi Tarif Sewa Villa dan Homestay Berbasis Algoritma CatBoost dan XGBoost Regressor**

Proposal Tugas Besar — Pembelajaran Mesin  
I Kadek Adi Sunetra · 2305551053  
Anthony Wisnu Jati · 2305551138  
Program Studi Teknologi Informasi, Universitas Udayana

> [!NOTE]
> **Arsip Historis Proposal Awal:** Naskah presentasi ini berasal dari tahap awal penyusunan proposal (`29` kolom rancangan awal, sebelum pelatihan model akhir selesai, dan `12` rujukan awal). Data bersih final (`978` unit, `38` prediktor, `54` kecamatan), hasil benchmark model final, dan `23` rujukan terverifikasi tersedia pada [README.md](../../README.md), [bedah model dan metrik](../panduan/bedah-model-dan-metrik.md), dan [laporan validasi dataset](../../aplikasi/data/processed/DATASET_VALIDATION_REPORT.md).

Presentasi terdiri dari 12 slide utama termasuk sampul, untuk 7–10 menit, serta satu slide rujukan cadangan. Tujuh bagian mengikuti urutan masalah, tujuan, gambaran dan skenario, data, metode, mekanisme sistem, serta kesimpulan. Rujukan dan gap dibahas dalam bagian metode. Speaker notes mengikuti naskah ini.

## 1. Latar Belakang Masalah

*Slide 2*

Pemilik villa dan homestay perlu menentukan tarif sebelum menawarkan propertinya kepada tamu. Harga penginapan di sekitar dapat menjadi pembanding, tetapi tidak selalu sesuai. Dua properti di kawasan yang sama dapat memiliki kapasitas, fasilitas, dan reputasi yang berbeda. Pemilik masih harus menilai perbedaan tersebut agar memperoleh acuan tarif yang relevan.

Penelitian ini mengusulkan estimasi tarif berdasarkan karakteristik properti. Dataset Airbnb Bali sudah menyediakan harga dan URL listing, tetapi belum memuat kapasitas serta fasilitas secara rinci. URL tersebut digunakan untuk memperoleh atribut tambahan dari properti yang sama, sebagai dasar pembelajaran model dan penjelasan prediksi.

## 2. Tujuan

*Slide 3*

Penelitian ini bertujuan untuk:

1. Membantu pemilik villa dan homestay di Bali memperoleh acuan tarif yang sesuai dengan karakteristik propertinya.
2. Merancang pengayaan melalui URL listing untuk melengkapi atribut properti dan menghubungkannya dengan data awal.
3. Membandingkan model regresi dan menguji kontribusi atribut hasil pengayaan terhadap estimasi tarif.

## 3. Gambaran Umum dan Skenario Contoh

### Gambaran Umum Penelitian

*Slide 4*

Bali Smart Pricing Engine dirancang untuk membantu pemilik villa dan homestay memperkirakan tarif per malam. Model akan mempelajari hubungan harga listing dengan lokasi, kapasitas, fasilitas, serta reputasi yang tersedia. Data pembanding berasal dari dataset Airbnb Bali yang diperkaya melalui URL listing.

Pemilik memasukkan karakteristik propertinya melalui dashboard. Sistem direncanakan menampilkan estimasi, penjelasan kontribusi fitur, dan gambaran harga dalam dataset. Perubahan fasilitas dapat dicoba untuk membandingkan dua prediksi sebagai bahan pertimbangan tarif.

**Karakteristik properti → Model prediksi → Estimasi tarif dan penjelasan**

### Skenario Contoh

*Slide 5*

Bayangkan seorang pemilik memiliki villa baru di Canggu, Badung, dengan dua kamar tidur dan kolam renang pribadi. Villa sudah siap menerima tamu, tetapi pemilik belum tahu tarif yang sebaiknya ditawarkan. Ia melihat harga villa di sekitar. Namun, kapasitas, fasilitas, dan jumlah ulasannya berbeda, sehingga harga tersebut sulit dijadikan acuan langsung.

| Karakteristik | Kondisi properti contoh |
|---|---|
| Lokasi | Canggu, Badung |
| Kapasitas | 4 tamu |
| Kamar tidur | 2 |
| Kamar mandi | 2 |
| Fasilitas | Kolam renang pribadi, dapur, AC, Wi-Fi, dan parkir |
| Reputasi | Listing baru; nol ulasan; rating belum tersedia |

Pemilik memasukkan kondisi villa, termasuk reputasi yang belum tersedia. Sistem direncanakan memberikan estimasi dan penjelasan fitur untuk membantu pertimbangan tarif. Rating belum tersedia tidak diisi sebagai rating tamu buatan.

Skenario dan gambar merupakan ilustrasi; belum ada nilai prediksi. Data awal Badung hanya 49 baris dan ketelitian untuk kawasan Canggu masih perlu diperiksa.

## 4. Bentuk Data

*Slide 6*

Sumber: Indonesia Airbnb Dataset: Bali, Luthfi Abdillah (pandaa12), Kaggle [1]. Data awal dan master sama-sama memiliki 1.235 baris. Pengayaan menambah struktur dari enam menjadi 29 kolom; jumlah kolom tersebut mencakup target serta referensi, bukan seluruhnya informasi masukan model.

| Data awal: 6 kolom | Isi |
|---|---|
| nama, link | Nama dan URL listing |
| harga | Target harga |
| rating, jumlah_review | Reputasi dasar |
| wilayah | Kabupaten/kota |

| Master: 29 kolom | Kelompok tambahan |
|---|---|
| Lokasi dan jenis | Lokasi mikro, koordinat, jenis properti |
| Kapasitas | Tamu, kamar tidur, tempat tidur, kamar mandi |
| Fasilitas | Kolam renang, dapur, AC, Wi-Fi, parkir, dan lainnya |
| Reputasi | Status listing baru dan badge yang tersedia |

Tabel gabungan memuat 1.058 nomor listing unik dan 177 baris tambahan dengan nomor berulang. Tersedia 1.036 berkas metadata JSON. Sebanyak 1.212 baris cocok dengan metadata tersebut, sedangkan 23 baris belum mempunyai pasangan. Nomor listing yang cocok belum memastikan semua rinciannya benar. Master mencampur beberapa jenis akomodasi; jenis akomodasi yang dipakai dalam model ditetapkan setelah labelnya diperiksa.

## 5. Tahapan Metode dan Rancangan Model

### Rujukan dan Alasan Pemilihan

*Slide 7*

Dua pembanding utama adalah Digno dan Tang. Keduanya meneliti harga sewa akomodasi yang ditawarkan melalui Airbnb. Digno menjadi rujukan nasional; Tang langsung membahas CatBoost. Airbnb adalah platform tempat akomodasi ditawarkan, bukan objek yang harganya diprediksi.

| Rujukan | Isi penelitian | Alasan dipilih |
|---|---|---|
| Digno dkk. [3] · JELIKU, 2023 | Inside Airbnb New York: 50.220 listing, 96 kolom, ditambah sentimen ulasan. Menguji prediksi harga, termasuk XGBoost. | Sama-sama memprediksi harga sewa akomodasi. Kita memakai data Bali dan menambahkan CatBoost dalam perbandingan model. |
| Tang dkk. [5] · 2024 | Harga sewa akomodasi melalui Airbnb di Sydney. Membandingkan sepuluh algoritma dengan 34 masukan; CatBoost terbaik pada datanya. | Dasar penggunaan CatBoost. Kita menguji kembali pilihan model pada sampel Bali, tanpa menganggap hasil Sydney otomatis berlaku. |

Dataset Bali yang sama sudah dipakai Brian Risk [2] dengan RF dari wilayah, rating, dan jumlah ulasan. Pada versi yang diperiksa, kamar serta fasilitas belum diambil melalui URL.

Digno tidak memakai dataset Kaggle Bali kita. JELIKU tercatat SINTA 5 pada profil yang diperiksa; masa akreditasi saat terbit belum seluruhnya dicocokkan dengan SK. Ringkasan Tang mengikuti abstrak penerbit; seluruh langkahnya belum diperiksa dari teks penuh. Syawaludin [4] dan Zhang [6] tetap menjadi rujukan pendukung, bukan dua pembanding utama.

### Gap Analysis dan Arah Penelitian

*Slide 8*

Digno menguji data New York; Tang menguji Sydney. Hasil mereka belum menjawab model terbaik dan kontribusi rincian properti pada sampel Bali kita. Penelitian mengikuti pendekatan prediksi dari informasi akomodasi, dengan perbedaan berikut.

| Penelitian sebelumnya | Yang ditambahkan atau diubah |
|---|---|
| Digno [3]: listing dan sentimen ulasan New York; menguji XGBoost serta model lain. | Menggunakan data Bali dan menambahkan CatBoost ke perbandingan RF–XGBoost. Rincian fisik diperoleh dari URL; sentimen tidak diadopsi. |
| Tang [5]: sepuluh model pada data Sydney; CatBoost terbaik pada datanya. | Menguji kembali RF, XGBoost, dan CatBoost pada Bali, serta membandingkan data awal dan hasil pengayaan pada properti uji yang sama. |

Fokus pengujian: apakah CatBoost terbaik pada sampel Bali, dan bagaimana tambahan informasi kamar, kapasitas, serta fasilitas mengubah kesalahan prediksi tarif?

Kita mengembangkan data melalui URL dan menguji model pada konteks Bali. Pengayaan URL tidak diklaim sebagai teknik baru. Notebook Brian [2] menjadi pembanding dataset yang sama. Model belum dilatih, sehingga belum ada klaim hasil lebih baik atau penemuan algoritma baru.



### Tahapan Pengayaan Data

*Slide 9*

**Data awal → Buka tautan → Catat rincian properti → Simpan JSON → Tambahkan ke data awal**

Tautan villa pada satu baris dibuka untuk membaca jumlah kamar, kapasitas tamu, dan fasilitasnya. Hasil disimpan dalam JSON, lalu ditambahkan pada baris villa yang sama. Nomor listing digunakan agar informasi tidak tertukar dengan properti lain.

Tersedia 1.036 berkas JSON dan tabel gabungan berisi 1.235 baris dengan 29 kolom. Informasi yang belum terbaca harus dibedakan dari fasilitas yang tidak tersedia. Harga awal tetap menjadi target prediksi.

Audit menemukan 168 nomor listing berlabel New pada data awal yang mempunyai rating numerik di master. Nilai itu perlu diperiksa sebelum dipakai. Kode scraper belum disertakan untuk diperiksa; data tidak diubah saat penyuntingan dokumen.

### Model dan Cara Pengujian

*Slide 10*

Model akan dibandingkan menggunakan data awal dan data yang sudah dilengkapi. Properti untuk pengujian dibuat sama, sehingga perubahan kesalahan dapat dibandingkan. Satu properti tidak boleh muncul sekaligus dalam data latihan dan pengujian.

| Model | Peran |
|---|---|
| Random Forest | Model pembanding awal |
| XGBoost | Memperbaiki prediksi melalui rangkaian pohon keputusan |
| CatBoost | Mengolah kategori seperti wilayah dan jenis properti |

| Evaluasi | Yang dinilai |
|---|---|
| MAE | Rata-rata besar kesalahan tarif, dalam Rupiah |
| RMSE | Memberi bobot lebih besar pada kesalahan yang besar |
| R² | Kemampuan model menjelaskan variasi harga |
| SHAP | Masukan yang berkontribusi terhadap prediksi |

Setiap model dibandingkan pada dua jenis data: informasi awal dan informasi yang telah dilengkapi. Properti uji dibuat sama agar hasil kedua percobaan dapat dibandingkan.

Pengaturan model dipilih menggunakan data latihan. Properti tanpa ulasan diuji tersendiri jika jumlah datanya memadai. SHAP menjelaskan prediksi model dan tidak membuktikan bahwa penambahan fasilitas menyebabkan kenaikan tarif. Belum ada hasil pelatihan yang dilaporkan.

## 6. Mekanisme Kerja Sistem Saat Jadi

*Slide 11*

Dashboard Streamlit direncanakan agar pemilik dapat menggunakan model setelah ketepatan dan batas penggunaannya dinilai. Melanjutkan skenario sebelumnya, pemilik ingin mengetahui:

> Berapa estimasi tarif villa dua kamar di Canggu dengan kolam renang pribadi dan belum memiliki ulasan?

Pemilik mengisi lokasi, kapasitas, fasilitas, dan reputasi aktual. Sistem menyiapkan masukan untuk model terpilih, kemudian menampilkan estimasi tarif, penjelasan fitur, dan gambaran harga listing dalam dataset.

Pemilik dapat mencoba perubahan fasilitas, misalnya ruang kerja, lalu membandingkan estimasi sebelum dan sesudahnya. Hasil menjadi bahan pertimbangan bersama kondisi usaha; sistem tidak memprediksi okupansi ataupun menjamin keuntungan renovasi.

## 7. Kesimpulan

*Slide 12*

Penelitian berangkat dari kebutuhan pemilik memperoleh acuan tarif dan keterbatasan atribut dataset Airbnb Bali. Dataset yang sama sudah pernah digunakan untuk prediksi. Pengembangan yang diusulkan berfokus pada pengayaan melalui URL listing serta pengujian manfaat informasi tambahan.

Data awal, cache, dan master telah tersedia. Langkah berikutnya adalah audit mutu data, perbandingan fitur dan model, serta pengembangan dashboard setelah evaluasi. Proposal tetap sampai Bab III; belum ada model terlatih atau klaim peningkatan kinerja.

## Rujukan Utama — Slide Cadangan

*Slide 13*

| Nomor | Rujukan |
|---|---|
| [1] | Abdillah · Indonesia Airbnb Dataset: Bali · Kaggle |
| [2] | Brian Risk · Indonesia Bali Airbnb Analysis Price Prediction · Kaggle 2026 |
| [3] | Digno dkk. · Prediksi Harga Properti Airbnb dengan Analisis Sentimen · JELIKU 2023 |
| [4] | Syawaludin dan Sunu · Perbandingan Model Ensemble untuk Harga Sewa Indekos · JITET 2025 |
| [5] | Tang dkk. · Forecasting Airbnb prices through machine learning · 2024 |
| [6] | Zhang dkk. · XAI-driven machine learning for homestay pricing · 2026 |

[1] Dataset: https://www.kaggle.com/datasets/pandaa12/indonesia-airbnb-dataset-bali-listings

[2] Notebook: https://www.kaggle.com/code/devraai/indonesia-bali-airbnb-analysis-price-prediction

[3] DOI: https://doi.org/10.24843/JLK.2023.v12.i01.p22

[4] DOI: https://doi.org/10.23960/jitet.v13i3S1.7737

[5] DOI: https://doi.org/10.1002/mde.3985

[6] DOI: https://doi.org/10.1108/JHTI-07-2025-0908

[7] Pengayaan lokasi — Akalın dan Alptekin, FedCSIS 2024: https://doi.org/10.15439/2024F7603

Daftar pustaka proposal berisi 12 sumber: enam artikel jurnal, empat paper prosiding, dataset, dan notebook. Rujukan [3] dan [5] menjadi pembanding utama. Rujukan [4] dan [6] mendukung pengumpulan data serta penjelasan prediksi. Notebook [2] menjadi pembanding dataset yang sama. Paper asli algoritma serta teori tercantum lengkap dalam proposal; sumber yang tidak dipakai telah dikeluarkan.
