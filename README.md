# Smart City: AI Prediksi Kemacetan Lalu Lintas Bengkulu

## 🏛️ Deskripsi Proyek

Aplikasi ini merupakan prototipe sistem prediksi kemacetan lalu lintas dan rekomendasi rute berbasis kecerdasan buatan (AI) untuk kota Bengkulu. Sistem ini memanfaatkan data graf jalan dari OpenStreetMap, titik keramaian (POI), serta model AI Decision Tree untuk memprediksi tingkat kemacetan dan memberikan saran rute terbaik secara interaktif.

---

## 🧠 1. Relevansi & Justifikasi Model AI

Model AI yang digunakan adalah **Decision Tree (logika berbasis aturan)**. Alasan pemilihannya:

Decision Tree dipilih karena mudah diimplementasikan, cepat dalam inferensi, dan dapat menangani data tabular sederhana seperti jam, cuaca, dan jumlah titik keramaian aktif. Model ini cocok untuk prototipe sistem prediksi kemacetan berbasis fitur-fitur yang tersedia tanpa memerlukan data historis dalam jumlah besar.

Model tidak menggunakan machine learning berbasis training dataset besar, namun berbasis logika deterministik.

---

## 📊 2. Data & Pengelolaan

### Jenis Data:

* Titik keramaian (POI): Data manual, terdiri dari sekolah, mall, kantor, pasar, dan universitas, lengkap dengan jam aktif.
* Graf jalan: OpenStreetMap (diambil otomatis dengan OSMnx).
* Data cuaca dan waktu: Input manual dari user.

### Pengumpulan Data:

* Simulasi menggunakan **data statik** yang dikodekan langsung dalam sistem
* Koordinat dan nama lokasi berdasarkan asumsi wilayah Bengkulu

### Praproses:

* POI memiliki atribut jam aktif dan dapat dikembangkan dengan atribut hari aktif.
* Data training AI disimulasikan berdasarkan kombinasi jam, cuaca, dan jumlah POI aktif.
* Data graf disimpan dalam cache (bengkulu_graph.pkl) untuk efisiensi.
* Semua data diolah secara terstruktur sebelum digunakan untuk prediksi dan visualisasi.

---

## 🛋️ 3. Desain Sistem (Logis dan Terstruktur)

### Alur Sistem:

1. User memilih lokasi awal, tujuan, kendaraan, jam, dan cuaca.
2. Sistem menghitung **faktor kemacetan** berdasarkan:

   * Banyaknya titik padat aktif
   * Apakah sedang jam sibuk (pagi/sore)
   * Cuaca (jika hujan menambah delay)
3. Sistem menjalankan logika decision-tree sederhana untuk:

   * Menilai apakah jalur utama kemungkinan macet
   * Merekomendasikan jalur alternatif
4. **Visualisasi rute** ditampilkan dengan folium (peta interaktif)
5. Sistem memberikan **analisis AI** dan **kesimpulan kemacetan**

### Diagram:

Input User → Proses AI (Decision Rules) → Cek POI Aktif + Faktor Cuaca + Waktu →
Prediksi Kemacetan → Rekomendasi Rute → Visualisasi Peta + Analisis Teks

---

## 🎯 4. Evaluasi Sistem & Metrik

### Evaluasi dilakukan berdasarkan:

* Sistem diuji dengan berbagai kombinasi input (jam, cuaca, jumlah POI aktif) untuk melihat perubahan prediksi kemacetan dan rekomendasi rute.
* Hasil prediksi AI (Decision Tree) ditampilkan secara eksplisit di hasil analisis.
* **Status rute rekomendasi** apakah benar menjauhi titik padat

### Metrik Evaluasi:

* Untuk prototipe ini, evaluasi dilakukan secara kualitatif dengan membandingkan hasil prediksi dengan ekspektasi logis (misal: kemacetan tinggi saat rush hour dan banyak POI aktif).

---

## 🚀 5. Kreativitas & Pengembangan

### Fitur :

* Simulasi cuaca & waktu yang mengubah status POI
* Visualisasi status POI dan rute pada peta interaktif.
* Integrasi AI Decision Tree untuk prediksi kemacetan secara otomatis.

### Potensi Pengembangan:

* Integrasi dengan data **cuaca API & sensor traffic**
* Sinkronisasi dengan Google Maps / Leaflet real-time
* Aplikasi mobile berbasis Flutter
* Sistem dapat dikembangkan dengan menambah atribut hari aktif pada POI agar prediksi lebih realistis (misal: sekolah/kantor tidak aktif saat weekend).
* Integrasi data real-time (sensor lalu lintas, crowdsourcing).
* Penggunaan model AI lain (misal: Neural Network) jika data historis tersedia.

---

## 📂 Struktur Folder

```
smartcity-bengkulu-traffic-ai/
├── index.py               # File utama aplikasi AI
├── README.md              # Dokumentasi sistem
├── requirements.txt       # Library Python
└── /screenshots           # (opsional) tampilan sistem
```

---

## 📚 Cara Menjalankan

```bash
pip install osmnx networkx geopy folium scikit-learn
python index.py
```

---

## 🌍 Link GitHub


