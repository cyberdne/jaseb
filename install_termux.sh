#!/data/data/com.termux/files/usr/bin/bash
set -e

# Update & install dependencies
pkg update -y && pkg upgrade -y
pkg install python git -y

# Install pip dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Buat folder sessions jika belum ada
mkdir -p backend/sessions

# Info API_ID dan API_HASH
if [ ! -f .env ]; then
  echo "Silakan edit file .env untuk mengisi TG_API_ID dan TG_API_HASH!"
  echo "TG_API_ID=ISI_API_ID_ANDA" > .env
  echo "TG_API_HASH=ISI_API_HASH_ANDA" >> .env
fi

# Jalankan sinkronisasi config (background)
cd daemon
nohup python config_sync.py &

# Jalankan forwarder (manual)
echo "\nJalankan python forwarder.py di folder daemon untuk memulai auto-forward!" 