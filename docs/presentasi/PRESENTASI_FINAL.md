# Bali Smart Pricing Engine
**Sistem Rekomendasi Tarif Sewa Harian Villa dan Homestay di Bali Berbasis Machine Learning & Explainable AI**

Presentasi Hasil Akhir — Tugas Besar Pembelajaran Mesin  
**I Kadek Adi Sunetra** · 2305551053  
**Anthony Wisnu Jati** · 2305551138  
Program Studi Teknologi Informasi · Fakultas Teknik · Universitas Udayana (2026)  
Dosen Pengampu: **Yogiswara Dharma Putra, S.TI., M.T.**

> Dek presentasi ini terdiri dari **12 slide (16:9)** berdurasi sekitar **8–10 menit**. Disusun dengan alur cerita (*storytelling*) yang mengalir dari masalah nyata pemilik penginapan, skenario kasus di Ubud, proses data dan pengujian model, hasil akurasi dan alasan harga (SHAP), hingga demo langsung aplikasi web yang menjawab skenario di awal. Naskah pada setiap slide di bawah ini adalah **narasi lisan siap ucap** yang sekaligus tertanam di *Speaker Notes* `PRESENTASI_FINAL.pptx`.

---

## Slide 1 — Sampul

*Slide 1*

Selamat pagi/siang Bapak dosen dan rekan-rekan sekalian. Perkenalkan, kami I Kadek Adi Sunetra dan Anthony Wisnu Jati dari Program Studi Teknologi Informasi Universitas Udayana. Hari ini kami akan memaparkan hasil akhir tugas besar Pembelajaran Mesin kami yang berjudul **Bali Smart Pricing Engine**, yaitu sistem rekomendasi tarif sewa harian untuk vila dan *homestay* di Bali berbasis *Machine Learning* dan *Explainable AI*.

---

## Slide 2 — Masalah Nyata di Lapangan

*Slide 2*

Penelitian ini berangkat dari persoalan yang sangat dekat dengan keseharian pariwisata Bali. Hingga akhir tahun 2025, jumlah akomodasi terdaftar di Bali sudah menembus lebih dari 17.500 unit—sebagian besar berupa vila privat dan *homestay* yang dikelola mandiri oleh masyarakat lokal. Di tengah persaingan sepadat ini, menentukan harga sewa per malam itu krusial: kalau dipasang terlalu mahal, tamu langsung pindah ke tempat lain; tapi kalau terlalu murah, pemasukannya tidak cukup menutup biaya listrik, air, dan perawatan harian.

Masalahnya, sebagian besar pengelola masih menentukan tarif dengan menebak sendiri atau sekadar menyamakan harga dengan penginapan tetangga. Padahal dua properti di desa yang sama bisa punya nilai jual yang jauh berbeda kalau kapasitas kamar, kolam renang, atau jaraknya ke pusat wisata berbeda. Memantau harga manual di situs seperti Airbnb pun menyita waktu dan sering mengecoh karena harga yang muncul di halaman depan belum tentu tarif murni untuk satu malam.

---

## Slide 3 — Skenario Nyata: Pemilik Vila di Ubud

*Slide 3*

Supaya lebih kebayang, coba kita lihat satu contoh kasus nyata. Bayangkan seorang pemilik mengelola vila dua kamar tidur di Ubud, Gianyar. Kapasitasnya untuk 4 tamu, punya 2 kamar mandi, kolam renang pribadi, *bathtub*, ruang kerja, parkir gratis, dan pemandangan sawah.

Pertanyaannya sederhana: **berapa harga per malam yang wajar untuk vila seperti ini—baik saat sudah berjalan dengan ulasan tamu, maupun jika kondisinya baru buka dan belum punya ulasan sama sekali?** Kalau pemilik hanya meniru vila sebelah, belum tentu fasilitasnya sama. Kalau memakai model berbasis analisis ulasan tamu, model itu langsung buntu untuk unit yang baru buka. Pertanyaan inilah yang ingin kita jawab—dan nanti di akhir presentasi, kita akan melihat langsung jawaban aplikasi web kami untuk vila Ubud ini.

---

## Slide 4 — Tujuan & Gambaran Besar Solusi

*Slide 4*

Dari masalah tadi, tujuan kami sederhana dan jelas pada tiga hal:
1. Membantu pemilik vila dan *homestay* di Bali mendapatkan patokan tarif harian yang masuk akal sesuai fisik, fasilitas, dan lokasi propertinya.
2. Melengkapi dan membenahi kualitas data katalog daring awal supaya cukup akurat untuk dipakai melatih model.
3. Membangun dan menguji model prediksi yang tidak hanya tepat—termasuk untuk properti baru tanpa ulasan—tetapi juga bisa menjelaskan *kenapa* harga tersebut direkomendasikan.

Alur besar sistemnya lugas: pemilik cukup memasukkan spesifikasi properti mereka, model *machine learning* memprosesnya, lalu keluar rekomendasi tarif per malam lengkap dengan rentang pasar wajar dan alasan faktor penentunya.

---

## Slide 5 — Dari Data Awal ke Data Siap Pakai

*Slide 5*

Tantangan pertama kami ada di data. Dataset awal Airbnb Bali dari Kaggle berisi 1.235 baris, tetapi hanya punya 6 kolom dasar—belum ada jumlah kamar, tidak ada koordinat lokasi, tidak ada daftar fasilitas, dan tarifnya masih tercampur paket 5 malam bawaan halaman pencarian.

Karena itu, kami mengambil rincian asli langsung dari halaman masing-masing properti dan memverifikasi tarif satu malam murni. Setelah duplikat, unit tanpa koordinat, dan tarif ekstrem disaring serta ratusan salah label kabupaten dan kapasitas kamar diluruskan, kami memperoleh **978 properti pasar reguler bersih** yang tersebar di **54 kecamatan** pada seluruh 9 kabupaten/kota di Bali dengan **38 fitur siap latih**.

Satu keputusan terpenting di tahap data: sekitar **27% properti (267 unit)** adalah properti baru yang memang belum punya ulasan. Nilai *rating*-nya sengaja kami biarkan **kosong alami (`NaN`)**, bukan diganti angka nol—karena dalam kenyataan, properti baru bukan berarti kualitasnya bintang nol.

---

## Slide 6 — Sebaran Wilayah & Pola Tarif Bali

*Slide 6*

Peta di sisi kiri memperlihatkan bagaimana 978 properti bersih ini tersebar merata di seluruh Bali, beserta 6 titik acuan wisata utama seperti Ubud, Canggu/Seminyak, Uluwatu, Sanur, Kintamani, dan Bandara Ngurah Rai yang kami hitung jarak fisiknya untuk setiap properti.

Di sisi kanan, terlihat bahwa sebaran tarif asli sangat miring ke kanan—mulai dari sekitar Rp 154 ribu sampai Rp 9,79 juta per malam, dengan nilai tengah Rp 1,47 juta. Kalau dilatih langsung dalam Rupiah, segelintir vila super mahal akan menarik model secara berlebihan. Karena itu, target harga diubah ke skala logaritma natural saat pelatihan sehingga distribusinya menjadi simetris dan jauh lebih stabil dipelajari, lalu hasilnya dikembalikan lagi ke Rupiah saat prediksi.

---

## Slide 7 — Tiga Model yang Diadu & Cara Uji yang Adil

*Slide 7*

Untuk mencari model terbaik, kami mengadu tiga keluarga algoritma pohon keputusan yang kuat di data tabel:
- **Random Forest** sebagai pembanding dasar yang menggabungkan ratusan pohon secara paralel.
- **XGBoost** yang membangun pohon secara bertahap untuk terus memperbaiki sisa kesalahan pohon sebelumnya.
- **CatBoost** yang punya keunggulan khusus karena bisa membaca langsung 54 nama kecamatan dan nilai *rating* kosong tanpa perlu memecahnya menjadi puluhan kolom biner baru.

Agar pengujiannya jujur dan bebas kebocoran data, sejak awal kami membagi data secara proporsional per kabupaten: **80% (782 unit)** dipakai untuk pelatihan dan validasi silang 5-lipatan, sementara **20% (196 unit)** dikunci penuh sebagai data uji terpisah. Jadi seluruh angka akurasi yang kami laporkan murni berasal dari properti yang belum pernah dilihat model sebelumnya.

---

## Slide 8 — Hasil Perbandingan Tiga Model

*Slide 8*

Ini hasil adu performa pada 196 data uji terpisah. Secara keseluruhan, **CatBoost tampil sebagai model terbaik** dengan memimpin pada R² tertinggi sebesar **0,6708**, rata-rata kesalahan (**MAE**) terendah **Rp 764 ribu**, serta kesalahan tengah (**MedAE**) terendah **Rp 391 ribu** per malam—artinya separuh dari seluruh properti uji meleset tidak lebih dari Rp 391 ribu.

Menariknya, hasil pengujian juga objektif menunjukkan kelebihan masing-masing model: **XGBoost** mencatat persentase kesalahan tengah (**MdAPE**) paling rapat di **27,61%**, unggul tipis 2,5 poin persen dari CatBoost (`30,09%`), sementara Random Forest berada di posisi ketiga di seluruh metrik. Selain itu, selisih R² validasi silang (`0,6636`) dan data uji (`0,6708`) sangat rapat, menandakan model tidak *overfitting* dan tetap stabil bahkan saat menemui kecamatan baru seperti Kuta Selatan.

---

## Slide 9 — Di Mana Model Paling Akurat? (Kelas Harga & Properti Baru)

*Slide 9*

Melihat satu angka rata-rata saja tidak cukup untuk pasar Bali yang rentang harganya sangat lebar. Karena itu kami bedah performa CatBoost per kelas harga dan status ulasan:
1. **Paling tajam di segmen utama (Villa Reguler Rp 750 ribu–2,5 juta)** yang mencakup hampir separuh pasar (45,4% data uji): rata-rata prediksi **Rp 1,46 juta** nyaris persis menyamai aktual **Rp 1,47 juta**, dengan error tengah hanya **24,84%**.
2. **Properti baru tanpa ulasan tetap andal**: pada 63 unit baru yang *rating*-nya kosong alami, CatBoost mencatat error tengah **29,07%** (MedAE Rp 296 ribu)—sebanding dengan unit yang sudah punya banyak ulasan (`30,10%`). Ini membuktikan sistem bisa dipakai pemilik baru sejak hari pertama buka.
3. **Keterbatasan jujur di ujung atas (Villa Premium Rp 6–10 juta)**: karena sampelnya baru 10 unit dan nilai jual vila super mewah banyak ditentukan estetika visual serta luas tanah yang belum ada di data tabel, model cenderung memprediksi lebih rendah di kelas ini.

---

## Slide 10 — Apa yang Paling Menentukan Tarif? (Transparansi SHAP)

*Slide 10*

Supaya pemilik properti tidak sekadar menerima angka tanpa tahu alasannya, kami memakai metode **SHAP** untuk membuka cara berpikir model. Secara global di sisi kiri, pendorong tarif terbesar adalah **tipe properti**, **jumlah kamar tidur**, **ketersediaan *bathtub***, **paket fasilitas mewah**, **total ruangan**, dan **kecamatan wisata**.

Di sisi kanan ada contoh nyata satu vila 4 kamar di **Pekutatan, Jembrana**. Dimulai dari harga dasar pasar Rp 1,41 juta, jumlah 4 kamar tidur, status vila, dan kelengkapan fasilitas mendorong prediksinya naik tajam. Namun karena lokasinya di Jembrana—bukan di Canggu atau Ubud—model secara cerdas menahan kenaikan tersebut agar tetap realistis dengan pasar barat Bali. Hasil akhirnya **Rp 2,35 juta**, hanya terpaut **1,1%** dari harga aslinya **Rp 2,37 juta**.

---

## Slide 11 — Tampilan Aplikasi Web: Menjawab Skenario Vila Ubud

*Slide 11*

Seluruh hasil pemodelan ini sudah kami kemas ke dalam aplikasi web interaktif Streamlit (*Bali Smart Pricing Engine*) dengan ukuran model sangat ringan, hanya 726 kilobyte.

Sekarang kita kembali ke skenario pemilik vila 2 kamar di Ubud di awal presentasi tadi. Begitu spesifikasi properti dimasukkan di panel sebelah kiri—lengkap dengan opsi centang *Listing Baru* apabila propertinya belum memiliki ulasan—sistem otomatis menghitung 7 jarak ke sentra wisata dan memberikan estimasi **Rp 3.292.301 per malam**, lengkap dengan **rentang pasar wajar Rp 2,90 juta hingga Rp 3,68 juta** (toleransi ±MedAE Rp 391 ribu). Di sebelah kanan atas, fitur **Simulasi *What-If*** bahkan membantu pemilik menghitung nilai tambah renovasi—misalnya ketersediaan *bathtub* menyumbang sekitar +Rp 426 ribu dan status *Superhost* sekitar +Rp 203 ribu per malam. Di luar kalkulator ini, aplikasi juga menyediakan tab Peta 978 properti, Dasbor Benchmark Model, dan Panel SHAP.

---

## Slide 12 — Kesimpulan, Keterbatasan & Penutup

*Slide 12*

Sebagai penutup, tiga hal utama menjawab langsung tujuan penelitian di awal tadi:
1. **Acuan tarif nyata bagi pemilik**: Aplikasi web *Bali Smart Pricing Engine* membantu pemilik vila dan *homestay* memperoleh estimasi harga pasar, rentang wajar (±Rp 391 ribu), dan simulasi tambah fasilitas — tidak lagi menebak atau sekadar meniru tetangga.
2. **Data katalog yang lengkap dan bersih**: Dari 1.235 baris data mentah 6 kolom, kami menyusun 978 data properti bersih di 54 kecamatan (38 fitur), sekaligus menjaga 267 properti baru tanpa ulasan tetap pada kondisi alaminya.
3. **Model andal dan alasannya transparan**: CatBoost tampil paling unggul dan seimbang dengan R² 0,6708—sangat akurat di kelas inti Villa Reguler (24,84%) serta tetap stabil untuk properti baru tanpa ulasan (29,07%)—dan SHAP membuka jelas faktor pendorong tarifnya.

Secara jujur, masih ada sekitar 33% variasi harga yang dipengaruhi faktor di luar tabel seperti kualitas foto arsitektur, luas tanah, serta musim ramai/sepi liburan—dan itulah arah pengembangan lanjutan kami. Terima kasih atas perhatiannya, kami siap melanjutkan ke sesi tanya jawab dan demo langsung aplikasi web.
