import gdown
import os
import logging
from utils.lock import download_lock  # Gunakan global lock berbasis asyncio

logger = logging.getLogger(__name__)

async def download_from_gdrive(gdrive_url: str, output_dir: str = "downloads") -> str:
    """
    Mengunduh file dari Google Drive menggunakan gdown (asynchronous dengan global lock).

    Args:
        gdrive_url (str): URL Google Drive
        output_dir (str): Folder tempat file akan disimpan

    Returns:
        str: Path ke file hasil unduhan
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    async with download_lock:  # Gunakan global lock agar hanya satu unduhan aktif
        try:
            logger.info(f"⬇️ Memulai unduhan GDrive: {gdrive_url}")
            # Biarkan gdown menentukan nama file
            result = gdown.download(url=gdrive_url, output=None, quiet=False)

            if result is None:
                raise Exception("❌ Unduhan GDrive gagal. Periksa URL atau izin file.")

            logger.info(f"✅ Selesai download: {result}")
            return result

        except Exception as e:
            logger.exception("❌ Terjadi kesalahan saat unduh GDrive:")
            raise e
