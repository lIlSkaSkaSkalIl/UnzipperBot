import asyncio

# Global lock untuk membatasi hanya 1 download aktif dalam satu waktu
download_lock = asyncio.Lock()
