import os
import logging
from pyrogram import Client
from pyrogram.types import Message

logger = logging.getLogger(__name__)

# Ukuran maksimum upload Telegram (2 GB)
MAX_UPLOAD_SIZE = 2 * 1024 * 1024 * 1024
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".webm", ".mov", ".avi", ".flv"]

async def upload_files(client: Client, message: Message, file_paths: list[str]):
    """
    Mengunggah file ke Telegram satu per satu, dengan validasi ukuran.
    Video dikirim sebagai streamable video, sisanya sebagai dokumen.

    Args:
        client (Client): Pyrogram client
        message (Message): Message asal untuk reply
        file_paths (list[str]): List path file yang akan diupload
    """
    logger.info(f"📤 Memulai upload {len(file_paths)} file...")

    for path in file_paths:
        if not os.path.exists(path):
            logger.warning(f"⚠️ File tidak ditemukan: {path}")
            continue

        file_size = os.path.getsize(path)
        file_name = os.path.basename(path)

        if file_size > MAX_UPLOAD_SIZE:
            logger.warning(f"⏩ Melewati file >2GB: {file_name}")
            await message.reply_text(f"⚠️ Melewati *{file_name}* karena ukurannya melebihi 2GB.")
            continue

        try:
            ext = os.path.splitext(file_name)[1].lower()
            caption = f"📄 {file_name} ({round(file_size / 1024**2, 2)} MB)"

            if ext in VIDEO_EXTENSIONS:
                logger.info(f"🎞️ Mengupload video: {file_name}")
                await message.reply_video(path, caption=caption)
            else:
                logger.info(f"📄 Mengupload dokumen: {file_name}")
                await message.reply_document(path, caption=caption)

            logger.info(f"✅ Sukses upload: {file_name}")

        except Exception as e:
            logger.exception(f"❌ Gagal upload {file_name}: {e}")
            await message.reply_text(f"❌ Gagal mengupload *{file_name}*: {e}")

    logger.info("🧹 Menghapus semua file setelah upload selesai.")
    _cleanup_all_files()

def _cleanup_all_files():
    """
    Menghapus semua isi folder downloads/ setelah semua proses selesai.
    """
    downloads_dir = "downloads"
    if not os.path.exists(downloads_dir):
        return

    for root, dirs, files in os.walk(downloads_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

    logger.info("🗑️ Folder downloads/ dibersihkan.")
