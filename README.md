# JASEB Telegram Auto Forwarder

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

## Fitur Utama
- Auto forward pesan ke semua grup/LPM yang tersedia pada akun Telegram (tanpa input manual target)
- Multi-login menggunakan akun manusia (userbot, bukan bot API)
- Log detail pengiriman (waktu, nama grup, status)
- Web konfigurasi & monitoring real-time
- Support Termux (daemon) & CPanel (web)

---

## Deploy Otomatis Backend di Railway
1. **Fork/clone repo ini ke GitHub Anda.**
2. **Klik badge "Deploy on Railway" di atas** atau buka [https://railway.app/new](https://railway.app/new).
3. **Pilih repo GitHub Anda, Railway akan otomatis build & deploy backend.**
4. **Ambil URL backend dari Railway (misal: https://jaseb-backend.up.railway.app).**
5. **Edit frontend (dashboard.html) dan Termux agar mengarah ke URL backend Railway.**

---

## Instalasi di Termux (Otomatis)
1. **Install Termux** dari Play Store/F-Droid.
2. **Jalankan perintah berikut di Termux:**
   ```bash
   pkg update && pkg install git python -y
   git clone https://github.com/username/jaseb.git
   cd jaseb
   chmod +x install_termux.sh
   ./install_termux.sh
   ```
   > Script ini akan otomatis menginstall dependensi, mengatur environment, dan menjalankan daemon.

3. **Edit file `.env` jika perlu (API_ID, API_HASH, dsb).**
4. **Jalankan sinkronisasi config:**
   ```bash
   cd daemon
   python config_sync.py &
   ```
5. **Jalankan forwarder:**
   ```bash
   python forwarder.py
   ```

---

## Instalasi di Web/CPanel
1. **Upload folder `frontend` ke hosting/public_html.**
2. **Edit file JS di frontend (dashboard.html) agar API_BASE mengarah ke URL backend Railway.**
3. **Akses dashboard di browser untuk kelola akun, konfigurasi, dan monitoring.**

---

## Catatan Keamanan
- Jangan gunakan untuk spam! Gunakan delay dan filter agar tidak terdeteksi sebagai spam oleh Telegram.
- Gunakan autentikasi pada web/API.
- Simpan session file dengan aman.

---

## Konfigurasi Lanjutan
- Untuk multi-login, simpan session file per user.
- Untuk real-time log, gunakan Socket.IO/WebSocket.

---

## Pengembangan Selanjutnya
- Penambahan fitur sesuai kebutuhan.
- Optimasi keamanan dan performa. 