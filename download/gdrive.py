import gdown
import os
import logging
import asyncio
from threading import Lock

logger = logging.getLogger(__name__)
download_lock = Lock()

async def download_from_gdrive(gdrive_url: str, output_dir: str = "downloads") -> str:
    """
    Mengunduh file dari Google Drive menggunakan gdown.

    Args:
        gdrive_url (str): URL Google Drive
        output_dir (str): Folder tempat file akan disimpan

    Returns:
        str: Path ke file hasil unduhan
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Gunakan global lock agar hanya satu unduhan yang aktif
    if not download_lock.acquire(blocking=False):
        raise Exception("🔒 Sedang ada proses download lain yang berjalan.")

    try:
        logger.info(f"⬇️ Memulai unduhan GDrive: {gdrive_url}")
        file_path = os.path.join(output_dir, "gdrive_download")

        # gdown bisa return None jika gagal
        result = gdown.download(url=gdrive_url, output=file_path, quiet=False)
        if result is None:
            raise Exception("❌ Unduhan GDrive gagal. Periksa URL atau izin file.")

        logger.info(f"✅ Selesai download: {result}")
        return result

    except Exception as e:
        logger.exception("❌ Terjadi kesalahan saat unduh GDrive:")
        raise e

    finally:
        download_lock.release()
