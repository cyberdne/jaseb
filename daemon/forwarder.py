import os
import asyncio
import datetime
import requests
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# Konfigurasi
api_id = int(os.getenv('TG_API_ID', 'YOUR_API_ID'))
api_hash = os.getenv('TG_API_HASH', 'YOUR_API_HASH')
session_name = os.getenv('TG_SESSION', 'user')
backend_url = os.getenv('JASEB_BACKEND', 'http://127.0.0.1:8000')
source_chat = os.getenv('JASEB_SOURCE', 'source_channel_username')  # bisa username/channel id

# Delay antar forward (detik) untuk keamanan
FORWARD_DELAY = 10

client = TelegramClient(session_name, api_id, api_hash)

async def get_all_groups():
    result = []
    async for dialog in client.iter_dialogs():
        if (dialog.is_group or dialog.is_channel) and not dialog.entity.broadcast:
            result.append((dialog.id, dialog.name))
    return result

@client.on(events.NewMessage(chats=source_chat))
async def handler(event):
    groups = await get_all_groups()
    for group_id, group_name in groups:
        try:
            await client.send_message(group_id, event.message)
            status = "Success"
        except FloodWaitError as e:
            status = f"FloodWait: {e.seconds}s"
            await asyncio.sleep(e.seconds)
        except Exception as e:
            status = f"Failed: {e}"
        # Log ke backend
        try:
            requests.post(f"{backend_url}/log", json={
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "group_name": group_name,
                "status": status
            }, timeout=5)
        except Exception:
            pass
        await asyncio.sleep(FORWARD_DELAY)

async def main():
    print("JASEB Forwarder running...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main()) 