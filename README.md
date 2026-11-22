# Bali Smart Pricing Engine
### Prediksi Tarif Sewa Harian Villa dan Homestay di Bali Menggunakan CatBoost, XGBoost, dan Explainable AI

Disusun oleh:
* **I Kadek Adi Sunetra** (NIM: 2305551053)
* **Anthony Wisnu Jati** (NIM: 2305551138)

Program Studi Teknologi Informasi, Fakultas Teknik, Universitas Udayana  
Dosen Pengampu: **Yogiswara Dharma Putra, S.TI., M.T.**

---

## Navigasi Cepat Deliverables Final

Seluruh keluaran akademik proyek ini menggunakan satu sumber aset visual bersama pada [`docs/assets/`](docs/assets/) dan satu daftar 23 rujukan IEEE terverifikasi verbatim (`[1]–[23]`) pada [`docs/penelitian/`](docs/penelitian/).

| Deliverable | Berkas Final | Keterangan |
|---|---|---|
| **Aplikasi Web Interaktif** | `.\aplikasi\run_app.bat` (`http://localhost:8501`) | Streamlit 4 tab: Kalkulator + What-If, Peta 978 Unit, Benchmark 3 Model, & SHAP |
| **Jurnal Ilmiah (JTIP-UNP)** | [JURNAL_FINAL.docx](docs/jurnal/JURNAL_FINAL.docx) · [JURNAL_FINAL.pdf](docs/jurnal/JURNAL_FINAL.pdf) · [JURNAL_FINAL.md](docs/jurnal/JURNAL_FINAL.md) | Naskah utuh Bagian 1–4 + 23 rujukan IEEE (15 halaman, sesuai batas JTIP) |
| **Laporan Tugas Besar** | [LAPORAN_FINAL.docx](docs/laporan/LAPORAN_FINAL.docx) · [LAPORAN_FINAL.pdf](docs/laporan/LAPORAN_FINAL.pdf) · [LAPORAN_FINAL.md](docs/laporan/LAPORAN_FINAL.md) | Laporan lengkap Bab I–V, 7 tabel, 11 gambar + tangkapan layar aplikasi, & 23 rujukan identik |
| **Presentasi Hasil Akhir** | [PRESENTASI_FINAL.pptx](docs/presentasi/PRESENTASI_FINAL.pptx) · [PRESENTASI_FINAL.pdf](docs/presentasi/PRESENTASI_FINAL.pdf) · [PRESENTASI_FINAL.md](docs/presentasi/PRESENTASI_FINAL.md) | Dek presentasi 15 slide (16:9) visual bersih dengan alur kronologis, *Speaker Notes*, & font tersemat |
| **Audit Rumus & 23 Rujukan** | [Peta Semua Rumus](docs/jurnal/peta_semua_rumus_jurnal.md) · [Audit Sitasi](docs/jurnal/audit_sitasi_dan_rujukan.md) · [PDF Berstabilo](docs/penelitian/rujukan_berstabilo/) | 23/23 PDF rujukan asli beserta 52 kutipan verbatim berstabilo |
| **Aset Visual Bersama** | [Alur Penelitian](docs/assets/alur-penelitian.png) · [Validasi Model](docs/assets/arsitektur-validasi-model.png) · [Peta & Log](docs/assets/peta-distribusi-dan-log-harga.png) · [Evaluasi & Segmen](docs/assets/evaluasi-prediksi-dan-segmen.png) · [SHAP](docs/assets/interpretabilitas-shap.png) | Diagram, grafik 300 DPI, & tangkapan layar aplikasi dipakai bersama Jurnal, Laporan, dan Presentasi |
| **Audit Kualitas Dataset** | [DATASET_VALIDATION_REPORT.md](aplikasi/data/processed/DATASET_VALIDATION_REPORT.md) | Audit kurasi 1.235 baris mentah &rarr; 978 unit bersih (54 kecamatan, 38 fitur) |

---

## Struktur Repositori

```text
├── aplikasi/                  # Pipeline Machine Learning & Antarmuka Web Streamlit
│   ├── app.py                 # Dashboard interaktif Streamlit (4 tab utama)
│   ├── requirements.txt       # Dependensi Python aplikasi ML
│   ├── run_app.bat            # Peluncur web dashboard (localhost:8501)
│   ├── run_pipeline.bat       # Eksekutor pipeline 02 s.d. 06
│   ├── data/
│   │   ├── raw/               # Dataset awal Kaggle (1.235 baris, 6 kolom)
│   │   ├── scraped/           # Cache JSON per listing (1.036 berkas)
│   │   └── processed/         # Master bersih (978 baris, 42 kolom) & split 80:20
│   ├── models/                # Model terbaik CatBoost (.cbm, 726 KiB) & metadata fitur
│   ├── reports/               # CSV benchmark model, akurasi segmen, & grafik SHAP
│   └── scripts/               # Pipeline 01 (scrape), 02 (merge), 03 (clean), 04 (train), 05 (SHAP), 06 (audit)
├── docs/
│   ├── assets/                # Sumber tunggal diagram, grafik 300 DPI, & tangkapan layar aplikasi
│   ├── jurnal/                # JURNAL_FINAL (.docx/.pdf/.md), template JTIP, peta rumus, & audit sitasi
│   ├── laporan/               # LAPORAN_FINAL (.docx/.pdf/.md)
│   ├── penelitian/            # 23 PDF rujukan asli (01..23) & 23 PDF berstabilo verbatim
│   └── presentasi/            # PRESENTASI_FINAL (.pptx/.pdf/.md — 15 slide)
├── .gitignore
├── LICENSE
└── README.md
```

---

## Ringkasan Data & Benchmark Model (Terverifikasi)

Pipeline memisahkan data uji secara terpisah sejak awal sebelum pelatihan (**0% Data Leakage**) dan menjaga nilai `rating` kosong alami pada unit baru (**cold-start**, ditandai `is_new_listing = 1`) tanpa imputasi global sebelum split:

* **Kurasi Data**: `1.235` baris mentah &rarr; `1.058` listing unik (`-177` duplikat `room_id`) &rarr; `1.036` unit berkoordinat GPS (`-22` tanpa lat/lon) &rarr; **`978` unit pasar reguler** (`-58` tarif ekstrem `< Rp 150 ribu`, `> Rp 10 juta`, atau `> Rp 4 juta/kamar`) pada **`54` kecamatan resmi** dan **`9` kabupaten/kota Bali**, mencakup `402` koreksi batas kabupaten (`SUBDISTRICT_MAP`), `73` rekonsiliasi kapasitas kamar, dan `267` unit baru tanpa ulasan (`27,3%`, `rating = NaN`).
* **Pembagian Data (`80:20`)**: **`782` data latih** (5-Fold CV) dan **`196` data uji terpisah** (*holdout*).
* **Fitur Prediktor Murni**: **`38` fitur** (`10` struktur & rasio kapasitas, `11` lokasi & 7 jarak Haversine, `8` fasilitas & skor kemewahan 0–5, `9` reputasi, operasi, & 4 sinyal teks).

| Model | 5-Fold CV $R^2$ | CV MAE (IDR) | Test $R^2$ (log) | Test MAE (IDR) | Test RMSE (IDR) | Test MedAE (IDR) | Test MdAPE |
|---| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CatBoost Regressor (Champion)** | **0,6636** | Rp 717.074 | **0,6708** | **Rp 764.207** | **Rp 1.231.953** | **Rp 391.492** | 30,09% |
| **XGBoost Regressor** | 0,6631 | **Rp 714.995** | 0,6622 | Rp 773.730 | Rp 1.249.748 | Rp 411.693 | **27,61%** |
| **Random Forest (Baseline)** | 0,6291 | Rp 737.098 | 0,6560 | Rp 809.098 | Rp 1.264.986 | Rp 470.400 | 31,63% |

* **Segmen Terbesar (`Villa Reguler`, Rp 750 rb–2,5 jt, `n = 89` / `45,4%` data uji)**: CatBoost mencapai rata-rata prediksi `Rp 1.456.611` (aktual `Rp 1.467.322`), **MedAE `Rp 306.870`**, dan **MdAPE `24,84%`**.
* **Ketahanan Cold-Start (`63` unit baru, `rating = NaN`, `review_count = 0`)**: CatBoost mencapai **MedAE `Rp 295.685`** dan **MdAPE `29,07%`** (sebanding dengan 133 unit berulasan: `MdAPE 30,10%`).
* **Explainable AI (SHAP TreeExplainer)**: Pendorong tarif teratas adalah `property_type` (`0,183`), `bedrooms` (`0,134`), `has_bathtub` (`0,101`), `total_luxury_amenities` (`0,099`), `total_rooms_index` (`0,068`), dan `sub_district` (`0,067`).

---

## Cara Menjalankan

```powershell
# 1. Jalankan dashboard interaktif Streamlit
.\aplikasi\run_app.bat

# 2. (Opsional) Jalankan ulang pipeline 02..06 dengan Python venv terisolasi
.\aplikasi\run_pipeline.bat
```
