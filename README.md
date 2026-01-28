# Space Invaders (Python Edition)

![Space Invaders Python](Graphics/screenshot.png)
> *Catatan: Ganti `Graphics/screenshot.png` dengan lokasi gambar screenshot permainan Anda.*

## 📝 Deskripsi

Proyek ini adalah rekreasi dari permainan video arcade klasik **"Space Invaders"** yang dibangun menggunakan bahasa pemrograman **Python**. Permainan ini menghadirkan pengalaman retro dengan grafis piksel, menampilkan pertempuran antara pesawat ruang angkasa pemain melawan formasi alien yang menyerang.

Tujuan utama permainan adalah menembak jatuh semua alien sebelum mereka mencapai bagian bawah layar, sambil menghindari tembakan musuh dan menjaga nyawa yang tersisa.

## ✨ Fitur Permainan

Berdasarkan versi saat ini, permainan mencakup elemen-elemen visual dan mekanik berikut:

*   **Formasi Musuh (Alien):** Musuh ditampilkan dalam bentuk piksel dengan kombinasi warna **kuning dan ungu** yang tersusun rapi di bagian atas layar.
*   **Pesawat Pemain:** Karakter pemain berupa pesawat berbentuk segitiga berwarna **biru** dengan dasar **kuning**, terletak di bagian bawah tengah layar.
*   **Sistem Pertahanan (Obstacle):** Terdapat **tiga (3) penghalang berwarna biru** yang berfungsi sebagai pelindung (bunker) di antara pemain dan musuh.
*   **Sistem Skor & Level:**
    *   **Score:** Menampilkan skor saat ini (contoh: `03400`).
    *   **High-Score:** Menampilkan skor tertinggi yang pernah dicapai (contoh: `21000`).
    *   **Level:** Indikator tingkat kesulitan permainan (contoh: `LEVEL 01`).
*   **Indikator Nyawa:** Status sisa nyawa pemain ditampilkan dengan **4 ikon spaceship** kecil di layar.
*   **Power-Up:** Terdapat item **Ikon Hati** yang akan muncul; jika pemain berhasil mengambil atau mengenainya, pemain akan mendapatkan tambahan nyawa (extra life).
*   **Efek Visual:** Tampilan laser tembakan pemain yang terlihat meluncur ke arah musuh.

## 🛠️ Prasyarat (Requirements)

Untuk menjalankan permainan ini, pastikan Anda telah menginstal:

*   **Python 3.1x**
*   **Pygame Library**

## 📦 Cara Instalasi dan Menjalankan

1.  **Clone atau Unduh Repository ini**
    ```bash
    git clone https://github.com/username/space-invaders-python.git
    cd space-invaders-python
    ```

2.  **Instal Library yang Dibutuhkan**
    Gunakan `pip` untuk menginstal modul pygame:
    ```bash
    pip install pygame
    ```

3.  **Jalankan Permainan**
    Buka terminal dan jalankan file utama (biasanya `main.py` atau `space_invaders.py`):
    ```bash
    python main.py
    ```

## 🎮 Kontrol (Controls)

*   **Tombol Panah Kiri (⬅️) / A:** Bergerak ke Kiri
*   **Tombol Panah Kanan (➡️) / D:** Bergerak ke Kanan
*   **Spasi (Spacebar):** Menembak Laser


## 🤝 Kontribusi

Kontribusi selalu diterima! Silakan lakukan *Fork* pada repository ini dan buat *Pull Request* jika Anda ingin menambahkan fitur baru atau memperbaiki bug.
