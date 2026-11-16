# BEDAH TOTAL MODEL MACHINE LEARNING & METRIK REGRESI
### Panduan Penguasaan Konsep dari Nol untuk Memahami Model dan Metrik Evaluasi Tarif Properti Bali

> **Tujuan Dokumen**: Membedah seluruh metrik evaluasi regresi dan cara kerja model machine learning yang digunakan pada proyek *Bali Smart Pricing Engine* sampai ke akarnya. Ditulis secara mendalam namun menggunakan analogi yang mudah dipahami oleh orang awam dalam waktu kurang dari satu jam belajar.

---

## DAFTAR ISI

1. [Peta Besar Masalah: Regresi vs Klasifikasi](#1-peta-besar-masalah-regresi-vs-klasifikasi)
2. [Eksplorasi Lengkap: Ada Berapa Metrik Evaluasi di Dunia ML Regresi?](#2-eksplorasi-lengkap-ada-berapa-metrik-evaluasi-di-dunia-ml-regresi)
   - [2.1 MAE (Mean Absolute Error)](#21-mae-mean-absolute-error--rata-rata-melesetnya-tebakan-per-properti)
   - [2.2 MSE (Mean Squared Error)](#22-mse-mean-squared-error--hukuman-kuadrat-bagi-kesalahan-besar)
   - [2.3 RMSE (Root Mean Squared Error)](#23-rmse-root-mean-squared-error--akar-penarik-satuan-asli)
   - [2.4 MedAE (Median Absolute Error)](#24-medae-median-absolute-error--nilai-tengah-kesalahan-penyelamat-dari-jebakan-villa-sultan)
   - [2.5 R² (Koefisien Determinasi — Skala Logaritmik)](#25-r-koefisien-determinasi--berapa-persen-perbedaan-harga-yang-bisa-dibuktikan-oleh-atribut-kita)
   - [2.6 Adjusted R²](#26-adjusted-r--penangkal-fitur-sampah)
   - [2.7 MAPE (Mean Absolute Percentage Error)](#27-mape-mean-absolute-percentage-error--persentase-rata-rata)
   - [2.8 MdAPE (Median Absolute Percentage Error)](#28-mdape-median-absolute-percentage-error--persentase-kesalahan-relatif-standar-akurasi-pasar)
   - [2.9 RMSLE (Root Mean Squared Logarithmic Error)](#29-rmsle-root-mean-squared-logarithmic-error--evaluasi-berbasis-rasio-skala)
3. [Hierarki 5 Metrik Evaluasi (MedAE, R², MdAPE, MAE, dan RMSE)](#3-hierarki-metrik-mana-metrik-yang-paling-kita-percaya-dan-apa-batas-batasnya)
4. [Evaluasi Bertingkat (Tier Analysis): Mengapa Evaluasi Global Belum Cukup?](#4-evaluasi-bertingkat-tier-analysis-mengapa-evaluasi-global-belum-cukup)
5. [Bedah 3 Model Machine Learning Kita Sampai ke Mekanisme Fisiknya](#5-bedah-3-model-machine-learning-kita-sampai-ke-mekanisme-fisiknya)
   - [5.1 Pohon Keputusan (Decision Tree) sebagai Batu Bata Dasar](#51-pohon-keputusan-decision-tree-sebagai-batu-bata-dasar)
   - [5.2 Model 1: Random Forest Regressor (Prinsip Musyawarah 300 Juri)](#52-model-1-random-forest-regressor-prinsip-musyawarah-300-juri)
   - [5.3 Model 2: XGBoost Regressor (Prinsip Evaluasi Tryout Berkelanjutan)](#53-model-2-xgboost-regressor-prinsip-evaluasi-tryout-berkelanjutan)
   - [5.4 Model 3: CatBoost Regressor (Sang Juara Data Kategori & Wilayah Bali)](#54-model-3-catboost-regressor-sang-juara-data-kategori--wilayah-bali)
   - [5.5 Mengapa LightGBM dan Stacking Ridge Kita Singkirkan?](#55-mengapa-lightgbm-dan-stacking-ridge-kita-singkirkan)
6. [Tabel Komparasi Head-to-Head 3 Model di Data Uji Bali](#6-tabel-komparasi-head-to-head-3-model-di-data-uji-bali)
7. [Kamus Mental Tanya-Jawab Penguji (Cheat Sheet Pemahaman Konseptual)](#7-kamus-mental-tanya-jawab-penguji-cheat-sheet-pemahaman-konseptual)

---

## 1. PETA BESAR MASALAH: REGRESI VS KLASIFIKASI

Sebelum masuk ke rumus, kita harus mendudukkan masalah mendasarnya terlebih dahulu:

Dalam dunia Machine Learning terawasi (*Supervised Learning*), hanya ada dua tugas utama:
1. **Klasifikasi**: Menebak label kategori atau kelompok (*diskrit*).
   * Contoh: Menentukan apakah email ini *Spam* atau *Bukan Spam*; menentukan apakah foto ini *Kucing* atau *Anjing*.
   * Metriknya: Akurasi (%), Precision, Recall, F1-Score, ROC-AUC.
2. **Regresi**: Menebak besaran angka kontinu yang memiliki satuan riil (*kontinu*).
   * Contoh: Memperkirakan suhu udara besok (°C); memperkirakan umur beton (hari); memperkirakan **tarif sewa harian villa per malam (Rupiah)**.
   * Metriknya: Selisih jarak matematis antara angka tebakan model dengan angka sebenarnya.

Dalam proyek **Bali Smart Pricing Engine**, tugas kita adalah **Regresi**. Kita ingin menaksir angka harga sewa per malam (misal: Rp 1.450.000).  
Karena kita menebak angka Rupiah, metrik klasifikasi seperti *F1-score* atau *Confusion Matrix* sama sekali tidak bisa dipakai di sini. Kita wajib menggunakan **Metrik Evaluasi Regresi**.

---

## 2. EKSPLORASI LENGKAP: ADA BERAPA METRIK EVALUASI DI DUNIA ML REGRESI?

Di dunia statistik dan data science internasional, terdapat 9 metrik regresi utama. Masing-masing lahir karena sejarah kelemahan metrik sebelumnya:

```
[Keluarga Selisih Moneter Asli]       [Keluarga Proporsi Variansi]       [Keluarga Relatif Persentase]
       ├── MAE (Rata-rata)                     ├── R² (R-Squared)                    ├── MAPE (Rata-rata %)
       ├── MSE (Kuadrat)                       └── Adjusted R²                       └── MdAPE (Median %)
       ├── RMSE (Akar Kuadrat)
       └── MedAE (Median / Nilai Tengah)
```

Berikut adalah bedah lengkap masing-masing metrik, sejarah kelahirannya, kelemahan, dan kapan harus digunakan:

---

### 2.1 MAE (Mean Absolute Error) — Rata-rata Melesetnya Tebakan per Properti

#### A. Definisi Sederhana & Cara Hitungnya Langkah demi Langkah
MAE adalah **rata-rata selisih uang (Rupiah) antara harga asli dan harga tebakan model untuk setiap properti**.

Cara hitungnya sangat sederhana dan dilakukan per satu-satu properti:
1. **Langkah 1**: Ambil properti pertama. Cek harga aslinya berapa, lalu cek harga tebakan model berapa. Hitung selisihnya (selalu positif, abaikan tanda minus).
2. **Langkah 2**: Lakukan hal yang sama untuk properti ke-2, ke-3, sampai properti terakhir (di proyek kita, ada 196 data properti uji).
3. **Langkah 3**: Jumlahkan seluruh selisih rupiah dari 196 properti tersebut.
4. **Langkah 4**: Bagi total selisih itu dengan jumlah propertinya (dibagi 196).

**Contoh Nyata Perhitungan**:
Bayangkan kita menguji 4 listing villa:
* **Villa 1**: Harga Asli Rp 1.000.000, Tebakan Model Rp 1.200.000 $\rightarrow$ Meleset = $\text{Rp } 200.000$.
* **Villa 2**: Harga Asli Rp 600.000, Tebakan Model Rp 500.000 $\rightarrow$ Meleset = $\text{Rp } 100.000$.
* **Villa 3**: Harga Asli Rp 2.500.000, Tebakan Model Rp 2.000.000 $\rightarrow$ Meleset = $\text{Rp } 500.000$.
* **Villa 4**: Harga Asli Rp 8.000.000, Tebakan Model Rp 6.000.000 $\rightarrow$ Meleset = $\text{Rp } 2.000.000$.

Perhitungan MAE:
$$\text{Total Selisih} = 200.000 + 100.000 + 500.000 + 2.000.000 = \text{Rp } 2.800.000$$
$$\text{MAE} = \frac{\text{Rp } 2.800.000}{4\text{ villa}} = \mathbf{Rp\ 700.000}$$

#### B. Arti Angka MAE CatBoost di Proyek Kita (Rp 764.207)
Pada 196 data uji di Bali, total seluruh kesalahan tebakan CatBoost dijumlahkan menghasilkan sekitar Rp 149,8 juta (persisnya Rp 149.784.549).  
Ketika dibagi 196 properti, didapatlah angka **Rp 764.207**.

Artinya bagi orang awam:  
**"Setiap kali sistem kita menebak harga satu penginapan di Bali, rata-rata tebakannya meleset sekitar Rp 764 ribu dari harga aslinya."**

#### C. Kelemahan Fatal MAE (Mengapa Rata-rata Bisa Menipu)
Rata-rata itu buta terhadap nilai ekstrem (*outlier*).  
Pada contoh 4 villa di atas:
* Villa 1, 2, dan 3 tebakannya sangat bagus (hanya meleset Rp 100rb – Rp 500rb).
* Tetapi karena Villa 4 (villa mewah) meleset Rp 2 juta, angka rata-ratanya ikut melambung menjadi Rp 700.000!  
Ini membuat model terlihat jelek secara keseluruhan, padahal untuk penginapan biasa model bekerja sangat baik. Itulah mengapa kita membutuhkan metrik berikutnya: **MedAE**.

---

### 2.2 MSE (Mean Squared Error) — Hukuman Kuadrat bagi Kesalahan Besar

#### A. Definisi & Rumus
MSE mengkuadratkan setiap selisih sebelum dirata-ratakan:
$$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$

#### B. Sejarah & Masalah yang Diselesaikan
Diciptakan oleh Carl Friedrich Gauss dan Adrien-Marie Legendre dalam metode kuadrat terkecil (*Ordinary Least Squares*). Mereka membutuhkan fungsi matematis yang mulus (*differentiable*) agar turunan kalkulusnya mudah dihitung oleh komputer saat proses optimasi gradien. Selain itu, MSE sengaja dirancang untuk **menghukum kesalahan besar secara berlipat ganda**.  
Jika Anda meleset Rp 10.000, kuadratnya kecil. Namun jika Anda meleset Rp 5.000.000, kuadratnya menjadi raksasa ($25 \times 10^{12}$).

#### C. Kelemahan Fatal
Satuannya ikut terkuadratkan! Jika target kita Rupiah, satuan MSE adalah **$\text{Rupiah}^2$ (Rupiah Kuadrat)**. Angka ini tidak memiliki arti intuitif bagi manusia atau pemilik villa. Anda tidak bisa berkata ke dosen: *"Model kita salah sebesar 1,4 triliun Rupiah kuadrat."*

---

### 2.3 RMSE (Root Mean Squared Error) — Akar Penarik Satuan Asli

#### A. Definisi & Rumus
RMSE adalah akar kuadrat dari MSE:
$$\text{RMSE} = \sqrt{\text{MSE}} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$

#### B. Sejarah & Masalah yang Diselesaikan
RMSE lahir semata-mata untuk mengembalikan satuan $\text{Rupiah}^2$ dari MSE kembali ke satuan moneter aslinya (**Rupiah**), namun tetap mempertahankan sifat MSE yang memberi hukuman berat pada kesalahan besar.

#### C. Karakteristik Penting: Mengapa RMSE Selalu Lebih Besar dari MAE?
$$\text{RMSE} \ge \text{MAE}$$
Di model CatBoost kita:
* **MAE** = Rp 764.207
* **RMSE** = Rp 1.231.953  
Mengapa RMSE melambung jauh lebih tinggi dari MAE? Karena dalam 196 data uji kita, ada beberapa villa mewah seharga Rp 6 juta s.d Rp 10 juta yang selisihnya bisa mencapai Rp 3–6 juta. Selisih besar tersebut dikuadratkan oleh RMSE, sehingga menarik angka RMSE ke atas. Semakin besar jarak antara RMSE dan MAE, semakin banyak variasi kesalahan besar (*outlier error*) dalam data.

---

### 2.4 MedAE (Median Absolute Error) — Nilai Tengah Kesalahan (Penyelamat dari Jebakan Villa Sultan)

#### A. Definisi Sederhana & Cara Hitungnya di Proyek Kita
MedAE **TIDAK menggunakan rata-rata**. MedAE mencari **nilai tengah** dari seluruh selisih kesalahan tebakan.

Cara hitungnya di proyek kita:
1. **Langkah 1**: Dari 196 properti yang diuji oleh model CatBoost, kumpulkan 196 angka selisih kesalahan (angka meleset dalam Rupiah).
2. **Langkah 2**: Urutkan 196 angka meleset tersebut berbaris dari yang paling kecil (paling jitu) sampai yang paling besar (paling ngawur):
   * Nomor 1: Meleset hanya Rp 2.521 (tebakan hampir 100% tepat).
   * Nomor 2: Meleset Rp 3.553.
   * ...
   * **Nomor 98 & 99 (tepat di tengah-tengah dari 196 data)**: Melesetnya Rp 389.220 dan Rp 393.765 (rata-ratanya **Rp 391.492**).
   * ...
   * Nomor 195: Meleset Rp 5.530.567.
   * Nomor 196: Meleset Rp 6.381.298 (properti kelas atas dengan variasi fitur yang belum seluruhnya tertangkap tabel).
3. **Langkah 3**: Ambil nilai tengah dari antrean genap tersebut (rata-rata posisi ke-98 dan ke-99). Angka inilah yang disebut **MedAE = Rp 391.492**.

#### B. Maksud Konkretnya bagi Pemilik Properti dan Orang Awam
Apa arti angka **MedAE Rp 391.492** ini?
* **Artinya**: Dari 196 penginapan di Bali yang diuji, **ada 98 penginapan (persis separuh / 50% data) yang tebakan modelnya SANGAT DEKAT dengan harga asli, yaitu salah tebaknya di bawah Rp 391.492 per malam!**
* Hanya 98 properti sisanya yang salah tebaknya di atas Rp 391 ribu. Sebagian besar properti yang selisihnya jauh tersebut merupakan villa kelas menengah ke atas dan premium (Rp 2,5 juta hingga Rp 10 juta per malam) yang tarifnya sangat dipengaruhi faktor fisik yang tidak tercatat di listing teks standar.

#### C. Mengapa MedAE Jauh Lebih Jujur Dibanding MAE?
Bayangkan ada 10 properti:
* 9 homestay biasa: masing-masing salah tebak hanya **Rp 200.000**.
* 1 villa sultan miliarder: salah tebak **Rp 8.000.000**.

Jika dihitung pakai **MAE (Rata-rata)**:
$$\text{MAE} = \frac{(9 \times 200.000) + 8.000.000}{10} = \frac{1.800.000 + 8.000.000}{10} = \mathbf{Rp\ 980.000}$$
Jika dosen membaca angka rata-rata Rp 980 ribu, dosen akan mengira: *"Modelmu jelek sekali, rata-rata salah tebaknya hampir sejuta!"*  
Padahal pada 9 dari 10 properti (90% properti), model kita sangat pintar karena cuma meleset Rp 200 ribu. Satu villa sultan telah merusak seluruh rata-rata kelas.

Jika dihitung pakai **MedAE (Nilai Tengah)**:
Urutan selisih kesalahan: `[200rb, 200rb, 200rb, 200rb, 200rb, 200rb, 200rb, 200rb, 200rb, 8jt]`.  
Nilai tengahnya adalah: **Rp 200.000**.  
MedAE kebal terhadap nilai pencilan (*outlier*). MedAE membuktikan bahwa untuk mayoritas akomodasi biasa di Bali, sistem kita memberikan taksiran harga yang sangat wajar.

---

### 2.5 R² (Koefisien Determinasi) — Berapa Persen Perbedaan Harga yang Bisa Dibuktikan oleh Atribut Kita?

#### A. Sebutan Resmi & Arti Bahasa Awamnya
* **Nama Resmi Akademik**: **Koefisien Determinasi** (*Coefficient of Determination*).
* **Kata Kuncinya**: **"Kemampuan Menjelaskan"** (*Explanatory Power*) atau **"Persentase Pengaruh Atribut"**.
* **Pertanyaan Nyata yang Dijawab**:  
  *"Berapa persen naik-turunnya (keragaman) harga sewa villa di Bali yang berhasil dibuktikan dan diterangkan oleh 38 kolom atribut yang ada di tabel kita?"*

#### B. Logika Awam Mengapa Disebut "Kemampuan Menjelaskan"
Harga sewa properti di Bali itu **berbeda-beda (bervariasi)**: ada homestay Rp 250 ribu, villa standar Rp 1,5 juta, hingga villa mewah Rp 9 juta per malam.  
Pertanyaannya: **Mengapa harga mereka bisa berbeda-beda?**  
Karena fasilitas dan lokasinya berbeda! Sebagian besar perbedaan itu tercatat di tabel kita: beda jumlah kamar tidur, ada kolam renang pribadi atau tidak, dekat pantai Canggu atau di pedalaman, serta rating ulasannya.

Angka **$R^2 = 67,08\%$** pada model CatBoost kita artinya:  
> **"Sebanyak 67,08% alasan mengapa harga villa di Bali berbeda-beda (naik-turun) berhasil dijelaskan dan dibuktikan oleh 38 atribut di tabel data kita."**  
> Atau dalam bahasa sehari-hari: **Tingkat keberhasilan 38 atribut kita dalam menjelaskan variasi tarif sewa di Bali adalah sebesar 67,08%.**

Sisa **32,92%** perbedaan harga belum bisa dijelaskan karena faktor penentunya memang tidak memiliki kolom di file CSV kita (misalnya: tidak ada kolom luas tanah dalam meter persegi, tidak ada kolom arah pemandangan laut/sawah, dan tidak ada kolom musim liburan).

#### C. Cara Hitung Matematisnya Langkah demi Langkah (Pada Skala `log_price`)
Di kode proyek kita ([04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L72-L80)), nilai $R^2$ dihitung langsung pada skala logaritmik ($y_i^{(\log)} = \ln(1 + y_i)$) sebelum dikembalikan ke Rupiah:
$$R^2 = 1 - \frac{\sum_{i=1}^{n} \left(y_i^{(\log)} - \hat{y}_i^{(\log)}\right)^2}{\sum_{i=1}^{n} \left(y_i^{(\log)} - \bar{y}^{(\log)}\right)^2}$$

Cara memahaminya tetap sederhana dengan membandingkan dua tebakan (di ruang logaritma):
1. **Orang Pertama (Tebakan Asal Pakai Rata-rata):** Selalu menjawab setiap properti Bali dengan angka rata-rata logaritmik $\bar{y}^{(\log)}$ (sekitar $14{,}20$ atau setara median ~Rp 1,47 juta/malam). Total kuadrat kesalahannya kita sebut $SS_{\text{tot}}$.
2. **Orang Kedua (Model CatBoost Kita):** Membaca 38 fitur untuk memprediksi $\hat{y}_i^{(\log)}$ per unit. Total kuadrat kesalahannya disebut $SS_{\text{res}}$.
3. **Perhitungan $R^2$:** Menghitung berapa persen kesalahan kuadrat si Orang Pertama yang berhasil dipangkas oleh model kita.

#### D. Makna Angka R² CatBoost di Proyek Kita (67,08%)
* Jika **$R^2 = 0\%$**: Model kita sama sekali tidak berguna, kecerdasannya persis sama dengan orang yang hanya menebak rata-rata.
* Jika **$R^2 = 100\%$**: Model sempurna tanpa salah sama sekali.
* Pada model CatBoost kita, **$R^2 = 67,08\%$**:  
  **Artinya**: **Model kita berhasil memangkas 67,08% kesalahan kuadrat skala log dari tebakan rata-rata polos**, sekaligus menangkap **67,08% variasi pola tarif sewa di Bali** berdasarkan 38 fitur fisik, lokasi, dan fasilitas yang tersedia.

#### E. Mengapa Nilai R² Mentok di 67,08% dan Ke Mana Sisa 32,92%-nya?
Mengapa nilainya tidak bisa 100%? Apakah model kita kurang pintar?

Jawabannya ada pada **keterbatasan kolom atribut di tabel dataset CSV kita**:
* Di dalam file CSV dataset kita, kita memiliki **38 kolom atribut** (jumlah kamar, ada kolam renang, jarak pantai, rating, kecamatan, dll).
* Angka **$R^2 = 67,08\%$** membuktikan bahwa **67,08% perbedaan harga antar villa di Bali berhasil dijelaskan secara akurat oleh 38 kolom yang ada di tabel data kita**.
* Sisa **32,92%** variasi harga tidak bisa ditebak oleh model bukan karena algoritmanya rusak, melainkan karena hasil penarikan halaman listing Airbnb kita **tidak menyediakan kolom-kolom fisik berikut**:
  1. **Tidak ada kolom Luas Bangunan ($m^2$)**: Villa 2 kamar di tanah 500 $m^2$ harganya pasti jauh lebih mahal dibanding kamar 20 $m^2$, namun luas meter persegi ini tidak tercatat di dataset.
  2. **Tidak ada kolom Pemandangan (View)**: Apakah balkon menghadap langsung ke sunset laut, sawah Ubud, atau cuma tembok gang sempit.
  3. **Tidak ada kolom Musim Sewa (Seasonality)**: Dataset ini adalah potret satu rentang waktu pemesanan, tidak mencatat perubahan tarif antara malam tahun baru (*peak season*) dan hari kerja biasa (*low season*).
  4. **Tidak ada kolom Tahun Pembangunan / Renovasi**: Kebugaran interior baru vs bangunan tua tidak tercatat di tabel.

Jadi, jika dosen bertanya ke mana sisa sekitar 33%-nya:  
*"38 kolom yang ada di dataset kita sudah optimal menjelaskan 67,08% dinamika harga, Pak. Sisa 32,92% adalah faktor yang memang tidak tersedia kolom atributnya pada halaman listing Airbnb standar, seperti luas bangunan meter persegi, pemandangan laut/sawah, dan fluktuasi musim liburan."*

---

### 2.6 Adjusted R² — Penangkal Fitur Sampah

#### A. Definisi & Rumus
$$R^2_{\text{adj}} = 1 - \left[ \frac{(1 - R^2)(n - 1)}{n - k - 1} \right]$$
di mana $n$ adalah jumlah sampel data dan $k$ adalah jumlah fitur yang dimasukkan.

#### B. Masalah yang Diselesaikan
Dalam statistik biasa, $R^2$ memiliki sifat licik: setiap kali Anda menambahkan fitur baru ke model—bahkan jika fitur itu sama sekali tidak berguna (misalnya: *"warna baju pemilik villa"* atau *"angka zodiak host"*), nilai $R^2$ biasa **pasti akan naik atau minimal tetap**, tidak akan pernah turun.  
Adjusted $R^2$ memasang "denda" berupa penalti $k$ (jumlah fitur). Jika Anda menambahkan fitur baru tetapi fitur itu tidak memberikan kontribusi akurasi yang signifikan, nilai Adjusted $R^2$ justru akan **turun**.

---

### 2.7 MAPE (Mean Absolute Percentage Error) — Persentase Rata-rata

#### A. Definisi & Rumus
$$\text{MAPE} = \frac{100\%}{n} \sum_{i=1}^{n} \left| \frac{y_i - \hat{y}_i}{y_i} \right|$$

#### B. Masalah Fatal pada MAPE (Mengapa Proyek Kita Menolak MAPE Biasa)
Meskipun populer di kalangan bisnis, MAPE memiliki dua cacat matematis yang sangat berbahaya:
1. **Pembagian dengan Nol / Angka Kecil**: Jika ada penginapan murah seharga Rp 150.000, lalu model menebak Rp 450.000 (selisih Rp 300.000), nilai persentase errornya adalah:
   $$\left|\frac{150.000 - 450.000}{150.000}\right| = \frac{300.000}{150.000} = \mathbf{200\%!}$$
   Satu kamar murah saja bisa membuat nilai MAPE meledak menjadi ratusan persen.
2. **Hukuman Asimetris**: MAPE menghukum tebakan berlebih (*overforecast*) jauh lebih kejam dibanding tebakan kurang (*underforecast*).

---

### 2.8 MdAPE (Median Absolute Percentage Error) — Persentase Kesalahan Relatif (Standar Akurasi Pasar)

#### A. Apa Maksudnya "Proporsional / Relatif"?
Mengapa kita tidak boleh hanya melihat selisih uang Rupiah saja?
Mari bandingkan dua kasus ini:
* **Kasus A (Homestay Murah)**: Harga asli Rp 300.000 per malam. Model menebak Rp 600.000.  
  Selisihnya Rp 300.000. Meleset Rp 300 ribu di sini **sangat fatal (kesalahan 100%)**, karena harga tebakannya menjadi 2 kali lipat dari harga aslinya!
* **Kasus B (Villa Mewah)**: Harga asli Rp 10.000.000 per malam. Model menebak Rp 10.300.000.  
  Selisihnya sama-sama Rp 300.000. Namun di villa mewah, meleset Rp 300 ribu **hampir tidak terasa (kesalahan cuma 3%)**!

Kata **"proporsional" atau "relatif"** artinya: **besar kecilnya kesalahan harus diukur sebanding dengan harga asli barangnya**. Meleset Rp 300 ribu di kamar murah bernilai jauh lebih gawat dibanding meleset Rp 300 ribu di villa sultan.

#### B. Cara Hitung MdAPE Langkah demi Langkah di Proyek Kita
1. **Langkah 1**: Untuk setiap properti dari 196 data uji, hitung persentase melesetnya:
   $$\text{Persentase Meleset} = \frac{|\text{Harga Asli} - \text{Tebakan Model}|}{\text{Harga Asli}} \times 100\%$$
   * Misal Properti 1: Meleset Rp 100.000 dari harga Rp 1.000.000 $\rightarrow \frac{100.000}{1.000.000} \times 100\% = 10\%$.
   * Misal Properti 2: Meleset Rp 400.000 dari harga Rp 1.000.000 $\rightarrow \frac{400.000}{1.000.000} \times 100\% = 40\%$.
2. **Langkah 2**: Kumpulkan 196 angka persentase meleset tersebut dari seluruh data uji.
3. **Langkah 3**: Urutkan 196 persentase itu dari yang paling kecil ke yang paling besar.
4. **Langkah 4**: Ambil nilai tengah dari antrean genap (rata-rata posisi ke-98 dan ke-99). Angka tersebut adalah **MdAPE = 30,09%**.

#### C. Menghitung Akurasi Pasar yang Mudah Dipahami Orang Awam (69,91%)
Jika model kita memiliki nilai tengah meleset sebesar 30,09%, maka sisa persentase menuju 100% adalah **tingkat kebenarannya**:
$$\text{Tingkat Akurasi Pasar} = 100\% - 30,09\% = \mathbf{69,91\%}$$

Artinya bagi pemilik penginapan di Bali:  
**"Secara umum, tingkat ketepatan median tebakan harga model CatBoost kita adalah sebesar 69,91% terhadap harga wajar pasar."**  
Ini bahasa yang paling mudah dicerna oleh siapa pun tanpa latar belakang matematika.

---

### 2.9 RMSLE (Root Mean Squared Logarithmic Error) — Evaluasi Berbasis Rasio Skala

#### A. Definisi Sederhana
RMSLE menghitung jarak kesalahan setelah harga asli dan harga tebakan sama-sama diubah ke dalam bentuk **skala logaritma natural ($\ln$)**:
$$\text{RMSLE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} \left( \ln(\hat{y}_i + 1) - \ln(y_i + 1) \right)^2}$$

#### B. Mengapa Ini Penting bagi Pelatihan Model Kita?
Di proyek kita, sebelum model dilatih, variabel harga diubah menjadi logaritma: $z = \ln(\text{price} + 1)$.  
Alasannya sama persis dengan prinsip proporsional di atas: agar algoritma komputer saat belajar tidak menganak-emaskan villa mewah dan tetap memperhatikan homestay murah dengan bobot yang adil.

---

## 3. HIERARKI METRIK: MANA METRIK YANG PALING KITA PERCAYA DAN APA BATAS-BATASNYA?

### A. Jawaban Hitam-Putih: Metrik Mana yang Paling Kita Percaya?
Jika dosen penguji bertanya:  
**"Dari semua metrik yang kamu hitung, metrik mana yang PALING KAMU PERCAYA dan paling jujur mencerminkan akurasi sistemmu di Bali?"**

Jawaban hitam-putih kita adalah:  
👉 **MedAE (Median Absolute Error = Rp 391.492 per malam)**.

#### Mengapa MedAE Menjadi Metrik Nomor Satu yang Paling Kita Percaya?
1. **Kondisi Riil Pasar Bali**: Data tarif penginapan di Bali memiliki jurang harga yang sangat curam (*positive skewness*). Mayoritas pasar adalah kamar homestay dan villa reguler (Rp 300 ribu s.d Rp 2,5 juta), namun ada segelintir villa mewah (Rp 6 juta s.d Rp 10 juta per malam).
2. **Mengapa MAE Tidak Bisa Dipercaya Penuh?**: MAE (Rp 764.207) menghitung rata-rata biasa. Kesalahan prediksi pada segelintir villa mewah yang meleset Rp 3–6 juta langsung **meracuni dan menarik angka rata-rata melambung tinggi**. MAE memberi kesan seolah-olah model kita meleset Rp 764 ribu di semua tempat, padahal aslinya tidak demikian!
3. **MedAE Paling Jujur**: MedAE memotong bias pencilan villa mewah tersebut dengan mengambil nilai tengah (rata-rata urutan ke-98 dan ke-99 dari 196 data uji). Angka **Rp 391.492** adalah bukti konkret bahwa **untuk 50% listing sewa di Bali (98 dari 196 properti), kesalahan tebakan model kita berada di bawah Rp 391 ribu per malam**.

---

### B. Jejeran 5 Metrik dengan Garis Batas dan Perannya Masing-Masing

Kami tidak memakai metrik secara acak. Kelima metrik pada evaluasi (`model_benchmark_results.csv`) dijejerkan dengan pembagian peran dan batas yang tegas:

```
[HIERARKI & GARIS BATAS 5 METRIK KITA]
  ├── TIER 1: MedAE (Rp 391.492)  ──> PALING KITA PERCAYA (Jujur di Lapangan, Bebas Bias Outlier)
  ├── TIER 2: Test R² (67,08%)    ──> STANDAR FORMAL AKADEMIK (Skala log_price; Uji Pola Global)
  ├── TIER 3: MdAPE (Akurasi ~70%)──> BAHASA BISNIS PEMILIK (Bebas Skala Rupiah, Adil Antar Kamar)
  ├── TIER 4: MAE (Rp 764.207)    ──> PEMBANDING RATA-RATA (Rata-rata Selisih Moneter Global)
  └── TIER 5: RMSE (Rp 1.231.953) ──> ALARM ERROR EKSTREM (Penalti Kuadrat bagi Vila Mahal)
```

| Tingkat Kepercayaan | Nama Metrik | Nilai CatBoost | Garis Batas Penggunaan & Siapa yang Menanyakan |
|:---:|---|:---:|---|
| **TIER 1 (Paling Dipercaya)** | **MedAE** *(Median Absolute Error)* | **Rp 391.492** | **Batas Penggunaan**: Tolok ukur keakuratan moneter riil untuk 50% akomodasi reguler di Bali tanpa tertipu pencilan villa mewah.<br>**Ditujukan untuk**: Pembuktian performa sistem nyata kepada tim penguji saat menganalisis bias data. |
| **TIER 2 (Standar Akademik)** | **Test $R^2$** *(Koefisien Determinasi, skala log)* | **67,08%** | **Batas Penggunaan**: Membuktikan secara statistik bahwa 38 atribut di tabel data kita berhasil menjelaskan 67,08% variasi logaritmik harga sewa pasar.<br>**Ditujukan untuk**: Syarat formal kelulusan laporan / artikel jurnal ilmiah. |
| **TIER 3 (Bahasa Bisnis)** | **MdAPE** *(Akurasi Relatif Pasar)* | **30,09% meleset** *(Akurasi 69,91%)* | **Batas Penggunaan**: Menilai persentase proporsional kesalahan terhadap harga asli properti agar adil bagi homestay murah maupun villa mahal.<br>**Ditujukan untuk**: Komunikasi dengan pemilik properti / masyarakat umum yang ingin tahu persentase akurasi sistem. |
| **TIER 4 (Pembanding Klasik)** | **MAE** *(Mean Absolute Error)* | **Rp 764.207** | **Batas Penggunaan**: Mengetahui nilai rata-rata meleset secara global dalam Rupiah.<br>**Catatan Batas**: *Tidak boleh dipakai sendirian* karena angka rata-ratanya tertarik naik oleh villa mewah. |
| **TIER 5 (Alarm Pencilan)** | **RMSE** *(Root Mean Squared Error)* | **Rp 1.231.953** | **Batas Penggunaan**: Mendeteksi seberapa besar selisih prediksi pada segelintir villa mahal karena galat dikuadratkan.<br>**Ditujukan untuk**: Menguji apakah ada segmen tarif atas yang masih meleset lebar dibanding MAE. |

---

## 4. EVALUASI BERTINGKAT (TIER ANALYSIS): MENGAPA EVALUASI GLOBAL BELUM CUKUP?

Dalam data science tingkat tinggi, menyebutkan akurasi global satu pulau Bali saja belum membuktikan bahwa model Anda adil (*unbiased*).  
Bisa saja sebuah model sangat pintar di homestay murah tetapi rusak total di villa mahal, atau sebaliknya.

Oleh karena itu, kami melakukan **Evaluasi Bertingkat (Tier Analysis)** pada 196 data uji CatBoost:

```
[196 Sampel Data Uji Independen]
  ├── Homestay / Budget (< Rp 750 Ribu)      : 41 unit | MedAE: Rp 150.589   | Akurasi: 61,20%
  ├── Villa Reguler (Rp 750 Ribu - Rp 2,5 Jt): 89 unit | MedAE: Rp 306.870   | Akurasi: 75,16%  <-- SEGMEN UTAMA BALI
  ├── Villa Menengah (Rp 2,5 Jt - Rp 6 Juta) : 56 unit | MedAE: Rp 1.231.149 | Akurasi: 65,31%
  └── Villa Premium (Rp 6 Juta - Rp 10 Juta) : 10 unit | MedAE: Rp 3.501.920 | Akurasi: 53,06%
```

### Insight Emas untuk Asistensi:
Perhatikan segmen **Villa Reguler (Rp 750 Ribu s.d Rp 2,5 Juta)**:
* Ini adalah **populasi terbesar akomodasi liburan di Bali pada himpunan uji (89 dari 196 data uji atau 45,4% pasar)**.
* Pada segmen krusial ini, model CatBoost mencapai performa puncak: **Akurasi Relatif Median 75,16%** (`MdAPE 24,84%`) dengan nilai tengah kesalahan (MedAE) hanya **Rp 306.870 per malam**.

---

## 5. BEDAH 3 MODEL MACHINE LEARNING KITA SAMPAI KE MEKANISME FISIKNYA

Mengapa kita membandingkan **Random Forest**, **XGBoost**, dan **CatBoost**?  
Ketiganya mewakili **tiga generasi evolusi algoritma ensemble berbasis pohon (*Tree-Based Ensemble*)** paling disegani di dunia data tabular:

```
[Generasi 1: Bagging Paralel]    ──>    [Generasi 2: Gradient Boosting]    ──>    [Generasi 3: Ordered Boosting]
   Random Forest (2001)                     XGBoost (2016)                           CatBoost (2018)
- 300 Pohon Independen                  - Pohon Sekuensial Residual              - Ordered Target Statistics
- Memotong Variansi Kesalahan           - Gradien Orde-2 (Taylor Expansion)      - Oblivious Symmetric Trees
- Pipeline ColumnTransformer (OHE 101)  - Pipeline ColumnTransformer (OHE 101)   - Native Kategori Wilayah & NaN
```

---

### 5.1 Pohon Keputusan (Decision Tree) sebagai Batu Bata Dasar

Sebelum memahami ketiga model di atas, Anda harus paham apa itu **Decision Tree (Pohon Keputusan)**:
Bayangkan Anda ingin menebak harga sewa sebuah tempat menginap di Bali. Anda mengajukan serangkaian pertanyaan ya/tidak:
1. *Apakah kapasitas tamu > 2 orang?*
   * Ya $\rightarrow$ *Apakah memiliki kolam renang pribadi?*
     * Ya $\rightarrow$ *Apakah lokasinya di Seminyak/Canggu?* $\rightarrow$ **Tebakan: Rp 2.500.000**.
     * Tidak $\rightarrow$ *Apakah lokasinya di Tabanan?* $\rightarrow$ **Tebakan: Rp 1.100.000**.
   * Tidak $\rightarrow$ *Apakah jenisnya Kamar Sewa Homestay?* $\rightarrow$ **Tebakan: Rp 350.000**.

**Kelemahan Fatal Satu Pohon Tunggal**:  
Satu pohon keputusan tunggal sangat rakus (*greedy*) dan rapuh. Pohon akan terus membuat cabang rumit sampai menghafal data latihan secara berlebihan (**Overfitting**). Saat diuji pada properti baru, tebakannya sering meleset jauh.  
Untuk mengatasi kelemahan satu pohon, manusia menciptakan **Ensemble Learning (Menggabungkan Ratusan Pohon)**.

---

### 5.2 Model 1: Random Forest Regressor (Prinsip Musyawarah 300 Juri)

#### A. Filosofi Kerja: Bagging (Bootstrap Aggregating)
Ditemukan oleh Leo Breiman pada tahun 2001. Daripada percaya pada satu juri pintar yang bisa salah, Random Forest membentuk sebuah dewan juri yang terdiri dari **300 pohon keputusan independen**:
1. **Bootstrap Sampling**: Setiap pohon dilatih menggunakan sampel baris data yang berbeda-beda, diambil secara acak dengan pengembalian (*random with replacement*).
2. **Random Subspacing**: Saat pohon ingin membuat percabangan simpul, pohon tidak boleh melihat seluruh 38 fitur sekaligus. Pohon hanya boleh memilih sebagian fitur acak (misal hanya boleh memilih antara kamar tidur, rating, atau jarak pantai). Hal ini mencegah pohon-pohon saling meniru dan memutus korelasi (*decorrelating trees*).
3. **Voting / Rata-rata**: Saat ada villa baru yang ingin diprediksi, seluruh 300 pohon memberikan tebakannya masing-masing. Prediksi akhir adalah **rata-rata matematika dari 300 pohon**:
   $$\hat{y} = \frac{1}{300} \sum_{b=1}^{300} T_b(x)$$

#### B. Mengapa Random Forest Hebat?
Secara teori probabilitas, merata-ratakan ratusan variabel acak independen akan **memangkas variansi kesalahan (*variance reduction*) secara drastis** tanpa menaikkan bias. Model menjadi sangat stabil dan tidak mudah tertipu pencilan.

#### C. Kelemahan Random Forest pada Data Properti Bali
1. **Boros Memori**: Random Forest menyimpan 300 pohon utuh asimetris tanpa berbagi aturan kedalaman seperti pohon simetris CatBoost (sehingga setelah benchmark selesai, Random Forest tidak dipakai untuk produksi dan hanya model champion `catboost_pricing_model.cbm` berukuran ~726 KiB / 743.720 byte yang disimpan).
2. **Pra-Pemrosesan Pipeline (`101` Kolom Tersandi)**: Random Forest tidak membaca teks kategori secara langsung. Pada pipeline `ColumnTransformer` proyek ini, 3 kategori latih (`9` kabupaten + `53` kecamatan + `4` tipe = **66 kolom dummy**) digabung bersama `SimpleImputer(median)` pada `rating` (`35` numerik) menjadi **101 kolom masukan** yang renggang (*sparse matrix*). Ini menciptakan tabel lebar yang menyulitkan pohon membaca interaksi lokasi yang halus.

---

### 5.3 Model 2: XGBoost Regressor (Prinsip Evaluasi Tryout Berkelanjutan)

#### A. Filosofi Kerja: Sequential Residual Learning
Diciptakan oleh Tianqi Chen pada tahun 2016. Berbeda 180 derajat dari Random Forest yang membangun pohon secara paralel dan mandiri, XGBoost membangun pohon secara **berurutan (sekuensial)** seperti murid yang belajar dari hasil tryout:
1. **Pohon 1** membuat tebakan awal kasar untuk seluruh villa. Tentu saja tebakannya masih banyak salahnya. Selisih antara harga asli dan tebakan pohon 1 disebut **Residual (Sisa Kesalahan)**.
2. **Pohon 2** TIDAK dilatih untuk menebak harga villa, melainkan dilatih khusus untuk **menebak sisa kesalahan dari Pohon 1**.
3. **Pohon 3** dilatih untuk menebak sisa kesalahan yang belum berhasil diselesaikan oleh Pohon 2, dan seterusnya hingga **350 pohon**.
4. Prediksi akhir adalah penjumlahan bertahap dari pohon-pohon tersebut yang diperlambat dengan laju belajar konservatif (*learning rate* $\eta = 0.035$):
   $$\hat{y}_i^{(t)} = \hat{y}_i^{(t-1)} + \eta f_t(x_i)$$

#### B. Senjata Rahasia XGBoost: Ekspansi Taylor Orde-2 & Regularisasi L1/L2
XGBoost menggunakan matematika kalkulus tingkat tinggi untuk mencari bentuk pohon optimal:
* Menghitung gradien tingkat pertama ($g_i$, turunan pertama) dan Hessian ($h_i$, turunan kedua kurvatur).
* Menyematkan penalti regularisasi matematis pada setiap daun pohon:
  $$\Omega(f) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^{T} w_j^2$$
  Jika sebuah pohon mencoba membuat daun terlalu banyak ($T$) atau memberikan bobot tebakan yang terlalu ekstrem ($w_j$), algoritma akan langsung "menghukum" pohon tersebut. Ini alasan mengapa XGBoost menjadi standar kompetisi data science dunia.

#### C. Kelemahan XGBoost pada Pipeline Bali Ini
Sama seperti Random Forest, XGBoost dalam skrip proyek ini dimasukkan ke `build_tree_pipeline` (`ColumnTransformer` dengan `OneHotEncoder(handle_unknown="ignore")` menjadi 66 kolom dummy + 35 kolom numerik dengan `SimpleImputer(median)` = **101 kolom tersandi**). Meskipun mesin XGBoost mampu menelan `NaN` secara native bila dijalankan terpisah, pemecahan kategori wilayah menjadi 66 kolom biner tetap memecah kerapatan sampel (*data fragmentation*).

---

### 5.4 Model 3: CatBoost Regressor (Sang Juara Data Kategori & Wilayah Bali)

#### A. Filosofi Kerja: Mengapa CatBoost Diciptakan?
Ditemukan oleh peneliti Yandex (Prokhorenkova dkk., 2018), CatBoost singkatan dari **Categorical Boosting**. Model ini dirancang untuk mengatasi kelemahan terbesar XGBoost dan LightGBM saat menghadapi data tabular yang penuh dengan fitur kategori berkardinalitas tinggi (seperti nama kabupaten, nama kecamatan, dan tipe penginapan di Bali).

CatBoost memiliki **Tiga Pilar Inovasi Mutakhir**:

#### 1. Ordered Target Statistics (Pengolahan Kategori Tanpa Kebocoran Data)
Bagaimana cara mengubah teks seperti *"Kecamatan Ubud"* menjadi angka matematika tanpa melakukan One-Hot Encoding?  
Algoritma biasa biasanya menghitung rata-rata harga di Ubud lalu menggantikan teks Ubud dengan rata-rata tersebut (*Target Encoding*). **Ini berbahaya karena menyebabkan kebocoran data (*Target Leakage*)**—model mengintip jawaban harga sebelum belajar.

CatBoost menyelesaikan ini dengan prinsip urutan acak (*Ordered Principle*):
* Sistem mengacak urutan baris data secara acak.
* Nilai numerik untuk kecamatan suatu villa hanya dihitung berdasarkan villa-villa yang berada **sebelum villa tersebut dalam urutan acak**:
  $$\hat{x}_{k}^i = \frac{\sum_{j=1}^{i-1} [x_{j}^i = x_{k}^i] \cdot y_j + a \cdot P}{\sum_{j=1}^{i-1} [x_{j}^i = x_{k}^i] + a}$$
* Hasilnya: 54 kecamatan dan 9 kabupaten di Bali pada dataset bersih dapat diproses langsung sebagai angka densitas yang akurat **tanpa kebocoran data (0% data leakage)** dan tanpa menambah kolom One-Hot Encoding!

#### 2. Oblivious Trees (Pohon Keputusan Simetris)
Pohon keputusan pada XGBoost dan Random Forest bentuknya asimetris (cabang kiri bisa tumbuh panjang ke bawah, cabang kanan pendek).  
CatBoost menggunakan **Pohon Simetris (Oblivious Trees)**:
* Pada kedalaman pohon yang sama, aturan pemisahnya WAJIB SAMA PERSIS untuk seluruh simpul.
* Struktur simetris ini bertindak sebagai regularisasi alami yang mencegah pohon membuat cabang-cabang aneh yang menghafal data.
* **Kecepatan Komputasi Kilat**: Pohon simetris dapat dievaluasi di level prosesor komputer hanya menggunakan operasi biner (*bitwise operations*), membuat waktu inferensi kalkulator kita di antarmuka Streamlit berjalan dalam hitungan milidetik.

#### 3. Ordered Boosting (Mencegah Pergeseran Prediksi)
Pada boosting konvensional, residual yang digunakan untuk melatih pohon baru dihitung dari model yang telah melihat data yang sama, menciptakan bias pergeseran (*prediction shift*). CatBoost mempertahankan model independen sehingga perhitungan kesalahan residual selalu bersih dan tidak bias.

---

### 5.5 Mengapa LightGBM dan Stacking Ridge Kita Singkirkan?

Pada tahap awal sebelum sinkronisasi repositori, sistem sempat mencoba skema beberapa model tambahan (termasuk LightGBM dan Ridge Regression Stacking). Kami menyingkirkan keduanya berdasarkan prinsip ilmiah **Occam's Razor (Prinsip Parsimoni)**:
1. **LightGBM Redundan**: Pada dataset berukuran 978 baris dengan fitur kategori wilayah dominan, LightGBM memberikan pendekatan histogram boosting yang sejenis dengan XGBoost namun tanpa keunggulan struktur pohon simetris CatBoost.
2. **Stacking Ridge Membawa Masalah Baru**: Menumpuk (*stacking*) prediksi beberapa model menggunakan meta-learner Ridge Regression melipatgandakan kompleksitas sistem saat inferensi (harus memuat banyak model sekaligus ke memori) dan menghilangkan kejelasan penjelasan langsung berbasis pohon (*TreeExplainer SHAP*).
3. **Keputusan Arsitektur Bersih**: Tiga model terpilih (**Random Forest**, **XGBoost**, **CatBoost**) memberikan narasi ilmiah yang paling kokoh: mewakili evolusi dari Bagging klasik, Gradient Boosting standar industri, hingga Ordered Boosting mutakhir.

---

## 6. TABEL KOMPARASI HEAD-TO-HEAD 3 MODEL DI DATA UJI BALI

> [!IMPORTANT]
> **MODEL FINAL YANG KITA PILIH DAN DIGUNAKAN DI APLIKASI: CATBOOST REGRESSOR!**  
> Proyek kita melatih dan menguji 3 model ensemble untuk komparasi ilmiah. **CatBoost Regressor keluar sebagai Juara 1**, sehingga berkas model `models/catboost_pricing_model.cbm` (~726 KB / 743.720 byte) adalah satu-satunya model yang dimuat dan dijalankan oleh antarmuka web kalkulator kita (`aplikasi/app.py`).

Berikut adalah bukti empiris komparasi 3 model pada **196 data uji independen** (`aplikasi/reports/model_benchmark_results.csv`):

| Parameter Evaluasi | Random Forest (Baseline) | XGBoost Regressor | CatBoost Regressor (Champion) | Pemenang & Keterangan Ilmiah |
|---|:---:|:---:|:---:|---|
| **Paradigma Algoritma** | Bagging (Paralel) | Gradient Boosting Klasik | Ordered Boosting Simetris | **CatBoost** (Arsitektur Generasi 3) |
| **Penanganan 54 Kecamatan** | Pipeline `OHE` + `SimpleImputer` (101 kolom) | Pipeline `OHE` + `SimpleImputer` (101 kolom) | **Native Ordered Statistics & NaN** (38 kolom) | **CatBoost** (Tanpa ledakan dimensi kolom) |
| **Skor 5-Fold CV $R^2$** | 62,91% | 66,31% | **66,36%** | **CatBoost Juara 1** (Paling stabil di validasi silang) |
| **Skor Test $R^2$ (Data Uji)** | 65,60% | 66,22% | **67,08%** | **CatBoost Juara 1** (Daya jelajah variansi tertinggi) |
| **Median Absolute Error (MedAE)**| Rp 470.400 | Rp 411.693 | **Rp 391.492** | **CatBoost Juara 1** (Selisih tipikal terendah) |
| **Mean Absolute Error (MAE)** | Rp 809.098 | Rp 773.730 | **Rp 764.207** | **CatBoost Juara 1** (Rata-rata selisih terendah) |
| **RMSE (Data Uji)** | Rp 1.264.986 | Rp 1.249.748 | **Rp 1.231.953** | **CatBoost Juara 1** (Penalti kuadrat terendah) |
| **Tingkat Error Relatif (MdAPE)**| 31,63% | **27,61%** | 30,09% | XGBoost tipis unggul pada median rasio global, CatBoost unggul di segmen Villa Reguler (24,84%) |
| **Akurasi Relatif Pasar** | 68,37% | **72,39%** | 69,91% | Semua model konvergen di kisaran 68%–72% |
| **Status Artefak Produksi** | Dihapus pasca-benchmark | Dihapus pasca-benchmark | **`catboost_pricing_model.cbm` (726 KB)** | **CatBoost Dipilih Tunggal & Ringan untuk App** |

---

## 7. KAMUS MENTAL TANYA-JAWAB PENGUJI (CHEAT SHEET PEMAHAMAN KONSEPTUAL)

Gunakan logika di bawah ini jika dosen pengampu menguji pemahaman konseptual Anda:

#### Q1: "Mengapa nilai R² CatBoost Anda 67,08%, ke mana perginya 32,92% sisanya?"
* **Jawaban Konseptual**:  
  *"Nilai 67,08% membuktikan bahwa 38 kolom atribut yang ada di dataset kita (kamar, tipe properti, fasilitas kolam, jarak sentra pantai/wisata, rating, dan kecamatan) sudah berhasil menangkap mayoritas pola penentu harga di Bali, Pak. Sisa 32,92% variasi harga dipengaruhi faktor yang memang tidak tersedia kolom atributnya pada halaman listing standar Airbnb, seperti luas bangunan dalam meter persegi ($m^2$), arah pemandangan riil (view laut/sawah), dan fluktuasi musim sewa liburan (high season vs low season). Untuk data pariwisata lintas kabupaten yang heterogen, capaian Test R² 67,08% (konsisten dengan CV R² 66,36% tanpa overfitting) sangat sehat dan valid secara akademik."*

#### Q2: "Mengapa Anda membanggakan MedAE daripada MAE?"
* **Jawaban Konseptual**:  
  *"Karena data harga sewa di Bali memiliki sebaran yang menceng (skewed oleh villa mewah bernilai tinggi), Pak. Di data uji kita ada properti kelas atas hingga Rp 9,79 juta per malam yang selisih prediksinya mencapai Rp 3–6 juta. Selisih besar pada segelintir villa kelas atas ini menarik angka rata-rata (MAE) naik menjadi Rp 764 ribu.*  
  *Sebaliknya, MedAE mengurutkan seluruh 196 kesalahan tebakan lalu mengambil nilai tengah (antara urutan ke-98 dan ke-99). Angka MedAE Rp 391.492 membuktikan bahwa bagi separuh populasi penginapan di Bali (98 dari 196 properti uji), tebakan model kita tidak meleset lebih dari sekitar Rp 391 ribu per malam."*

#### Q3: "Apa bukti konkret bahwa CatBoost lebih unggul dari XGBoost dan Random Forest pada kasus Bali?"
* **Jawaban Konseptual**:  
  *"Bukti terkuat ada pada cara menangani 54 kecamatan (53 kecamatan di data latih + Kuta Selatan yang khusus muncul di data uji) dan 9 kabupaten di Bali serta kestabilan akurasinya di setiap metrik utama, Pak. Di pipeline skrip kita, Random Forest dan XGBoost memakai One-Hot Encoding + SimpleImputer(median) yang melebarkan matriks menjadi 101 kolom (66 dummy + 35 numerik). CatBoost mengolah teks kecamatan langsung menggunakan Ordered Target Statistics tanpa kebocoran data serta memproses rating kosong (`NaN`) secara native.*  
  *Hasilnya terbukti nyata di data uji 196 sampel: CatBoost menang serentak pada CV R² (66,36%), Test R² (67,08% vs XGBoost 66,22% & RF 65,60%), MAE terendah (Rp 764.207), RMSE terendah (Rp 1.231.953), dan MedAE terendah (Rp 391.492 vs XGBoost Rp 411.693). Terlebih lagi, pada segmen pasar terbesar di Bali yaitu Villa Reguler (89 dari 196 sampel uji atau 45,4%), akurasi relatif median CatBoost mencapai 75,16% (MdAPE 24,84%) dengan nilai tengah kesalahan hanya Rp 306.870 per malam."*

#### Q4: "Mengapa target harga diubah ke skala logaritma natural?"
* **Jawaban Konseptual**:  
  *"Agar model belajar secara adil dan proporsional terhadap harga kamar, Pak. Meleset Rp 300 ribu di homestay murah seharga Rp 300 ribu itu kesalahan fatal (100% meleset), sedangkan meleset Rp 300 ribu di villa Rp 10 juta hampir tidak terasa (cuma 3% meleset).*  
  *Jika harga tidak diubah ke skala logaritma, model komputer akan sibuk memikirkan villa-villa mewah saja dan mengabaikan homestay murah. Transformasi logaritma menyeimbangkan bobot kesalahan sehingga akurasi di properti murah maupun mewah tetap terjaga."*
