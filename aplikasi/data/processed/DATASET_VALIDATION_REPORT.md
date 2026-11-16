# LAPORAN VALIDASI KUALITAS DATASET: BALI SMART PRICING
(Audit Integritas Data, Normalisasi Tarif 1 Malam, Validasi Geospasial, dan Kelayakan ML)

---

## 1. Ringkasan Eksekutif
* **Nama Dataset**: Bali Airbnb Enriched & Normalized Master Dataset
* **Total Unit Penginapan Unik (Pasar Reguler)**: **978 unit**
* **Total Fitur / Atribut**: **42 kolom**
* **Nilai Maksimum Ranjang (`beds`)**: **18 tempat tidur** (100% bebas cacat regex 96.036)
* **Status Kelayakan Pemodelan**: **VALID & BEBAS DATA LEAKAGE**

---

## 2. Audit Integritas & Kelengkapan Data (Missing Values)

| Nama Fitur | Jumlah Kosong (Null) | Persentase Kosong | Status Imputasi |
| :--- | :---: | :---: | :--- |
| `room_id` | 0 | 0.0% | Bersih (0%) |
| `name` | 0 | 0.0% | Bersih (0%) |
| `price_idr` | 0 | 0.0% | Bersih (0%) |
| `log_price` | 0 | 0.0% | Bersih (0%) |
| `rating` | 267 | 27.3% | Kosong Alami (Listing Baru; ditangani di pipeline) |
| `is_new_listing` | 0 | 0.0% | Bersih (0%) |
| `review_count` | 0 | 0.0% | Bersih (0%) |
| `is_room_only` | 0 | 0.0% | Bersih (0%) |
| `latitude` | 0 | 0.0% | Bersih (0%) |
| `longitude` | 0 | 0.0% | Bersih (0%) |
| `accommodates` | 0 | 0.0% | Bersih (0%) |
| `bedrooms` | 0 | 0.0% | Bersih (0%) |
| `beds` | 0 | 0.0% | Bersih (0%) |
| `bathrooms` | 0 | 0.0% | Bersih (0%) |
| `is_superhost` | 0 | 0.0% | Bersih (0%) |
| `has_self_checkin` | 0 | 0.0% | Bersih (0%) |
| `has_private_pool` | 0 | 0.0% | Bersih (0%) |
| `has_pool` | 0 | 0.0% | Bersih (0%) |
| `has_bathtub` | 0 | 0.0% | Bersih (0%) |
| `has_parking` | 0 | 0.0% | Bersih (0%) |
| `has_workspace` | 0 | 0.0% | Bersih (0%) |
| `nlp_luxury` | 0 | 0.0% | Bersih (0%) |
| `nlp_beach_ocean` | 0 | 0.0% | Bersih (0%) |
| `nlp_nature_view` | 0 | 0.0% | Bersih (0%) |
| `nlp_budget_cozy` | 0 | 0.0% | Bersih (0%) |
| `has_jacuzzi` | 0 | 0.0% | Bersih (0%) |
| `has_service_staff` | 0 | 0.0% | Bersih (0%) |
| `guests_per_bedroom` | 0 | 0.0% | Bersih (0%) |
| `baths_per_bedroom` | 0 | 0.0% | Bersih (0%) |
| `beds_per_bedroom` | 0 | 0.0% | Bersih (0%) |
| `total_rooms_index` | 0 | 0.0% | Bersih (0%) |
| `total_luxury_amenities` | 0 | 0.0% | Bersih (0%) |
| `dist_canggu_seminyak_km` | 0 | 0.0% | Bersih (0%) |
| `dist_ubud_center_km` | 0 | 0.0% | Bersih (0%) |
| `dist_uluwatu_km` | 0 | 0.0% | Bersih (0%) |
| `dist_sanur_km` | 0 | 0.0% | Bersih (0%) |
| `dist_kintamani_km` | 0 | 0.0% | Bersih (0%) |
| `dist_airport_km` | 0 | 0.0% | Bersih (0%) |
| `min_dist_tourism_hub_km` | 0 | 0.0% | Bersih (0%) |
| `regency` | 0 | 0.0% | Bersih (0%) |
| `sub_district` | 0 | 0.0% | Bersih (0%) |
| `property_type` | 0 | 0.0% | Bersih (0%) |

---

## 3. Analisis Statistik Target Variabel (Tarif Sewa Harian 1 Malam / `price_idr`)

* **Tarif Terendah (Min)**: Rp 154,358 / malam
* **Tarif Tertinggi (Max)**: Rp 9,786,094 / malam
* **Tarif Rata-Rata (Mean)**: Rp 2,064,199 / malam
* **Tarif Median (Nilai Tengah)**: Rp 1,470,000 / malam
* **Standar Deviasi**: Rp 1,820,809
* **Kuartil 1 (Q1)**: Rp 748,716 / malam
* **Kuartil 3 (Q3)**: Rp 2,771,936 / malam
* **Interquartile Range (IQR)**: Rp 2,023,220

---

## 4. Validasi Geospasial (Pulau Bali Bounding Box)
* **Listing dengan Koordinat Lengkap**: 978 dari 978 listing (100.0%)
* **Akurasi di Dalam Batas Wilayah Bali**: **100.0%**

---

## 5. Prevalensi Fasilitas & Sinyal Semantik NLP

| Fasilitas / Atribut | Persentase Listing | Keterangan |
| :--- | :---: | :--- |
| `is_new_listing` | **27.3%** | Fitur biner 1/0 |
| `is_room_only` | **26.1%** | Fitur biner 1/0 |
| `is_superhost` | **60.6%** | Fitur biner 1/0 |
| `has_self_checkin` | **47.4%** | Fitur biner 1/0 |
| `has_private_pool` | **38.2%** | Fitur biner 1/0 |
| `has_pool` | **82.8%** | Fitur biner 1/0 |
| `has_bathtub` | **49.4%** | Fitur biner 1/0 |
| `has_parking` | **91.6%** | Fitur biner 1/0 |
| `has_workspace` | **62.6%** | Fitur biner 1/0 |
| `nlp_luxury` | **15.6%** | Fitur biner 1/0 |
| `nlp_beach_ocean` | **32.8%** | Fitur biner 1/0 |
| `nlp_nature_view` | **39.3%** | Fitur biner 1/0 |
| `nlp_budget_cozy` | **3.8%** | Fitur biner 1/0 |
| `has_jacuzzi` | **5.2%** | Fitur biner 1/0 |
| `has_service_staff` | **10.3%** | Fitur biner 1/0 |
