# Smart City: AI Prediksi Kemacetan Lalu Lintas Bengkulu

## 🏛️ Deskripsi Proyek

Sistem ini merupakan prototipe **prediksi kemacetan lalu lintas** berbasis kecerdasan buatan untuk mendukung program **Smart City di Bengkulu**. Aplikasi ini dapat memprediksi potensi kemacetan berdasarkan **waktu, cuaca, hari (weekend/weekday)**, dan **lokasi titik keramaian** seperti sekolah, pasar, dan kantor. Sistem juga memberikan **rekomendasi rute alternatif** secara real-time dengan visualisasi menggunakan peta.

---

## 🧠 1. Relevansi & Justifikasi Model AI

Model AI yang digunakan adalah **Decision Tree (logika berbasis aturan)**. Alasan pemilihannya:

* Mudah diimplementasikan dan dimengerti
* Cocok untuk **data diskrit dan bersifat if-else** seperti waktu, hari, dan kategori titik keramaian
* Efisien untuk aplikasi simulasi ringan tanpa memerlukan training data besar

Model tidak menggunakan machine learning berbasis training dataset besar, namun berbasis logika deterministik.

---

## 📊 2. Data & Pengelolaan

### Jenis Data:

* **Titik POI (Point of Interest):** Sekolah, pasar, kantor, mall
* **Faktor waktu:** Jam (0-24)
* **Hari:** Apakah weekend atau bukan
* **Cuaca:** Cerah / Hujan

### Pengumpulan Data:

* Simulasi menggunakan **data statik** yang dikodekan langsung dalam sistem
* Koordinat dan nama lokasi berdasarkan asumsi wilayah Bengkulu

### Praproses:

* POI dianalisis berdasarkan jam aktif dan tipe lokasi
* Jika weekend, sekolah dan kantor dianggap **tidak aktif**
* Waktu dan cuaca dikombinasikan menjadi faktor prediksi kemacetan

---

## 🛋️ 3. Desain Sistem (Logis dan Terstruktur)

### Alur Sistem:

1. **Pengguna memilih**: Lokasi awal & tujuan, jam, cuaca, hari
2. Sistem menghitung **faktor kemacetan** berdasarkan:

   * Banyaknya titik padat aktif
   * Apakah sedang jam sibuk (pagi/sore)
   * Cuaca (jika hujan menambah delay)
3. Sistem menjalankan logika decision-tree sederhana untuk:

   * Menilai apakah jalur utama kemungkinan macet
   * Merekomendasikan jalur alternatif
4. **Visualisasi rute** ditampilkan dengan folium (peta interaktif)
5. Sistem memberikan **analisis AI** dan **kesimpulan kemacetan**

### Diagram (Opsional di README):

```
Input User → Proses AI (Decision Rules) → Cek POI Aktif + Faktor Cuaca + Waktu →
Prediksi Kemacetan → Rekomendasi Rute → Visualisasi Peta + Analisis Teks
```

---

## 🎯 4. Evaluasi Sistem & Metrik

### Evaluasi dilakukan berdasarkan:

* **Jumlah POI aktif** yang memengaruhi jalur
* **Skor kemacetan** (rentang 0–10), dihitung dari kombinasi waktu, cuaca, dan titik padat
* **Status rute rekomendasi** apakah benar menjauhi titik padat

### Metrik Evaluasi:

* **Kelas Kemacetan**:

  * 0–4: Lancar
  * 5–7: Padat
  * 8–10: Macet Berat
* Validasi dilakukan secara simulasi manual berdasarkan input skenario (weekend/hari sibuk)

---

## 🚀 5. Kreativitas & Pengembangan

### Fitur Inovatif:

* Simulasi cuaca & waktu yang mengubah status POI
* **Pengecualian otomatis titik sekolah/kantor saat weekend**
* Penambahan analisis AI berupa:

  * Penjelasan penyebab kemacetan
  * Skor kemacetan akhir
  * Rekomendasi waktu alternatif

### Potensi Pengembangan:

* Integrasi dengan data **cuaca API & sensor traffic**
* Sinkronisasi dengan Google Maps / Leaflet real-time
* Aplikasi mobile berbasis Flutter
* Visualisasi heatmap area macet di kota Bengkulu

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
pip install folium tkinter
python index.py
```

---

## 🌍 Link GitHub

[https://github.com/namakamu/smartcity-bengkulu-traffic-ai](https://github.com/namakamu/smartcity-bengkulu-traffic-ai) *(ganti dengan link asli kelompokmu)*
