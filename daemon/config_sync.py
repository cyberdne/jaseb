import requests
import os
import json
import time

BACKEND_URL = os.getenv('JASEB_BACKEND', 'http://127.0.0.1:8000')
SYNC_INTERVAL = 60  # detik

while True:
    try:
        r = requests.get(f'{BACKEND_URL}/sync')
        data = r.json()
        with open('sync_data.json', 'w') as f:
            json.dump(data, f)
        print('Sync success:', len(data['accounts']), 'akun')
    except Exception as e:
        print('Sync error:', e)
    time.sleep(SYNC_INTERVAL) 