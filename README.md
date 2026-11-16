# Bali Smart Pricing Engine
### Sistem Rekomendasi Tarif Sewa Harian Villa dan Homestay di Bali Berbasis Machine Learning & Explainable AI

Disusun oleh:
* **I Kadek Adi Sunetra** (NIM: 2305551053)
* **Anthony Wisnu Jati** (NIM: 2305551138)

Program Studi Teknologi Informasi, Fakultas Teknik, Universitas Udayana  
Dosen Pengampu: **Yogiswara Dharma Putra, S.TI., M.T.**

---

## Navigasi Cepat Proyek

| Keperluan | Lokasi Berkas |
|---|---|
| **Menjalankan Aplikasi Web Streamlit** | `.\aplikasi\run_app.bat` (`http://localhost:8501`) |
| **Naskah Jurnal Ilmiah (JTIP Section 1–2 + 23 Rujukan)** | [DOCX](docs/jurnal/jurnal_bali_smart_pricing.docx) · [PDF](docs/jurnal/jurnal_bali_smart_pricing.pdf) · [Template](docs/jurnal/template_jtip.docx) |
| **Peta Lengkap Rumus & Audit Sitasi (23/23 PDF, 52 Kutipan)** | [Peta Semua Rumus](docs/jurnal/peta_semua_rumus_jurnal.md) · [Matriks Audit](docs/jurnal/audit_sitasi_dan_rujukan.md) · [PDF Berstabilo](docs/penelitian/rujukan_berstabilo/) |
| **Panduan Pemahaman Sistem & Tanya Jawab** | [Quickstart](docs/panduan/quickstart.md) · [Bedah Model & Metrik](docs/panduan/bedah-model-dan-metrik.md) |
| **Diagram Alur, Validasi Silang, & Peta Spasial** | [Alur Penelitian](docs/diagram/alur-penelitian.png) · [Validasi Model](docs/diagram/arsitektur-validasi-model.png) · [Peta Spasial & Log](docs/diagram/peta-distribusi-dan-log-harga.png) |
| **Audit Validasi Kualitas Dataset (978 Unit)** | [DATASET_VALIDATION_REPORT.md](aplikasi/data/processed/DATASET_VALIDATION_REPORT.md) |
| **Arsip Proposal Laporan & Presentasi Awal** | [Laporan](docs/laporan/laporan.md) · [Presentasi](docs/presentasi/naskah.md) |

> **Status Naskah Jurnal**: **Bagian 1 (`1. INTRODUCTION`)**, **Bagian 2 (`2. RESEARCH METHOD`)**, **`ABSTRACT`**, serta **`REFERENCES` (`[1]–[23]` terverifikasi kronologis dan teraudit verbatim)** telah selesai di [`docs/jurnal/jurnal_bali_smart_pricing.docx`](docs/jurnal/jurnal_bali_smart_pricing.docx), siap dilanjutkan ke Bagian 3 (*Results and Discussion*) dan Bagian 4 (*Conclusion*).

---

## Struktur Repositori

```text
├── aplikasi/                  # Pipeline Machine Learning & Antarmuka Web Streamlit
│   ├── app.py                 # Dashboard interaktif Streamlit (4 tab utama)
│   ├── requirements.txt       # Dependensi Python aplikasi ML
│   ├── run_app.bat            # Peluncur web dashboard (localhost:8501)
│   ├── run_pipeline.bat       # Eksekutor pipeline 02 s.d. 06
│   ├── data/
│   │   ├── raw/               # Dataset awal (1.235 baris, 6 kolom)
│   │   ├── scraped/           # Cache JSON per listing (1.036 berkas)
│   │   └── processed/         # Master bersih (978 baris, 42 kolom) & split train/test
│   ├── models/                # Model juara terlatih (CatBoost .cbm) & metadata fitur
│   ├── reports/               # CSV benchmark model, akurasi segmen, & grafik SHAP
│   └── scripts/               # Pipeline 01 (scrape), 02 (merge), 03 (clean), 04 (train), 05 (SHAP), 06 (audit)
├── docs/
│   ├── diagram/               # Bagan alur penelitian, arsitektur validasi, & peta spasial/log
│   ├── jurnal/                # Naskah JTIP (.docx/.pdf), template, audit sitasi, & peta rumus
│   ├── laporan/               # Arsip laporan tugas besar & aset tangkapan layar
│   ├── panduan/               # Quickstart penguasaan & bedah matematis metrik
│   ├── penelitian/            # 23 PDF rujukan asli (01..23) & PDF berstabilo verbatim
│   └── presentasi/            # Arsip naskah slide & ekspor PPTX/PDF
├── .gitignore
├── LICENSE
└── README.md
```

---

## Ringkasan Data & Benchmark Model (Terverifikasi)

Pipeline memisahkan data uji secara terisolasi sebelum fitting (**0% Data Leakage**) dan menjaga nilai `rating` kosong alami pada unit baru (**cold-start**, ditandai `is_new_listing`) tanpa imputasi global sebelum split:

* **Kurasi Data**: `1.235` baris mentah &rarr; `1.058` listing unik (`-177` duplikat `room_id`) &rarr; `1.036` unit berkoordinat GPS (`-22` tanpa lat/lon) &rarr; **`978` unit pasar reguler** (`-58` tarif ekstrem `< Rp 150 ribu`, `> Rp 10 juta`, atau `> Rp 4 juta/kamar`) di seluruh **`54` kecamatan resmi** dan **`9` kabupaten/kota Bali**, mencakup `402` koreksi batas kabupaten, `73` rekonsiliasi kapasitas kamar, dan `267` unit baru tanpa ulasan (`27,3%`, `rating = NaN`).
* **Partisi Terisolasi (`80:20`)**: **`782` data latih** (5-Fold CV) dan **`196` data uji holdout**.
* **Fitur Prediktor Murni**: **`38` fitur** (`35` fitur numerik/biner fisik, fasilitas, semantik judul, & jarak Haversine + `3` kategori nominal: `regency`, `sub_district`, `property_type`).

| Model | 5-Fold CV $R^2$ | Test $R^2$ | Test MAE (IDR) | Test MedAE (IDR) | Test RMSE (IDR) | Test MdAPE |
|---| :---: | :---: | :---: | :---: | :---: | :---: |
| **CatBoost Regressor (Champion)** | **0,6636** | **0,6708** | **Rp 764.207** | **Rp 391.492** | **Rp 1.231.953** | 30,09% |
| **XGBoost Regressor** | 0,6631 | 0,6622 | Rp 773.730 | Rp 411.693 | Rp 1.249.748 | **27,61%** |
| **Random Forest (Baseline)** | 0,6291 | 0,6560 | Rp 809.098 | Rp 470.400 | Rp 1.264.986 | 31,63% |

* **Segmen Terbesar (`Villa Reguler`, `89` dari `196` data uji)**: CatBoost mencapai **MedAE `Rp 306.870`** dengan **MdAPE `24,84%`** (akurasi relatif median **`75,16%`**).
* **Explainable AI (XAI)**: Kontribusi fitur lokal & global dihitung menggunakan `SHAP TreeExplainer`.

---

## Cara Menjalankan

```powershell
# 1. Jalankan dashboard interaktif Streamlit
.\aplikasi\run_app.bat

# 2. (Opsional) Jalankan ulang pipeline 02..06 dengan Python venv terisolasi
.\aplikasi\run_pipeline.bat
```
