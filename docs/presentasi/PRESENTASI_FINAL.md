# Bali Smart Pricing Engine
**Sistem Rekomendasi Tarif Sewa Harian Villa dan Homestay di Bali Berbasis Machine Learning & Explainable AI**

Presentasi Hasil Akhir — Tugas Besar Pembelajaran Mesin  
**I Kadek Adi Sunetra** · 2305551053  
**Anthony Wisnu Jati** · 2305551138  
Program Studi Teknologi Informasi · Fakultas Teknik · Universitas Udayana (2026)  
Dosen Pengampu: **Yogiswara Dharma Putra, S.TI., M.T.**

> Dek presentasi ini terdiri dari **15 slide (16:9)** berdurasi sekitar **9–11 menit** (`PRESENTASI_FINAL.pptx` / `.pdf`). Naskah pada setiap slide di bawah ini merupakan skrip lisan siap ucap yang sekaligus tertanam otomatis pada *Speaker Notes* PowerPoint.

---

## Slide 1 — Sampul

*Slide 1*

*Durasi:* ~20 detik

*Narasi:*
Selamat pagi atau siang Bapak dosen pengampu dan rekan-rekan sekalian. Perkenalkan, kami I Kadek Adi Sunetra dan Anthony Wisnu Jati dari Program Studi Teknologi Informasi Universitas Udayana. Hari ini kami akan memaparkan hasil akhir tugas besar Pembelajaran Mesin kami yang berjudul Bali Smart Pricing Engine, yaitu sistem rekomendasi tarif sewa harian vila dan homestay di Bali berbasis Machine Learning dan Explainable AI.

---

## Slide 2 — Masalah Nyata di Lapangan

*Slide 2*

*Durasi:* ~45 detik

*Narasi:*
Penelitian kami berangkat dari kondisi nyata pariwisata Bali saat ini. Berdasarkan penelitian di Jurnal Kajian Bali tahun 2026, kunjungan wisatawan mancanegara memang sudah menembus 6,9 juta perjalanan pada 2025, tapi okupansi hotel berbintang justru tertahan di 57 sampai 67 persen karena wisatawan makin memilih vila privat dan homestay. Akibatnya, jumlah properti terdaftar melonjak dari 12.227 unit pada 2024 menjadi 17.543 unit pada akhir 2025, didominasi 7.610 vila dan 5.594 homestay.

Di tengah persaingan yang sepadat ini, sebuah penelitian di Bali tahun 2025 mengungkapkan bahwa penentuan harga yang adaptif dan dinamis jauh lebih efektif untuk meningkatkan pendapatan harian. Ditambah lagi, penelitian tahun 2026 menunjukkan bahwa kesesuaian harga dan adanya ulasan yang jelas sangat menentukan keputusan tamu memesan vila, dibandingkan sekadar memasang diskon atau promosi biasa.

Lalu masalahnya, sebagian besar pemilik vila atau homestay saat ini masih sangat sering memasang tarif dengan menebak sendiri atau sekadar meniru penginapan di sekitarnya. Cara seperti ini tidak punya dasar yang jelas: kalau harga dipasang terlalu mahal, calon tamu langsung pindah ke pesaing; sebaliknya, kalau terlalu murah, pemasukan tidak cukup menutup biaya listrik, air, dan perawatan harian.

*Tunjuk:*
Tunjuk angka besar 17.543 unit di kanan atas, lalu arahkan ke tiga poin risiko salah harga di bawahnya.

*Transisi:*
Supaya masalah ini lebih kebayang, mari kita lihat satu contoh kasus nyata yang dialami pemilik vila di Bali.

*Tanya:*
Kenapa pemilik tidak melihat langsung harga di Airbnb saja secara manual?

*Jawab:*
Karena dua properti di area yang sama sering berbeda jauh fasilitas dan kapasitasnya, dan harga di halaman pencarian Airbnb belum tentu tarif murni untuk satu malam—seperti yang akan kita tunjukkan pada bagian data sebentar lagi.

---

## Slide 3 — Skenario Nyata: Vila 2 Kamar di Ubud

*Slide 3*

*Durasi:* ~35 detik

*Narasi:*
Mari kita lihat satu contoh kasus nyata. Bayangkan seorang pemilik mengelola vila privat dua kamar tidur di Ubud, Gianyar, dengan kapasitas 4 tamu, 2 kamar mandi, kolam renang pribadi, bathtub, ruang kerja, parkir gratis, dan pemandangan sawah.

Pertanyaannya adalah, berapa tarif per malam yang wajar untuk vila seperti ini? Ada dua tantangan di sini. Pertama, kalau pemilik hanya sekadar meniru harga properti yang berada di sekitarnya, sangat mungkin penginapan di sekitar itu tidak punya bathtub atau kolam renang pribadi, sehingga patokannya pasti meleset. Kedua, bagaimana kalau vila ini baru saja buka dan belum punya satu pun ulasan tamu? Pendekatan yang hanya mengandalkan analisis ulasan jelas langsung buntu pada kondisi ini.

Nah, kasus vila Ubud ini akan langsung kita jawab lewat aplikasi web kami di bagian akhir presentasi nanti.

*Tunjuk:*
Tunjuk tiga angka spesifikasi (2 kamar tidur, 4 tamu, 2 kamar mandi) dan pita pertanyaan gelap di bagian bawah layar.

*Transisi:*
Dari kasus nyata tadi, kami merumuskan tiga tujuan utama yang menjadi pegangan seluruh penelitian ini.

*Tanya:*
Kenapa contohnya memakai Ubud, apakah sistem hanya berlaku untuk Ubud?

*Jawab:*
Tidak—Ubud hanya satu contoh nyata yang mudah dibayangkan. Sistem kami mencakup seluruh sembilan kabupaten dan kota di Bali pada 54 kecamatan resmi.

---

## Slide 4 — Tujuan & Gambaran Besar Solusi

*Slide 4*

*Durasi:* ~35 detik

*Narasi:*
Dari masalah tadi, ada tiga tujuan utama yang ingin kami capai. Pertama, membantu pemilik vila dan homestay di Bali mendapatkan rekomendasi tarif harian yang wajar sesuai spesifikasi fisik, fasilitas, dan lokasi propertinya.

Kedua, melengkapi dan membenahi data katalog daring awal yang masih minim agar cukup akurat untuk dipakai melatih model. Ketiga, membangun serta membandingkan model machine learning yang andal—termasuk bagi properti baru tanpa ulasan—lalu menyajikannya lewat aplikasi web interaktif yang juga menjelaskan alasan di balik estimasi harganya.

Alur besarnya sederhana seperti di bagian bawah layar: pemilik cukup memasukkan spesifikasi properti, model memproses seluruh faktornya, lalu sistem mengeluarkan estimasi tarif wajar beserta alasannya.

*Tunjuk:*
Tunjuk urutan nomor 01, 02, 03 dari atas ke bawah, lalu arahkan ke alur 3 kotak di bagian bawah.

*Transisi:*
Untuk mencapai tujuan kedua dan ketiga, langkah pertama yang paling krusial adalah melihat kondisi data awal yang kita miliki—dan kenapa data itu belum cukup.

*Tanya:*
Kenapa harus ada penjelasan alasan harga, tidak cukup angka prediksi saja?

*Jawab:*
Penelitian valuasi properti di jurnal Scientific Reports tahun 2026 membuktikan bahwa pemilik dan penilai properti jauh lebih percaya memakai rekomendasi sistem ketika mereka bisa melihat faktor apa saja yang menaikkan atau menurunkan harganya.

---

## Slide 5 — Data Awal: 6 Kolom & Kenapa Belum Cukup

*Slide 5*

*Durasi:* ~45 detik

*Narasi:*
Sekarang kita masuk ke data. Data awal yang kami ambil dari repositori publik Kaggle, yaitu Indonesia Airbnb Dataset Bali, hanya berjumlah 1.235 baris dan isinya cuma 6 kolom dasar: nama penginapan, harga mentah, rating, jumlah ulasan, tautan URL listing, dan wilayah kabupaten.

Kalau kita langsung melatih model dari 6 kolom ini saja, hasilnya pasti sangat kurang. Kenapa? Penelitian penentuan harga Airbnb tahun 2021 membuktikan bahwa tarif sewa sangat dipengaruhi oleh tipe ruang, kapasitas kamar, kelengkapan fasilitas, dan jarak ke tempat wisata. Bahkan penelitian studi kasus Airbnb di Istanbul tahun 2024 membuktikan bahwa menambahkan fitur jarak lokasi wisata saja sudah menaikkan Adjusted R² XGBoost sampai 22 persen dan menurunkan error MAE 10 persen.

Di data awal kita, semua atribut penting itu belum ada—tidak ada jumlah kamar, tidak ada daftar fasilitas, dan tidak ada koordinat GPS. Setelah kami cek ke halaman asli Airbnb, kolom harganya juga ternyata masih tercampur paket 5 malam, banyak label kabupaten yang tertukar karena radius peta, dan rating properti baru masih tercampur teks "New" atau kosong.

*Tunjuk:*
Tunjuk daftar 6 kolom mentah di kotak kiri, lalu arahkan ke 4 celah fatal pada panel gelap di sebelah kanan.

*Transisi:*
Untungnya data awal menyimpan kolom tautan URL tiap properti. Tautan inilah yang kami manfaatkan untuk melengkapi data di tahap berikutnya.

*Tanya:*
Kenapa tidak langsung memakai data agregator berbayar seperti AirDNA atau Inside Airbnb?

*Jawab:*
Penelitian di jurnal Annals of Tourism Research tahun 2018 mencatat bahwa Airbnb tidak merilis statistik resmi per wilayah, dan kajian di jurnal PLoS One tahun 2024 menyoroti bahwa agregator komersial kerap menutup prosedur pengambilan datanya. Selain itu Bali belum tercakup lengkap rincian fasilitasnya, jadi pengayaan langsung dari URL listing jauh lebih transparan.

---

## Slide 6 — Pengayaan Data Lewat Tautan Listing (6 → 30 Kolom)

*Slide 6*

*Durasi:* ~45 detik

*Narasi:*
Untuk melengkapi kekosongan tadi, kami membuat skrip penarikan data menggunakan nomor unik room_id dari kolom tautan. Mengikuti prinsip transparansi pengambilan data yang ditekankan penelitian di jurnal PLoS One tahun 2024, penarikan dilakukan berjeda 4 sampai 7 detik hingga terkumpul 1.036 berkas JSON lokal berisi koordinat GPS, kapasitas kamar, tipe properti, status host, daftar fasilitas, dan deskripsi.

Secara bersamaan, kami juga menguji langsung harga menginap satu malam murni—check-in H+5 sampai check-out H+6—pada 28 properti di koridor Denpasar, Kuta, dan Canggu. Dari situ ada 6 properti yang beririsan langsung dengan data awal, dan terbukti angka harga awal memang paket 5 malam. Jadi 6 unit irisan memakai tarif 1 malam langsung, sedangkan sisanya kami bagi 5 agar semuanya seragam per malam.

Saat seluruh data digabungkan, sebanyak 1.212 dari 1.235 baris berhasil dipadankan, sehingga struktur data berkembang dari 6 kolom mentah menjadi 30 kolom yang jauh lebih lengkap.

*Tunjuk:*
Ikuti alur 4 kotak atas dari kiri ke kanan (01 sampai 04), lalu tunjuk kotak kiri bawah yang merinci 24 atribut baru.

*Transisi:*
Setelah jadi 30 kolom, data ini belum langsung bisa dilatih karena masih ada beberapa kesalahan yang harus dibersihkan dulu di slide berikut.

*Tanya:*
Kenapa hanya 1.036 JSON dari 1.235 baris awal, ke mana sisanya?

*Jawab:*
Di dalam 1.235 baris awal ada 177 baris duplikat dengan room_id yang sama akibat irisan area pencarian, ditambah 22 tautan yang sudah tidak aktif atau tidak punya koordinat—jadi unit unik yang valid berkoordinat memang tepat 1.036 properti.

---

## Slide 7 — Pembersihan Anomali & Properti Baru

*Slide 7*

*Durasi:* ~50 detik

*Narasi:*
Di tahap pembersihan, alur penyusutan datanya bisa dilihat langsung di empat kotak bagian atas. Dari 1.235 baris gabungan awal, kami hapus 177 baris duplikat berdasarkan room_id sehingga tersisa 1.058 unit unik, lalu kami keluarkan 22 unit yang tidak punya koordinat GPS sehingga tersisa 1.036 unit.

Pada 1.036 unit ini, kami meluruskan 402 salah label kabupaten memakai kamus wilayah resmi Bali, serta memperbaiki kapasitas kamar pada 73 unit dari pola judul iklannya seperti "1BR" atau "2 Bedroom". Selanjutnya, agar model fokus pada pasar harian reguler, kami menyaring 58 tarif ekstrem—di bawah Rp 150 ribu, di atas Rp 10 juta, atau di atas Rp 4 juta per kamar—hingga diperoleh tepat 978 properti bersih di 54 kecamatan pada 9 kabupaten dan kota di Bali.

Satu keputusan penting ada di kotak kanan: 267 properti atau 27,3 persen data adalah unit baru yang belum punya ulasan. Karena properti yang sudah berulasan punya rating di rentang 3,50 sampai 5,00 dengan nilai tengah 4,95, rating 267 properti baru ini sengaja kami biarkan kosong alami (NaN) dan diberi penanda listing baru—bukan diisi angka nol supaya model tidak mengira vila baru berkualitas bintang nol.

*Tunjuk:*
Tunjuk corong 1.235 → 1.058 → 1.036 → 978 di atas, lalu tekankan kotak kanan gelap soal 267 properti baru.

*Transisi:*
Setelah punya 978 unit bersih dengan 30 kolom, bagaimana akhirnya kami menyusun 38 fitur prediktor inti? Mari kita lihat hitungannya di slide berikutnya.

*Tanya:*
Kenapa tarif di atas Rp 10 juta per malam dikeluarkan?

*Jawab:*
Jumlahnya hanya 18 unit dan umumnya berupa resor komersial atau vila ultra-mewah sangat khusus. Kalau dipaksakan masuk ke model pasar reguler, kesalahan besar dari belasan unit itu akan merusak akurasi prediksi bagi mayoritas vila dan homestay reguler.

---

## Slide 8 — Dari 30 Kolom Menuju 38 Fitur Prediktor Inti

*Slide 8*

*Durasi:* ~45 detik

*Narasi:*
Dari 30 kolom hasil pengayaan tadi, hitungannya sampai menjadi 38 fitur inti bisa dilihat jelas di bagian atas layar. Pertama, kami membuang 1 kolom tautan URL karena alamat web bukan variabel untuk memprediksi harga.

Berikutnya, mengikuti penelitian pemodelan harga properti berbasis lokasi tahun 2022 dan 2023, kami menambahkan 12 fitur baru: yaitu 4 rasio kepadatan ruang, 1 skor total fasilitas mewah skala 0 sampai 5 tanpa bobot subjektif, serta 7 fitur jarak ke 6 sentra wisata utama plus jarak sentra terdekat dengan rumus Haversine. Ditambah 1 kolom target harga skala logaritma, tabel akhir berisi tepat 42 kolom.

Sebelum pelatihan, kami memisahkan 4 kolom yang bukan fitur masukan—yaitu ID properti, nama iklan, harga Rupiah asli, dan target logaritma—sehingga lahir tepat 38 fitur prediktor inti: 10 fitur struktur ruang, 11 fitur lokasi dan jarak, 8 fitur fasilitas mewah, serta 9 fitur reputasi dan sinyal teks.

*Tunjuk:*
Ikuti kotak hitungan di atas (30 − 1 + 13 = 42 − 4 = 38), lalu tunjuk sekilas 4 kotak rumpun fitur di bawahnya.

*Transisi:*
Sekarang mari kita lihat sebaran lokasi 978 properti ini di peta Bali dan kenapa target harganya perlu diubah ke skala logaritma.

*Tanya:*
Kenapa skor fasilitas mewah dibuat penjumlahan 0 sampai 5 tanpa bobot?

*Jawab:*
Supaya tidak ada bias subjektif dari peneliti. Kami biarkan algoritma pohon keputusan sendiri yang mempelajari bobot pengaruh masing-masing fasilitas dari data pasar riil.

---

## Slide 9 — Sebaran Lokasi & Pola Tarif di Bali

*Slide 9*

*Durasi:* ~40 detik

*Narasi:*
Peta di sisi kiri menunjukkan sebaran 978 properti bersih kami di seluruh Bali, lengkap dengan 6 bintang kuning sebagai titik ukur jarak Haversine, yaitu Canggu dan Seminyak, Ubud, Uluwatu, Sanur, Kintamani, serta Bandara Ngurah Rai.

Di sisi kanan atas, grafik merah memperlihatkan sebaran harga aslinya yang miring tajam ke kanan—dari Rp 154 ribu sampai Rp 9,79 juta per malam dengan skewness 1,638. Sesuai penelitian prediksi harga properti di jurnal Applied Sciences tahun 2023, kalau model dilatih langsung pada distribusi semiring ini, segelintir vila yang sangat mahal akan menarik bobot pelatihan terlalu kuat.

Karena itu, target kami ubah ke skala logaritma natural seperti grafik biru di kanan bawah. Kemiringannya langsung turun menjadi minus 0,059 yang nyaris simetris, sehingga proses belajar model jauh lebih stabil sebelum hasil prediksinya dikembalikan lagi ke Rupiah.

*Tunjuk:*
Tunjuk bintang kuning pada peta kiri, lalu bandingkan grafik merah di kanan atas dengan grafik biru di kanan bawah.

*Transisi:*
Dengan 978 data bersih, 38 fitur inti, dan target yang sudah seimbang, selanjutnya kita masuk ke pemilihan algoritma dan cara pengujiannya.

*Tanya:*
Bagaimana rumus mengembalikan prediksi logaritma ke satuan Rupiah?

*Jawab:*
Memakai inversi eksponensial yaitu exp(prediksi_log) dikurangi 1, sehingga semua error bisnis seperti MAE, RMSE, MedAE, dan MdAPE tetap dihitung jujur dalam Rupiah asli.

---

## Slide 10 — Tiga Model yang Diadu & Prinsip Uji Adil

*Slide 10*

*Durasi:* ~45 detik

*Narasi:*
Untuk pemodelan, kami memilih keluarga algoritma pohon keputusan. Penelitian perbandingan model tahun 2024 menunjukkan ansambel pohon jauh lebih stabil daripada regresi linier untuk pola harga yang nonlinier. Penelitian Airbnb di jurnal JELIKU Universitas Udayana tahun 2023 juga membuktikan gradient boosting mengungguli deep learning, SVR, dan KNN pada data properti seperti ini.

Kami mengadu tiga algoritma: Random Forest sebagai pembanding dasar, XGBoost yang memperbaiki kesalahan secara bertahap, dan CatBoost. Perbedaan utamanya ada pada cara membaca data: Random Forest dan XGBoost perlu memecah 54 kecamatan menjadi 101 kolom biner serta mengisi rating kosong dengan nilai tengah, sedangkan CatBoost membaca langsung 38 fitur asli dan nilai rating kosong secara alami.

Agar pengujiannya adil dan bebas kebocoran data sesuai panduan validasi di Journal of Analysis and Testing tahun 2018, data kami bagi proporsional per kabupaten 80 banding 20 sejak awal: 782 unit untuk pelatihan dan validasi silang 5-lipatan, sementara 196 unit uji dikunci penuh di luar pelatihan maupun pra-pemrosesan.

*Tunjuk:*
Tunjuk 3 model di kartu putih kiri (tekankan CatBoost di bawah), lalu arahkan ke angka 80% dan 20% pada panel gelap kanan.

*Transisi:*
Setelah ketiga model diadu pada 196 data uji terpisah tadi, begini hasil performanya di slide berikut.

*Tanya:*
Apa yang terjadi kalau di data uji ada kecamatan yang tidak pernah muncul di data latih?

*Jawab:*
Kasus itu benar-benar terjadi pada kecamatan Kuta Selatan yang hanya muncul di data uji. Di Random Forest dan XGBoost kami pasang handle_unknown="ignore" agar aman bernilai nol, sedangkan CatBoost menanganinya otomatis lewat statistik prior tanpa error.

---

## Slide 11 — Hasil Perbandingan Tiga Model

*Slide 11*

*Durasi:* ~45 detik

*Narasi:*
Ini hasil pengujian pada 196 properti uji yang belum pernah dilihat model sebelumnya. CatBoost Regressor tampil paling unggul dengan R² tertinggi 0,6708, rata-rata kesalahan MAE terendah Rp 764 ribu, RMSE Rp 1,23 juta, dan kesalahan tengah MedAE terendah Rp 391 ribu per malam. Artinya, separuh dari seluruh properti uji meleset tidak lebih dari Rp 391 ribu.

Stabilitasnya juga terbukti kuat: R² validasi silang CatBoost sebesar 0,6636 hampir sama persis dengan R² data uji 0,6708—selisihnya cuma 0,0072, menandakan model tidak overfitting dan bebas kebocoran data.

Secara objektif, XGBoost unggul tipis pada persentase kesalahan tengah MdAPE di 27,61 persen dibanding CatBoost 30,09 persen, sementara Random Forest berada di posisi terakhir di semua metrik. Karena CatBoost memimpin di R², seluruh ukuran error Rupiah, serta menangani 54 kecamatan dan properti baru secara alami, CatBoost kami pilih sebagai model utama.

*Tunjuk:*
Tunjuk 3 kartu KPI di atas, lalu baris hijau CatBoost dan angka 27,61% hijau pada baris XGBoost.

*Transisi:*
Namun angka rata-rata untuk seluruh Bali saja belum cukup untuk melihat apakah model akurat di kelas murah maupun kelas mewah. Mari kita bedah per kelas harga di slide berikutnya.

*Tanya:*
Kenapa memilih CatBoost kalau MdAPE XGBoost lebih rendah 2,5 persen?

*Jawab:*
Karena CatBoost unggul di 5 dari 7 indikator—termasuk R² dan seluruh galat Rupiah (MAE, RMSE, MedAE)—serta punya keunggulan arsitektur langsung pada 54 kecamatan dan 267 properti baru tanpa kolom dummy maupun imputasi median buatan.

---

## Slide 12 — Ketepatan per Kelas Harga & Properti Baru

*Slide 12*

*Durasi:* ~50 detik

*Narasi:*
Sesuai rekomendasi kajian evaluasi metrik tahun 2022 serta riset penilaian properti modern tahun 2023 dan 2025, data harga yang miring wajib dinilai memakai metrik nilai tengah seperti MedAE dan MdAPE serta dibedah per kelas harga.

Di grafik kanan, akurasi terbaik dicapai pada segmen terbesar pasar yaitu Villa Reguler Rp 750 ribu sampai 2,5 juta yang mencakup 45,4 persen data uji: rata-rata prediksi Rp 1,46 juta hampir identik dengan aktual Rp 1,47 juta, dengan error tengah 24,84 persen. Lalu untuk menjawab tantangan properti baru di Slide 3, titik oranye di grafik kiri memperlihatkan 63 unit baru tanpa ulasan tetap diprediksi dengan error tengah 29,07 persen—hampir sama dengan unit berulasan di 30,10 persen.

Di sisi lain, kami juga jujur pada kelemahan model: di kelas Villa Premium Rp 6 sampai 10 juta, prediksi masih terlalu rendah—Rp 4,35 juta dibanding aktual Rp 7,51 juta. Penyebabnya karena sampelnya baru 10 unit dan vila semewah itu banyak ditentukan kualitas visual foto serta luas tanah yang belum tercatat di data tabel.

*Tunjuk:*
Tunjuk bar "Villa Reguler" pada grafik kanan, lalu titik berlian oranye di grafik kiri, lalu bar paling kanan "Villa Premium".

*Transisi:*
Setelah tahu seberapa akurat model di tiap segmen, sekarang pertanyaannya: faktor apa saja yang paling kuat mendorong harga naik atau turun?

*Tanya:*
Kalau R² unit baru lebih rendah (0,52) dibanding unit berulasan (0,74), kenapa dibilang tetap andal?

*Jawab:*
Karena R² sangat sensitif terhadap segelintir vila baru berharga mahal yang menyebar lebar tanpa sinyal ulasan, sedangkan bagi mayoritas unit baru (diukur dari MedAE Rp 296 ribu dan MdAPE 29,1 persen), ketepatannya sejajar dengan properti yang sudah berulasan.

---

## Slide 13 — Faktor Penentu Tarif (Transparansi SHAP)

*Slide 13*

*Durasi:* ~45 detik

*Narasi:*
Supaya model tidak jadi kotak hitam, kami memakai metode SHAP dari konferensi NeurIPS tahun 2017 untuk membuka faktor pendorong harga. Di grafik sebelah kiri, penentu terbesar secara keseluruhan adalah tipe properti, jumlah kamar tidur, keberadaan bathtub, skor fasilitas mewah, total ruangan, dan kecamatan wisata—sejalan dengan riset penentu harga Airbnb tahun 2021.

Di sebelah kanan ada contoh nyata satu properti uji, yaitu vila 4 kamar di Pekutatan, Jembrana. Mulai dari harga dasar pasar Rp 1,41 juta, jumlah 4 kamar, tipe vila, desain mewah, dan bathtub mendorong prediksi naik cukup tinggi. Namun karena lokasinya di Jembrana—bukan di Canggu atau Ubud—model otomatis menahan kenaikannya sehingga keluar prediksi Rp 2,35 juta, cuma selisih 1,1 persen dari harga aslinya Rp 2,37 juta.

Penelitian valuasi properti di jurnal Scientific Reports tahun 2026 juga menegaskan bahwa transparansi seperti inilah yang membuat pemilik percaya memakai rekomendasi sistem.

*Tunjuk:*
Tunjuk daftar fitur teratas di panel kiri (a), lalu ikuti tangga merah naik dan batang biru Jembrana turun di panel kanan (b) hingga prediksi Rp 2,35 juta.

*Transisi:*
Sekarang saatnya kita kembali ke pertanyaan vila dua kamar di Ubud pada Slide 3 dan melihat langsung jawaban aplikasi web kami.

*Tanya:*
Kenapa kolam renang pribadi tidak muncul sendiri di 10 besar grafik kiri?

*Jawab:*
Bukan karena tidak penting, tapi pengaruhnya sudah masuk ke fitur Skor Fasilitas Mewah di posisi ke-4 dan sangat berkorelasi dengan kategori Tipe Properti Villa di posisi ke-1.

---

## Slide 14 — Aplikasi Web: Menjawab Skenario Vila Ubud

*Slide 14*

*Durasi:* ~45 detik

*Narasi:*
Seluruh model CatBoost yang ukurannya hanya 726 kilobyte ini sudah kami terapkan ke aplikasi web interaktif Streamlit. Di sini kita bisa lihat jawaban langsung untuk skenario vila 2 kamar di Ubud dari Slide 3 tadi.

Pada panel kiri, pemilik cukup memilih lokasi Gianyar–Ubud, tipe Villa Pribadi, 2 kamar tidur, 4 tamu, 2 kamar mandi, lalu mencentang fasilitasnya—dan kalau unitnya baru buka tanpa ulasan, cukup centang kotak "Listing Baru" di atas slider Rating. Sistem otomatis menghitung 7 jarak wisata lalu mengeluarkan estimasi Rp 3.292.301 per malam dengan rentang pasar wajar Rp 2,90 sampai 3,68 juta.

Di kanan atas ada fitur Simulasi What-If: pemilik bisa langsung mengecek perkiraan tambahan tarif jika menambah fasilitas tertentu, misalnya bathtub menyumbang sekitar plus Rp 426 ribu dan status Superhost plus Rp 203 ribu per malam. Di luar kalkulator ini, aplikasi juga punya tab Peta 978 properti, Benchmark Model, dan Panel SHAP.

*Tunjuk:*
Tunjuk angka hijau Rp 3.292.301 dan checkbox "Listing Baru" di kiri, lalu tunjuk tabel Simulasi What-If di kanan atas.

*Transisi:*
Dengan terjawabnya kasus vila Ubud tadi, mari kita tutup dengan rangkuman tiga kesimpulan utama dan keterbatasan penelitian kami.

*Tanya:*
Apakah aplikasi langsung menghitung ulang 7 jarak Haversine saat pengguna mengganti kecamatan?

*Jawab:*
Ya, setiap kecamatan menyimpan koordinat pusatnya, jadi begitu kabupaten atau kecamatan diganti di dropdown, seluruh 7 jarak Haversine dan 4 rasio kapasitas langsung dihitung ulang secara real-time sebelum diprediksi CatBoost.

---

## Slide 15 — Kesimpulan, Keterbatasan & Penutup

*Slide 15*

*Durasi:* ~40 detik

*Narasi:*
Sebagai penutup, ada tiga kesimpulan utama yang menjawab langsung tujuan kami di awal. Pertama, aplikasi web Bali Smart Pricing Engine membantu pemilik vila dan homestay mendapatkan patokan tarif harian yang wajar lengkap dengan rentang toleransi plus minus Rp 391 ribu dan simulasi fasilitas, sehingga tidak perlu lagi menebak sendiri atau meniru properti di sekitarnya.

Kedua, keterbatasan 6 kolom data awal berhasil kami atasi lewat pengayaan halaman listing dan pembersihan menyeluruh hingga menghasilkan 978 properti bersih di 54 kecamatan dengan 38 fitur inti, sambil menjaga 267 properti baru tanpa ulasan tetap alami. Ketiga, CatBoost terbukti paling unggul dengan R² 0,6708—sangat akurat di kelas utama Villa Reguler 24,8 persen dan tetap stabil untuk properti baru 29,1 persen—dengan alasan harga yang transparan lewat SHAP.

Secara jujur, sisa sekitar 33 persen variasi harga masih dipengaruhi faktor di luar tabel seperti kualitas foto arsitektur, luas tanah, dan musim ramai atau sepi liburan—dan itulah fokus pengembangan kami ke depan. Terima kasih atas perhatiannya, kami siap melanjutkan ke sesi tanya jawab dan demo aplikasi web.

*Tunjuk:*
Tunjuk poin 01, 02, 03 secara berurutan di panel gelap kiri, lalu kotak keterbatasan di kanan atas, dan akhiri dengan menatap audiens.

*Transisi:*
Selesai — lanjut ke sesi Tanya Jawab dan Demo Langsung Streamlit (`http://localhost:8501`).

*Tanya:*
Kalau proyek ini dilanjutkan jadi produk nyata, langkah pertama apa yang paling besar dampaknya menaikkan akurasi?

*Jawab:*
Mengubah pengambilan data dari satu waktu saja menjadi pemantauan berkala lintas musim (longitudinal scraping) sekaligus menambahkan fitur luas tanah dan kualitas visual foto—karena itulah penyebab utama sisa 33 persen variasi harga saat ini.
