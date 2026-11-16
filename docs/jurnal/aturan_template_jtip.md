# Spesifikasi & Aturan Baku Template Naskah JTIP-UNP
### Panduan Format Naskah Jurnal Teknologi Informasi dan Pendidikan (JTIP)
**Sumber Acuan**: Berkas Resmi `docs/jurnal/template_jtip.docx` (Revisi JTIP 2023 / Terbitan 2024)  
**Metode Analisis**: *Vision-First Visual Inspection* (Rendering PDF/PNG 150 DPI per Halaman) + *Deep XML/Style Dissection* via Python.

---

## 1. Metadata & Identitas Jurnal

| Elemen Header | Nilai Baku Template |
|---|---|
| **Nama Publikasi** | Jurnal Teknologi Informasi dan Pendidikan |
| **Penerbit / Afiliasi** | Fakultas Teknik, Universitas Negeri Padang (UNP) |
| **Identitas ISSN** | **P.ISSN**: 2086 – 4981 \| **E.ISSN**: 2620 – 6390 |
| **Portal Resmi** | `tip.ppj.unp.ac.id` |
| **DOI Pattern** | `https://doi.org/10.24036/jtip.v{vol}i{no}` |
| **Lisensi Terbitan** | Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0) |

---

## 2. Parameter Tata Letak Halaman (Page Layout)

Berdasarkan inspeksi visual dan ekstraksi properti section Word (`Section 0`):

* **Ukuran Kertas**: **A4 (Quarto)** — 21,59 cm × 27,94 cm (612 pt × 792 pt).
* **Format Kolom**: **1 Kolom Penuh (*Single Flat Left-Right Column*)**. Seluruh teks utama (Pendahuluan sampai Referensi) ditulis dalam format 1 kolom, bukan 2 kolom.
* **Margin Halaman**:
  * *Catatan Teknis Krusial*: Teks panduan di paragraf pendahuluan menyebut: *"The margin text from the left and top are 2 cm, right and bottom are 2 cm."* Namun, pada setup dokumen Word asli (`w:pgMar`), margin yang terpasang adalah:
    * **Top**: 2,00 cm (56,7 pt)
    * **Bottom**: 2,00 cm (56,7 pt)
    * **Left**: 3,00 cm (85,05 pt)
    * **Right**: 3,00 cm (85,05 pt)
    * **Header / Footer Distance**: 2,00 cm (56,7 pt)
  * *Rekomendasi Aman*: Tetap gunakan margin bawaan berkas template asli (Top 2 cm, Bottom 2 cm, Left 3 cm, Right 3 cm) agar tidak merusak layout visual bawaan redaksi.
* **Batasan Jumlah Halaman**:
  * **Original Research Article**: **Maksimum 15 halaman**.
  * **Review / Survey Paper**: **Maksimum 18 halaman**.
* **Spasi Paragraf**: *Single Space* (1,0) dengan spasi before 0 pt dan after 0 pt (kecuali pemisah heading).

---

## 3. Tipografi & Skema Warna Baku

Seluruh naskah JTIP menggunakan satu rumpun font tunggal: **Palatino Linotype**.  
Warna penanda aksen (*brand color*) JTIP pada judul dan heading adalah **Vivid Blue (`#0070C0`)**.

| Komponen Teks | Font Family | Ukuran | Gaya (*Style*) | Warna (*Hex*) | Perataan (*Alignment*) | Indentasi / Spasi |
|---|---|:---:|---|:---:|:---:|---|
| **Judul Artikel** | Palatino Linotype | **14 pt** | Bold | `#0070C0` | Center | Maksimal ~12 kata, spasi 1.0 |
| **Nama Penulis** | Palatino Linotype | **10 pt** | Bold | `#000000` | Center | Tanpa gelar, superskrip angka afiliasi & tanda bintang |
| **Afiliasi Penulis** | Palatino Linotype | **9 pt** | Regular | `#000000` | Center | Format: Unit/Lab, Prodi, Fakultas, Kampus, Kota, Negara |
| **Email Korespondensi** | Palatino Linotype | **9 pt** | Italic / Bold label | `#0070C0` | Center | `*Corresponding Author: email@domain` |
| **Kontak WhatsApp** | Palatino Linotype | **9 pt** | Italic | `#000000` | Center | Highlight kuning (`*deleted after publishing`) |
| **Header Kotak Abstrak** | Palatino Linotype | **10 pt** | Bold | `#0070C0` | Left | `Article Information` & `ABSTRACT (10pt)` |
| **Isi Abstrak** | Palatino Linotype | **10 pt** | Italic | `#000000` | Justify | 150 – 250 kata, *past tense*, tanpa sitasi |
| **Metadata Artikel** | Palatino Linotype | **9 pt** | Italic (label) | `#000000` | Left | History (Rec, Rev, Acc, Pub, Page) & Keywords |
| **How to Cite** | Palatino Linotype | **9 pt** | Regular (APA style) | `#000000` | Justify | Ditempatkan di baris bawah kotak abstrak |
| **Heading Utama (Lv 1)** | Palatino Linotype | **11 pt** | Bold (Kapital) | `#0070C0` | Left | Nomor urut: `1. INTRODUCTION`, `2. RESEARCH METHOD`, dst. |
| **Sub-Heading (Lv 2)** | Palatino Linotype | **11 pt** | Bold (Title Case) | `#0070C0` | Left | Format: `3.1. Sub-section 1` |
| **Sub-Sub-Heading (Lv 3)**| Palatino Linotype | **11 pt** | Bold (Title Case) | `#0070C0` | Left | Format: `3.2.1. Subsub section 1` |
| **Isi Paragraf (Body)** | Palatino Linotype | **11 pt** | Regular | `#000000` | Justify | First Line Indent: **36 pt (1,27 cm)**, Single Space |
| **Judul Tabel (Caption)** | Palatino Linotype | **10 pt** | Bold label + regular | `#000000` | Center | **Di ATAS** tabel, Sentence case: `Table 1. Deskripsi tabel` |
| **Isi Sel Tabel** | Palatino Linotype | **9–10 pt**| Regular | `#000000` | Center / Left | Three-line table, **tanpa garis vertikal** |
| **Judul Gambar (Caption)**| Palatino Linotype | **10 pt** | Bold label + regular | `#000000` | Center | **Di BAWAH** gambar: `Figure 1. Deskripsi gambar` |
| **Persamaan Matematika** | Palatino Linotype / Cambria Math | **11 pt** | Italic variabel | `#000000` | Center | Nomor `(1)` rata kanan (*flush right*) |
| **Daftar Pustaka** | Palatino Linotype | **9 pt** | Regular | `#000000` | Justify | IEEE Style, Hanging indent ~18–24 pt |

---

## 4. Anatomi & Struktur Standar IMRaD

Sesuai template revisi 2023, naskah mengikuti format baku IMRaD dengan nomor urut:

```text
Judul Makalah (14 pt, Bold, Vivid Blue #0070C0)
├── Penulis, Afiliasi, Email Korespondensi, Kontak HP
├── Kotak Informasi Artikel (Tabel 2 Kolom Borderless):
│   ├── Kolom Kiri: Article History & Keywords (5-7 kata)
│   └── Kolom Kanan: ABSTRACT (150-250 kata, 10 pt Italic)
├── How to Cite (Format APA) & Pernyataan Lisensi CC BY-SA 4.0
├── 1. INTRODUCTION (11 pt, Bold, #0070C0)
│   ├── 3 s.d. 6 Paragraf terstruktur
│   ├── Background, Problem Statement, Literature Review, Research Gap
│   └── Proposed Solution & Value of Innovation
├── [2. THE COMPREHENSIVE THEORETICAL BASIS AND PROPOSED METHOD/ALGORITHM] (Opsional)
├── 2. RESEARCH METHOD (11 pt, Bold, #0070C0)
│   ├── Desain dan Prosedur Penelitian (kronologis)
│   ├── Akuisisi & Preprocessing Data
│   ├── Rekayasa Fitur & Partisi Data
│   └── Perumusan Algoritma & Metrik Evaluasi
├── 3. RESULTS AND DISCUSSION (11 pt, Bold, #0070C0)
│   ├── 3.1. Sub-bagian Hasil & Benchmark Komparasi
│   ├── 3.2. Sub-bagian Pembahasan Terperinci & Analisis Galat
│   ├── 3.3. Sub-bagian Explainable AI (XAI) & Makna Bisnis
│   └── Integrasi Tabel & Gambar Beresolusi Tinggi
├── 4. CONCLUSION (11 pt, Bold, #0070C0)
│   ├── Pernyataan kesesuaian hasil dengan tujuan di Pendahuluan
│   └── Prospek pengembangan & riset lanjutan
├── ACKNOWLEDGEMENTS (11 pt, Bold, #0070C0 – Opsional)
└── REFERENCES (11 pt, Bold, #0070C0)
    └── Minimal 15 entri rujukan internasional terkini (IEEE Style, 9 pt)
```

---

## 5. Aturan Penulisan Elemen Spesifik

### 5.1 Judul Artikel (Title)
1. Ditulis seringkas dan seakurat mungkin: **maksimal sekitar 12 kata**.
2. **Dilarang keras memakai kata-kata pemborosan (*waste words*)**, seperti:
   - *"A study of..."* / *"Studi tentang..."*
   - *"Investigations of..."* / *"Investigasi terhadap..."*
   - *"Implementation of..."* / *"Implementasi sistem..."*
   - *"Analysis of..."* / *"Analisis perbandingan..."*
   - *"Design of..."* / *"Rancang bangun..."*
3. **Dilarang memakai singkatan atau akronim** dalam judul, kecuali jika naskah memang memperkenalkan metode/algoritma baru yang bernama singkatan tersebut.
4. Huruf awal setiap kata kapital (*Title Case*), rata tengah, 14 pt, Bold, warna `#0070C0`.

### 5.2 Abstrak & Kata Kunci
1. **Panjang Abstrak**: Antara **150 hingga 250 kata**.
2. **Bentuk Kalimat**: Wajib menggunakan bentuk lampau (*past tense*).
3. **Sifat Mandiri (*Stand-alone*)**: Abstrak harus dapat dipahami secara utuh tanpa membaca isi makalah.
4. **Dilarang mencantumkan sitasi rujukan** di dalam abstrak.
5. **Kata Kunci (*Keywords*)**: Maksimal **5 sampai 7 kata/frasa kunci**, menggunakan ejaan baku, hindari kata umum/jamak, pisahkan dengan baris titik/bullet kotak kecil (`▪`).

### 5.3 Bagian Pendahuluan (*Introduction*)
Template mewajibkan Pendahuluan ditulis dalam **3 sampai 6 paragraf** yang mencakup:
1. Latar belakang yang jelas (*clear background*).
2. Pernyataan masalah yang spesifik (*clear statement of the problem*).
3. Tinjauan literatur yang relevan (*relevant literature on the subject*).
4. Solusi atau pendekatan yang diusulkan (*proposed approach or solution*).
5. Nilai kebaruan / inovasi riset (*new value of research which is innovation*).

### 5.4 Penulisan Gambar (*Figures*)
1. Gambar disajikan **rata tengah (*Center*)**.
2. Resolusi wajib tajam (minimal 300 DPI), teks di dalam diagram/grafik harus terbaca jelas pada skala cetak.
3. Judul gambar (*caption*) diletakkan **di BAWAH gambar**.
4. Format caption:
   `Figure 1. The image title is written in Sentence case (initially in capital letters)`
   - Label `Figure 1.` dicetak **Tebal (Bold)**, diikuti tanda titik, spasi, lalu keterangan dalam *Sentence case* (10 pt).
5. Untuk gambar multi-bagian:
   - Diberikan sub-label `(a)`, `(b)` di bawah masing-masing gambar.
   - Caption induk di bawahnya menyebutkan kedua sub-bagian:  
     `Figure 2. Selectivity of model for (a) single tier, (b) multi-tier evaluation`
6. Seluruh gambar **wajib disitir secara eksplisit di dalam teks narasi** (contoh: *"...as shown in Figure 1..."*).

### 5.5 Penulisan Tabel (*Tables*)
1. Format tabel: **Tabel Tiga Garis (*Three-Line Table*)**:
   - Garis horizontal 1: Garis batas atas tabel.
   - Garis horizontal 2: Garis pemisah antara header kolom dengan data sel.
   - Garis horizontal 3: Garis batas penutup bawah tabel.
2. **DILARANG KERAS menggunakan garis vertikal (*No vertical borders*)**.
3. Tabel diletakkan **rata tengah (*Center*)**.
4. Judul tabel (*caption*) diletakkan **di ATAS tabel**.
5. Format caption:
   `Table 1. The performance of benchmark models`
   - Label `Table 1.` dicetak **Tebal (Bold)**, diikuti tanda titik, spasi, lalu kalimat deskriptif dalam *Sentence case* (10 pt).
6. Seluruh tabel **wajib disitir di dalam teks** (contoh: *"...listed in Table 1..."*).

### 5.6 Persamaan Matematika (*Equations*)
1. Persamaan diletakkan **rata tengah (*Center-aligned*)**.
2. Nomor urut persamaan ditaruh di dalam tanda kurung dan **rata kanan margin (*Flushed to the right margin*)**:
   $$E_v - E = \frac{h}{2m} (k_x^2 + k_y^2) \qquad (1)$$
3. Wajib dibuat menggunakan Microsoft Equation Editor atau MathType (bukan gambar bitmap/screenshot).
4. Setiap variabel dan simbol yang muncul pada persamaan wajib didefinisikan secara eksplisit pada paragraf sesudahnya.

### 5.7 Sitasi & Daftar Pustaka (*References*)
1. **Format Sitasi Teks**: Standar **IEEE Style** menggunakan nomor dalam kurung siku:
   - Contoh tunggal: `[1]`, `[2]`.
   - Contoh majemuk: `[5]–[7]`, `[14], [15]`.
   - Jika diletakkan di awal kalimat: `"Ref [18] showed that..."`.
2. **Aturan Penulis**:
   - Jika penulis berjumlah hingga 6 orang: cantumkan seluruh nama penulis.
   - Jika penulis lebih dari 6 orang: tulis nama penulis pertama diikuti `et al.` (contoh: `J. D. Bellamy et al.`).
3. **Persyaratan Jumlah & Kualitas Referensi**:
   - **Minimal 15 entri referensi** untuk naskah penelitian asli (*original research paper*).
   - Diutamakan bersumber dari jurnal dan prosiding internasional terkini (5–10 tahun terakhir).
   - Dianjurkan menggunakan manajer referensi (Mendeley, Zotero, atau EndNote) dengan gaya sitasi IEEE.
4. **Tipografi Daftar Pustaka**: Font Palatino Linotype **9 pt**, spasi 1.0, rata kiri-kanan (*justify*).
5. **Format Entri**:
   - **Artikel Jurnal**:  
     `[1] J. K. Author, "Title of paper," Abbrev. Title of Periodical, vol. x, no. x, pp. xxx–xxx, Month, year, doi: xxx.`
   - **Prosiding Konferensi**:  
     `[2] J. K. Author, "Title of paper," in Abbreviated Name of Conf., year, pp. xxx–xxx, doi: xxx.`
   - **Buku**:  
     `[3] J. K. Author, Title of Published Book, xth ed. City of Publisher: Abbrev. of Publisher, year.`
   - **Tesis / Disertasi**:  
     `[4] J. K. Author, "Title of thesis," M.S. thesis, Dept., Univ., City, State, year.`
