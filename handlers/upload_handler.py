import os
import logging
from pyrogram import Client
from pyrogram.types import Message

logger = logging.getLogger(__name__)

MAX_UPLOAD_SIZE = 2 * 1024 * 1024 * 1024  # 2 GB
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".webm", ".mov", ".avi", ".flv"]

async def upload_files(client: Client, message: Message, file_paths: list[str]):
    """
    Mengunggah file ke Telegram satu per satu, validasi ukuran & jenis.

    Args:
        client (Client): Pyrogram client
        message (Message): Message untuk membalas
        file_paths (list[str]): Daftar file hasil ekstrak
    """
    logger.info(f"📤 Upload dimulai untuk {len(file_paths)} file.")
    uploaded_count = 0
    skipped_count = 0

    for path in file_paths:
        if not os.path.exists(path):
            logger.warning(f"⚠️ File tidak ditemukan: {path}")
            skipped_count += 1
            continue

        file_size = os.path.getsize(path)
        file_name = os.path.basename(path)

        if file_size == 0:
            logger.warning(f"⚠️ Melewati file kosong: {file_name}")
            skipped_count += 1
            continue

        if file_size > MAX_UPLOAD_SIZE:
            logger.warning(f"⏩ Lewati file >2GB: {file_name}")
            await message.reply_text(f"⚠️ *{file_name}* lebih dari 2GB, dilewati.")
            skipped_count += 1
            continue

        ext = os.path.splitext(file_name)[1].lower()
        caption = f"📄 {file_name} ({round(file_size / 1024**2, 2)} MB)"

        try:
            if ext in VIDEO_EXTENSIONS:
                logger.info(f"🎞️ Upload video: {file_name}")
                await message.reply_video(path, caption=caption)
            else:
                logger.info(f"📄 Upload dokumen: {file_name}")
                await message.reply_document(path, caption=caption)

            logger.info(f"✅ Berhasil upload: {file_name}")
            uploaded_count += 1

        except Exception as e:
            logger.exception(f"❌ Upload gagal: {file_name}")
            await message.reply_text(f"❌ Gagal upload *{file_name}*: {e}")
            skipped_count += 1

    logger.info(f"📊 Upload selesai. Berhasil: {uploaded_count}, Dilewati: {skipped_count}")
    await message.reply_text(f"✅ Selesai upload.\n📥 Total: {len(file_paths)}\n📤 Berhasil: {uploaded_count}\n⏩ Dilewati: {skipped_count}")

    _cleanup_all_files()

def _cleanup_all_files():
    """
    Menghapus semua isi dari folder downloads/
    """
    downloads_dir = "downloads"
    if not os.path.isdir(downloads_dir):
        return

    for entry in os.scandir(downloads_dir):
        try:
            if entry.is_file():
                os.remove(entry.path)
            elif entry.is_dir():
                _remove_dir_recursive(entry.path)
        except Exception as e:
            logger.warning(f"⚠️ Gagal menghapus {entry.path}: {e}")

    logger.info("🗑️ Semua file di 'downloads/' dihapus.")

def _remove_dir_recursive(path):
    for entry in os.scandir(path):
        if entry.is_file():
            os.remove(entry.path)
        elif entry.is_dir():
            _remove_dir_recursive(entry.path)
    os.rmdir(path)
