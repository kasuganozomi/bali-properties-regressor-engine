# Peta Lengkap Semua Rumus di Naskah Jurnal

Dokumen ini memetakan **seluruh rumus yang tercantum pada [JURNAL_FINAL.md](JURNAL_FINAL.md)** (*2 blok alur dimensi fitur di Subbab 2.5* dan *5 persamaan matematis bernomor `Equation (1)`–`Equation (5)`*, dilengkapi definisi 3 metrik pembanding standar $R^2$, MAE, dan RMSE yang diacu pada Subbab 2.6), lengkap dengan arti tiap simbol, alasan pemakaiannya, contoh hitungan nyata, dan posisi implementasinya di kode Python proyek.

---

## 1. Peta Cepat Seluruh Rumus

| No | Nama Rumus | Letak di `JURNAL_FINAL` | Jenis | Fungsi Inti | Sumber Kode Python |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **F1** | Jalur Pra-Pemrosesan RF & XGBoost (`38 → 101`) | Subbab 2.5 | Alur Fitur | Menambal `rating` kosong pakai median lalu memekarkan 3 kolom teks menjadi 66 kolom biner `dummy` (`66 + 35 = 101`) | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L62-L69) |
| **F2** | Jalur Pra-Pemrosesan CatBoost (`38 → 38`) | Subbab 2.5 | Alur Fitur | Mengolah 3 kolom kategori via *ordered target statistics* dan membiarkan `NaN` asli di percabangan pohon | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L135-L138) |
| **(1)** | Jarak Haversine ($d_{i,h}$) | Subbab 2.4, Eq. (1) | Matematis | Menghitung jarak fisik permukaan bumi (km) dari koordinat unit ke 6 titik wisata/bandara Bali | [03_preprocess_and_clean.py](../../aplikasi/scripts/03_preprocess_and_clean.py#L43-L49) |
| **(2)** | Transformasi Logaritmik ($y_i^{(\log)}$) | Subbab 2.4, Eq. (2) | Matematis | Mengecilkan skala harga Rupiah sebelum model dilatih agar vila mahal tidak mendominasi bobot | [03_preprocess_and_clean.py](../../aplikasi/scripts/03_preprocess_and_clean.py#L104) |
| **(3)** | Eksponensial Balik ($\widehat{y}_i$) | Subbab 2.6, Eq. (3) | Matematis | Mengembalikan prediksi skala log ke Rupiah asli agar selisih harga terbaca langsung | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L74-L75) |
| **(4)** | *Median Absolute Error* (MedAE) | Subbab 2.6, Eq. (4) | Metrik (IDR) | Nilai tengah selisih Rupiah; menunjukkan akurasi tipikal mayoritas unit tanpa bias vila ekstrem | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L78) |
| **(5)** | *Median Absolute Percentage Error* (MdAPE) | Subbab 2.6, Eq. (5) | Metrik (%) | Nilai tengah persentase meleset relatif terhadap tarif asli properti | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L79) |
| **S1–S3** | Metrik Pembanding Standar ($R^2$, MAE, RMSE) | Subbab 2.6 (teks) | Metrik Standar | Mengukur proporsi variansi skala log ($R^2$), rata-rata selisih Rupiah (MAE), dan penalti kuadrat pencilan (RMSE) | [04_train_and_benchmark_models.py](../../aplikasi/scripts/04_train_and_benchmark_models.py#L73-L77) |

---

## 2. Kelompok A — Alur Kolom & Jalur Pra-Pemrosesan Model (`F1–F2`)

Sebelum memasuki pemodelan, data awal Kaggle (`6` kolom) diperkaya menjadi `30` kolom pada Subbab 2.2 (`+24` kolom: `room_id`, lokasi & tipe, kapasitas, status operasi, `7` fasilitas biner, dan `4` kata kunci teks), lalu pada Subbab 2.4 kolom `url` dibuang (`-1`) dan ditambahkan `12` fitur rekayasa plus `1` target logaritmik (`+13`) menjadi `42` kolom akhir (`4` nonprediktor: `room_id, name, price_idr, log_price` dan `38` fitur prediktor $X$).

### F1 vs F2. Kedua Jalur Pra-Pemrosesan Model (Subbab 2.5)

Kedua baris blok rumus di Subbab 2.5 menjelaskan **perlakuan berbeda** terhadap input $X$ yang sama persis (`38` fitur: **3 kolom teks kategori** + **35 kolom angka**):

#### Jalur F1 (Random Forest & XGBoost)
$$38\text{ Fitur } X \longrightarrow \text{SimpleImputer (median)} + \text{One-Hot Encoding (66 Dummy)} + 35\text{ Numerik} \longrightarrow 101\text{ Fitur (RF \& XGB)}$$

- **Apa artinya:**
  1. **Untuk 35 kolom angka:** `SimpleImputer(strategy="median")` menambal kolom `rating` yang kosong (`NaN` pada 267 unit baru) dengan nilai tengah data latih (**4,95**), supaya tidak dianggap `0` atau membuat model lama error. Kolom angka lain tidak ada yang kosong.
  2. **Untuk 3 kolom teks (`regency`, `sub_district`, `property_type`):** `OneHotEncoder` memecah setiap nama unik menjadi 1 kolom sakelar `1/0` (*dummy*):
     - `regency`: `9` kabupaten/kota di data latih $\to$ `9` kolom.
     - `sub_district`: `53` kecamatan muncul di `782` data latih $\to$ `53` kolom. *(Kecamatan `Kuta Selatan` kebetulan hanya jatuh ke `196` data uji; aturan `handle_unknown="ignore"` membuatnya aman bernilai `0` di seluruh `53` kolom kecamatan tanpa crash dan tanpa kebocoran data uji).*
     - `property_type`: `4` jenis properti $\to$ `4` kolom.
  3. **Hasil total:** $(9 + 53 + 4) + 35 = 66 + 35 = 101\text{ fitur angka}$.

#### Jalur F2 (CatBoost Regressor)
$$38\text{ Fitur } X \longrightarrow \text{Ordered Target Statistics (3 Kategori)} + \text{NaN Native} \longrightarrow 38\text{ Fitur (CatBoost)}$$

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

## 4. Kelompok C — Metrik Evaluasi (`Equation (4)–(5)` dan Metrik Standar `S1–S3`)

Pada `Equation (4)–(5)` serta metrik pembanding standar ($R^2$, MAE, RMSE) di Subbab 2.6: $N$ adalah jumlah unit evaluasi ($N = 196$ di data uji terpisah, $N = 782$ di validasi silang *out-of-fold*), $y_i$ adalah harga asli (IDR), $\widehat{y}_i$ adalah harga prediksi (IDR) hasil Equation (3), dan $y_i^{(\log)}, \widehat{y}_i^{(\log)}, \bar{y}^{(\log)}$ adalah nilai asli, prediksi, dan rata-rata pada skala logaritma.

### Equation (4) & Equation (5) — Akurasi Unit Tipikal (`MedAE`) dan Persentase Relatif (`MdAPE`)

$$\text{MedAE} = \text{median}\left(\left|y_i - \widehat{y}_i\right|\right) \qquad\qquad \text{MdAPE} = \text{median}\left(\frac{\left|y_i - \widehat{y}_i\right|}{y_i}\right) \times 100\%$$

- **Kenapa kedua persamaan ini ditampilkan formal di `JURNAL_FINAL`?** Karena sebaran tarif Bali miring tajam dan rata-rata (`MAE`) gampang tertarik naik oleh 5% vila mewah bertarif Rp 6–10 juta yang selisih prediksinya jutaan rupiah.
- **Equation (4) — MedAE:** mengurutkan seluruh selisih $|y_i - \widehat{y}_i|$ dari paling kecil ke paling besar, lalu mengambil **angka tepat di posisi tengah (persentil ke-50)**. Pada CatBoost (`MedAE = Rp 391.492`), **separuh dari 196 properti uji** (`98` unit) prediksinya meleset **$\le$ Rp 391.492**.
- **Equation (5) — MdAPE:** selisih Rupiah tiap properti dibagi dulu dengan **harga aslinya** ($y_i$), dikali `100%`, lalu diambil nilai tengahnya. Pembagian terhadap $y_i$ membedakan galat Rp 300 ribu pada *homestay* Rp 500 ribu (`60%`) dibanding vila Rp 3 juta (`10%`).

---

### Metrik Pembanding Standar (`S1–S3` — Dirujuk pada Teks Subbab 2.6)

Ketiga metrik baku berikut dihitung di kode proyek dan dirujuk perannya secara ringkas pada Subbab 2.6:

- **S1 — Koefisien Determinasi ($R^2$ pada skala `log_price`):**
  $$R^2 = 1 - \frac{\sum_{i=1}^{N}\left(y_i^{(\log)} - \widehat{y}_i^{(\log)}\right)^2}{\sum_{i=1}^{N}\left(y_i^{(\log)} - \bar{y}^{(\log)}\right)^2}$$
  Mengukur proporsi variansi harga logaritmik yang dijelaskan model dibanding menebak rata-rata polos $\bar{y}^{(\log)}$. CatBoost meraih $R^2 = \mathbf{0{,}6708}$ (`67,08%` variasi harga terjawab oleh 38 fitur).
- **S2 — MAE & S3 — RMSE (pada skala Rupiah hasil Equation (3)):**
  $$\text{MAE} = \frac{1}{N}\sum_{i=1}^{N}\left|y_i - \widehat{y}_i\right| \qquad\qquad \text{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^{N}\left(y_i - \widehat{y}_i\right)^2}$$
  `MAE` mengambil rata-rata mutlak selisih Rupiah secara setara, sedangkan `RMSE` menguadratkan selisih sehingga kesalahan besar pada 10 vila premium (`MAE = Rp 3,23 juta`) mendongkrak `RMSE` global ke `Rp 1.231.953`.

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
