# Peta Lengkap Semua Rumus di Naskah Jurnal

Dokumen ini memetakan **seluruh rumus yang tercantum pada Bagian 2 naskah jurnal** (*4 blok rumus alur kolom/pra-pemrosesan* dan *8 persamaan matematis bernomor `Equation (1)`–`Equation (8)`*), lengkap dengan arti tiap simbol, alasan pemakaiannya, contoh hitungan nyata, dan posisi implementasinya di kode Python proyek.

---

## 1. Peta Cepat Seluruh Rumus

| No | Nama Rumus | Letak di Jurnal | Jenis | Fungsi Inti | Sumber Kode Python |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **A1** | Mutasi Kolom Pengayaan (`6 + 24 = 30`) | Subbab 2.2 | Alur Kolom | Menggabungkan 6 kolom dasar Kaggle dengan 24 atribut baru hasil *scraping* & ekstraksi | [02_merge_and_build_dataset.py](../../aplikasi/scripts/02_merge_and_build_dataset.py#L386-L417) |
| **A2** | Mutasi Kolom Rekayasa (`30 − 1 + 13 = 42`) | Subbab 2.4 | Alur Kolom | Membuang 1 kolom `url`, menambah 12 prediktor + 1 target log menjadi 38 prediktor + 4 nonprediktor | [03_preprocess_and_clean.py](../../aplikasi/scripts/03_preprocess_and_clean.py#L116-L133) |
| **A3** | Jalur Pra-Pemrosesan RF & XGBoost (`38 → 101`) | Subbab 2.5 | Alur Fitur | Menambal `rating` kosong pakai median lalu memekarkan 3 kolom teks menjadi 66 kolom biner `dummy` (`66 + 35 = 101`) | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L62-L69) |
| **A4** | Jalur Pra-Pemrosesan CatBoost (`38 → 38`) | Subbab 2.5 | Alur Fitur | Mengolah 3 kolom kategori via *ordered target statistics* dan membiarkan `NaN` asli di percabangan pohon | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L135-L138) |
| **(1)** | Jarak Haversine ($d_{i,h}$) | Subbab 2.4, Eq. (1) | Matematis | Menghitung jarak fisik permukaan bumi (km) dari koordinat unit ke 6 titik wisata/bandara Bali | [03_preprocess_and_clean.py](../../aplikasi/scripts/03_preprocess_and_clean.py#L43-L49) |
| **(2)** | Transformasi Logaritmik ($y_i^{(\log)}$) | Subbab 2.4, Eq. (2) | Matematis | Mengecilkan skala harga Rupiah sebelum model dilatih agar vila mahal tidak mendominasi bobot | [03_preprocess_and_clean.py](../../aplikasi/scripts/03_preprocess_and_clean.py#L104) |
| **(3)** | Eksponensial Balik ($\widehat{y}_i$) | Subbab 2.6, Eq. (3) | Matematis | Mengembalikan prediksi skala log ke Rupiah asli agar selisih harga terbaca langsung | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L74-L75) |
| **(4)** | Koefisien Determinasi ($R^2$) | Subbab 2.6, Eq. (4) | Metrik (Log) | Mengukur berapa besar keragaman harga yang berhasil dijelaskan model dibanding rata-rata polos | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L73) |
| **(5)** | *Mean Absolute Error* (MAE) | Subbab 2.6, Eq. (5) | Metrik (IDR) | Rata-rata selisih absolut harga dalam Rupiah pada seluruh sampel uji | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L76) |
| **(6)** | *Root Mean Squared Error* (RMSE) | Subbab 2.6, Eq. (6) | Metrik (IDR) | Akar rata-rata kuadrat galat; menghukum kesalahan besar pada vila mahal lebih berat | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L77) |
| **(7)** | *Median Absolute Error* (MedAE) | Subbab 2.6, Eq. (7) | Metrik (IDR) | Nilai tengah selisih Rupiah; menunjukkan akurasi tipikal mayoritas unit tanpa bias vila ekstrem | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L78) |
| **(8)** | *Median Absolute Percentage Error* (MdAPE) | Subbab 2.6, Eq. (8) | Metrik (%) | Nilai tengah persentase meleset relatif terhadap tarif asli properti | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L79) |

---

## 2. Kelompok A — Rumus Alur Kolom & Jalur Pra-Pemrosesan Model

### A1. Rumus Penambahan Kolom Pengayaan (Subbab 2.2)

$$\text{Dataset Awal Kaggle (6 Kolom)} + \text{Pengayaan Web Scraping \& Parsing (24 Kolom)} = \text{Dataset Hasil Pengayaan (30 Kolom)}$$

- **6 Kolom awal (`AirBnB_Bali_All.csv`):** `nama` $\to$ `name`, `harga` (dinormalisasi ke 1 malam) $\to$ `price_idr`, `rating`, `jumlah_review` $\to$ `review_count`, `link` $\to$ `url`, `wilayah` $\to$ `regency`.
- **24 Kolom baru (`+24`):** `room_id` (1), lokasi & tipe (`sub_district`, `latitude`, `longitude`, `property_type`: 4), kapasitas (`is_room_only`, `accommodates`, `bedrooms`, `beds`, `bathrooms`: 5), status operasi (`is_new_listing`, `is_superhost`, `has_self_checkin`: 3), fasilitas biner (`has_private_pool`, `has_pool`, `has_bathtub`, `has_parking`, `has_workspace`, `has_jacuzzi`, `has_service_staff`: 7), dan kata kunci NLP judul/deskripsi (`nlp_luxury`, `nlp_beach_ocean`, `nlp_nature_view`, `nlp_budget_cozy`: 4).
- **Hasil:** $6 + 24 = 30\text{ kolom}$ di tabel pengayaan.

---

### A2. Rumus Pembentukan Tabel Akhir dari *Feature Engineering* (Subbab 2.4)

$$30\text{ Kolom Pengayaan} - 1\text{ Kolom URL} + 13\text{ Rekayasa Fitur} = 42\text{ Kolom Akhir} = 4\text{ Metadata \& Target} + 38\text{ Fitur Prediktor } X$$

- **Dibuang (`-1`):** kolom `url`, karena alamat tautan tidak membantu memprediksi harga sewa.
- **Ditambah (`+13`):**
  - 4 fitur rasio kepadatan: `guests_per_bedroom`, `baths_per_bedroom`, `beds_per_bedroom`, `total_rooms_index`.
  - 1 skor fasilitas mewah tanpa bobot manual: `total_luxury_amenities` (`0` sampai `5`).
  - 7 fitur jarak Haversine: 6 jarak ke `canggu_seminyak`, `ubud_center`, `uluwatu`, `sanur`, `kintamani`, `airport`, plus 1 jarak terdekat ke 4 sentra wisata utama (`min_dist_tourism_hub_km`).
  - 1 kolom target hasil logaritma: `log_price`.
- **Pecahan 42 kolom akhir pada `dataset_train.csv` & `dataset_test.csv`:**
  - **4 kolom bukan prediktor:** `room_id`, `name`, `price_idr` (untuk evaluasi bisnis dalam Rupiah), `log_price` (target $y$ yang diprediksi model).
  - **38 fitur prediktor $X$:** 26 atribut dari tahap pengayaan (`30 - 3 metadata [room_id, name, price_idr] - 1 url`) ditambah 12 fitur hasil rekayasa.

---

### A3 vs A4. Kedua Jalur Pra-Pemrosesan Model (Subbab 2.5)

Kedua baris rumus di Subbab 2.5 menjelaskan **perlakuan berbeda** terhadap input $X$ yang sama persis (`38` fitur: **3 kolom teks kategori** + **35 kolom angka**):

#### Jalur A3 (Random Forest & XGBoost)
$$38\text{ Fitur Prediktor } X \longrightarrow \text{SimpleImputer (median)} + \text{One-Hot Encoding (3 Kategori} \to 66\text{ Dummy Biner)} + 35\text{ Numerik} \longrightarrow 101\text{ Fitur Masukan}$$

- **Apa artinya:**
  1. **Untuk 35 kolom angka:** `SimpleImputer(strategy="median")` menambal kolom `rating` yang kosong (`NaN` pada 267 unit baru) dengan nilai tengah data latih (**4,95**), supaya tidak dianggap `0` atau membuat model lama error. Kolom angka lain tidak ada yang kosong.
  2. **Untuk 3 kolom teks (`regency`, `sub_district`, `property_type`):** `OneHotEncoder` memecah setiap nama unik menjadi 1 kolom sakelar `1/0` (*dummy*):
     - `regency`: `9` kabupaten/kota di data latih $\to$ `9` kolom.
     - `sub_district`: `53` kecamatan muncul di `782` data latih $\to$ `53` kolom. *(Kecamatan `Kuta Selatan` kebetulan hanya jatuh ke `196` data uji; aturan `handle_unknown="ignore"` membuatnya aman bernilai `0` di seluruh `53` kolom kecamatan tanpa crash dan tanpa kebocoran data uji).*
     - `property_type`: `4` jenis properti $\to$ `4` kolom.
  3. **Hasil total:** $(9 + 53 + 4) + 35 = 66 + 35 = 101\text{ fitur angka}$.

#### Jalur A4 (CatBoost Regressor)
$$38\text{ Fitur Prediktor } X \longrightarrow \text{Ordered Target Statistics (3 Kategori)} + \text{Percabangan NaN Native} \longrightarrow 38\text{ Fitur Masukan}$$

- **Apa artinya:**
  1. **Untuk 3 kolom teks kategori:** tidak dipecah menjadi 66 kolom `0/1`, melainkan diubah langsung oleh CatBoost secara internal memakai *ordered target statistics*—yaitu mengonversi nama kecamatan/kabupaten/tipe menjadi estimasi rata-rata harga secara berurutan per permutasi acak baris agar tidak membocorkan target baris itu sendiri (*target leakage*).
  2. **Untuk nilai `NaN` pada `rating`:** dibiarkan tetap `NaN` (tidak ditambal angka `4,95`), lalu pohon CatBoost memutuskan sendiri arah cabang terbaik (kiri atau kanan) bagi properti baru.
  3. **Hasil total:** tetap **38 fitur** tanpa pembengkakan dimensi kolom.

---

## 3. Kelompok B — Persamaan Spasial & Pasangan Transformasi Harga (`Equation (1)–(3)`)

### Equation (1) — Jarak Haversine ($d_{i,h}$)

$$d_{i,h} = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\varphi}{2}\right) + \cos(\varphi_i)\cos(\varphi_h)\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)$$

- **Arti simbol:**
  - $d_{i,h}$: jarak lurus di atas permukaan lengkung bumi antara properti ke-$i$ dengan simpul wisata $h$ (satuan **km**).
  - $R = 6.371{,}0\text{ km}$: jari-jari rata-rata bola bumi.
  - $\varphi_i, \varphi_h$: garis lintang (*latitude*) properti dan simpul wisata dalam satuan **radian** ($\text{radian} = \text{derajat} \times \pi / 180$).
  - $\lambda_i, \lambda_h$: garis bujur (*longitude*) properti dan simpul wisata dalam **radian**.
  - $\Delta\varphi = \varphi_h - \varphi_i$ dan $\Delta\lambda = \lambda_h - \lambda_i$: selisih lintang dan bujur.
- **Kenapa pakai rumus ini, bukan selisih koordinat biasa?** Bumi itu melengkung seperti bola, dan jarak 1 derajat bujur berubah sesuai garis lintang. Haversine menghitung jarak fisik sebenarnya (km) yang langsung dipakai ke 7 fitur jarak spasial.
- **Contoh nyata dari `dataset_test.csv`:**
  - Unit `room_id = 1717194563248411498` (*Stylish Cozy Studio at Kerobokan*, Denpasar Barat) berada di koordinat $(-8{,}6739^\circ,\; 115{,}1751^\circ)$.
  - Simpul `canggu_seminyak` berada di $(-8{,}6650^\circ,\; 115{,}1450^\circ)$.
  - Setelah dikonversi ke radian ($\varphi_i = -0{,}151388$, $\varphi_h = -0{,}151233$, $\Delta\varphi = 0{,}000155$, $\Delta\lambda = -0{,}000525$), rumus menghasilkan nilai akar $a = 7{,}35 \times 10^{-8}$ dan jarak tepat $d = \mathbf{3{,}4536\text{ km}}$.

---

### Equation (2) & Equation (3) — Pasangan Rumus Logaritmik dan Eksponensial Balik

Kedua rumus ini adalah **pasangan operasi bolak-balik** (*berlawanan persis seperti mengunci lalu membuka gembok*):

#### Equation (2) — Masuk ke Skala Logaritmik (Saat Pra-Pemrosesan sebelum Latih)
$$y_i^{(\log)} = \ln(1 + y_i)$$

#### Equation (3) — Kembali ke Skala Rupiah Asli (Saat Evaluasi setelah Prediksi)
$$\widehat{y}_i = \exp\left(\widehat{y}_i^{(\log)}\right) - 1$$

- **Arti simbol:**
  - $y_i$: tarif sewa harian asli (IDR/malam).
  - $y_i^{(\log)}$: tarif yang sudah dikompresi dengan logaritma natural ($\ln$, basis $e \approx 2{,}71828$) sebelum masuk ke pelatihan model.
  - $\widehat{y}_i^{(\log)}$: angka prediksi mentah yang dikeluarkan model (masih dalam skala logaritmik).
  - $\widehat{y}_i$: angka prediksi final setelah dikembalikan menjadi Rupiah ($\exp(x) = e^x$).
- **Kenapa harus diubah ke $\ln$ dulu, tidak langsung melatih pada Rupiah?**
  - Tarif asli 978 unit miring tajam ke kanan (*skewness* $= \mathbf{1{,}638}$): mayoritas unit seharga Rp 400 ribu–Rp 2,5 juta, tetapi segelintir vila mendekati **Rp 9,79 juta**.
  - Kalau dilatih langsung di skala Rupiah, meleset Rp 1 juta pada vila Rp 9 juta akan menghukum fungsi kuadrat/pohon jauh lebih keras daripada meleset Rp 300 ribu pada *homestay* Rp 500 ribu (yang secara persentase justru salah 60%).
  - Dengan $\ln(1 + y_i)$, sebaran harga memadat simetris (*skewness* turun menjadi **$-0{,}059$**), sehingga model adil mempelajari perubahan persentase di semua segmen.
- **Kenapa ada $+1$ dan $-1$?** Itu bentuk standar fungsi `np.log1p(y)` dan pasangannya `np.expm1(y_hat)`. Penambahan `+1` menjaga agar nilai nol tidak menghasilkan $\ln(0) = -\infty$, dan `-1` pada Equation (3) mengembalikannya ke nilai asli tanpa sisa bias `1` Rupiah.
- **Bukti hitung bolak-balik pada data nyata (`dataset_test.csv`):**
  1. Unit `1717194563248411498` bertarif asli $y_i = \text{Rp } 617.500$:
     - **Equation (2):** $y_i^{(\log)} = \ln(1 + 617.500) = \mathbf{13{,}333436}$.
     - Jika model memprediksi tepat $13{,}333436$, maka lewat **Equation (3):** $\widehat{y}_i = e^{13{,}333436} - 1 = \mathbf{\text{Rp } 617.500}$.
  2. Unit `1745051694636360970` (*Amerta Yora | Private Pool Villa*, Tabanan) bertarif $y_i = \text{Rp } 1.488.400 \iff y_i^{(\log)} = \mathbf{14{,}213213}$.
     - Bandingkan jarak angkanya: selisih harga **Rp 870.900** cuma terasa sebagai loncatan **0,88 unit** di skala logaritma ($14{,}21 - 13{,}33$). Itulah mengapa pohon keputusan jauh lebih stabil saat dilatih di skala log.

---

## 4. Kelompok C — Lima Persamaan Metrik Evaluasi (`Equation (4)–(8)`)

Pada `Equation (4)`–`(8)`: $N$ adalah jumlah unit evaluasi ($N = 196$ di data uji terpisah, $N = 782$ di validasi silang *out-of-fold*), $y_i$ adalah harga asli (IDR), $\widehat{y}_i$ adalah harga prediksi (IDR) hasil Equation (3), dan $y_i^{(\log)}, \widehat{y}_i^{(\log)}, \bar{y}^{(\log)}$ adalah nilai asli, prediksi, dan rata-rata pada skala logaritma.

### Equation (4) — $R^2$ (*Coefficient of Determination* / Koefisien Determinasi)

$$R^2 = 1 - \frac{\sum_{i=1}^{N}\left(y_i^{(\log)} - \widehat{y}_i^{(\log)}\right)^2}{\sum_{i=1}^{N}\left(y_i^{(\log)} - \bar{y}^{(\log)}\right)^2}$$

- **Cara membaca pecahannya secara awam:**
  - **Pembilang (atas):** total kesalahan kuadrat **model kita** ($\text{prediksi} - \text{asli}$).
  - **Penyebut (bawah):** total kesalahan kuadrat jika kita malas dan **menebak semua properti dengan satu angka rata-rata** $\bar{y}^{(\log)}$.
- **Arti nilai:** semakin mendekati **1,0**, artinya kesalahan model makin kecil dibanding tebakan rata-rata polos. Contoh: pada CatBoost uji terpisah, $R^2 = \mathbf{0{,}6708}$ berarti **67,08%** variasi harga (pada skala log) berhasil dijelaskan oleh ke-38 fitur properti, lokasi, dan fasilitas, sedangkan sisanya (~33%) berasal dari faktor tak tercatat seperti kualitas desain interior, promo musiman host, atau foto properti.
- **Kenapa dihitung di skala `log_price`, bukan IDR?** Karena model dilatih mengoptimalkan `RMSE` pada `log_price`, sehingga $R^2$ di skala log mengukur seberapa baik model menangkap pola tarif proporsional lintas seluruh kelas harga.

---

### Equation (5) vs Equation (6) — Rata-Rata Selisih Rupiah (`MAE`) vs Penalti Galat Besar (`RMSE`)

$$\text{MAE} = \frac{1}{N}\sum_{i=1}^{N}\left|y_i - \widehat{y}_i\right| \qquad\qquad \text{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^{N}\left(y_i - \widehat{y}_i\right)^2}$$

- **Equation (5) — MAE:** ambil semua selisih harga dalam Rupiah, hilangkan tanda minus (`|...|` = mutlak supaya salah kurang Rp 200 rb dan salah lebih Rp 200 rb tidak saling menghapus), lalu **rata-ratakan biasa**. Tiap Rp 100 ribu meleset dihitung seimbang.
- **Equation (6) — RMSE:** setiap selisih **dikuadratkan dulu** baru dirata-rata dan diakar kembali ke Rupiah. Karena dikuadratkan, satu kesalahan besar mendongkrak skor naik drastis (meleset `Rp 2 juta` bobot kuadratnya $20^2 = 400$ kali lebih berat daripada meleset `Rp 100 ribu` yang bobotnya $1^2 = 1$).
- **Fakta penting:** selama masih ada perbedaan besar kecilnya error antar unit, **`RMSE` selalu lebih besar daripada `MAE`**. Selisih jauh antara `RMSE` dan `MAE` menjadi alarm adanya properti ekstrem yang meleset lebar (di dataset kita, kelas Premium Rp 6–10 juta hanya ada 10 unit di data uji tetapi punya `MAE = Rp 3,23 juta`).

---

### Equation (7) vs Equation (8) — Akurasi Unit Tipikal (`MedAE`) dan Persentase Relatif (`MdAPE`)

$$\text{MedAE} = \text{median}\left(\left|y_i - \widehat{y}_i\right|\right) \qquad\qquad \text{MdAPE} = \text{median}\left(\frac{\left|y_i - \widehat{y}_i\right|}{y_i}\right) \times 100\%$$

- **Kenapa tidak cukup `MAE` dan `RMSE` saja?** Karena rata-rata (`MAE`) gampang tertarik naik oleh 5% vila mewah bertarif Rp 8–10 juta yang selisih prediksinya jutaan rupiah.
- **Equation (7) — MedAE:** mengurutkan seluruh selisih $|y_i - \widehat{y}_i|$ dari paling kecil ke paling besar, lalu mengambil **angka tepat di posisi tengah (persentil ke-50)**.
  - Contoh baca hasil CatBoost (`MedAE = Rp 391.492`): **separuh dari 196 properti uji** (`98` properti) prediksinya meleset **$\le$ Rp 391.492**, jauh lebih rendah dari rata-ratanya (`MAE = Rp 764.207`).
- **Equation (8) — MdAPE:** selisih Rupiah tiap properti dibagi dulu dengan **harga aslinya** ($y_i$), dikali `100%`, lalu diambil nilai tengahnya.
  - Kenapa perlu dibagi harga asli? Karena salah **Rp 300 ribu** pada *homestay* seharga Rp 500 ribu (meleset **60%**) terasa fatal bagi pemilik, sedangkan salah **Rp 300 ribu** pada vila Rp 3 juta (meleset **10%**) sangat wajar di pasar.

---

### Contoh Hitungan Mini (3 Properti Ilustratif) agar Langsung Nalar

Misalkan ada $N = 3$ unit diuji dengan hasil prediksi berikut:

| Properti | Tarif Asli ($y_i$) | Prediksi ($\widehat{y}_i$) | Selisih Mutlak ($\lvert y_i - \widehat{y}_i \rvert$) | Persentase Meleset ($\lvert y_i - \widehat{y}_i \rvert / y_i$) |
| :--- | ---: | ---: | ---: | ---: |
| 1. *Homestay* Budget | Rp 500.000 | Rp 550.000 | **Rp 50.000** | **10,0%** |
| 2. Vila Reguler | Rp 1.500.000 | Rp 1.350.000 | **Rp 150.000** | **10,0%** |
| 3. Vila Premium | Rp 8.000.000 | Rp 6.000.000 | **Rp 2.000.000** | **25,0%** |

- **MAE:** $(50.000 + 150.000 + 2.000.000) / 3 = \mathbf{\text{Rp } 733.333}$ (rata-rata ikut tertarik tinggi oleh vila no. 3).
- **RMSE:** $\sqrt{(50.000^2 + 150.000^2 + 2.000.000^2)/3} = \mathbf{\text{Rp } 1.158.303}$ (melonjak tajam karena $2.000.000^2$ sangat dominan).
- **MedAE:** nilai tengah dari `[Rp 50.000, Rp 150.000, Rp 2.000.000]` = **Rp 150.000** (menggambarkan akurasi wajar mayoritas properti).
- **MdAPE:** nilai tengah dari `[10,0%, 10,0%, 25,0%]` = **10,0%** (separuh unit meleset $\le 10\%$).

---

### Hasil Aktual Kelima Metrik pada Proyek Ini (196 Data Uji)

Nilai tercatat dari [model_benchmark_results.csv](../../aplikasi/reports/model_benchmark_results.csv):

| Model | CV $R^2$ (782 Unit) | Test $R^2$ (log) | Test MAE (IDR) | Test RMSE (IDR) | Test MedAE (IDR) | Test MdAPE (%) |
| :--- | :---: | :---: | ---: | ---: | ---: | :---: |
| **CatBoost Regressor** | **0,6636** | **0,6708** | **Rp 764.207** | **Rp 1.231.953** | **Rp 391.492** | 30,09% |
| **XGBoost Regressor** | 0,6631 | 0,6622 | Rp 773.730 | Rp 1.249.748 | Rp 411.693 | **27,61%** |
| **Random Forest (*Baseline*)** | 0,6291 | 0,6560 | Rp 809.098 | Rp 1.264.986 | Rp 470.400 | 31,63% |

**Cara membaca tabel hasil di atas secara praktis:**
1. **CatBoost paling akurat secara keseluruhan ($R^2$, MAE, RMSE, MedAE terbaik):** menjelaskan `67,08%` variasi harga di data uji, rata-rata meleset `Rp 764 ribu`, dan untuk separuh properti melesetnya hanya **`<= Rp 391 ribu`**.
2. **Kenapa semua model punya `RMSE` di atas Rp 1,2 juta?** Rincian per kelas di [tier_accuracy_breakdown.csv](../../aplikasi/reports/tier_accuracy_breakdown.csv) memperlihatkan pada segmen *Villa Reguler* (Rp 750 rb–2,5 jt, 89 unit), CatBoost sangat presisi (`MedAE Rp 306.870`, `MdAPE 24,84%`), tetapi pada segmen *Villa Premium* (Rp 6–10 jt, hanya 10 unit di data uji) rata-rata prediksi tertahan di Rp 4,35 jt terhadap aktual Rp 7,51 jt (`MAE Rp 3,23 juta`) sehingga mengangkat angka `RMSE` keseluruhan.
3. **XGBoost unggul tipis di `MdAPE` (`27,61%` vs `30,09%`):** pada properti bertarif rendah–menengah tertentu, persentase relatif unit tengah XGBoost lebih rapat 2,5 poin persen, walau dalam selisih Rupiah murni (`MAE`, `RMSE`, `MedAE`) dan proporsi varian ($R^2$) tetap diungguli CatBoost.
