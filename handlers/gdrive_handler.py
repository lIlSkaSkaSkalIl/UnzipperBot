import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message

from download.gdrive import download_from_gdrive
from handlers.extract_handler import extract_archive
from handlers.upload_handler import upload_files

logger = logging.getLogger(__name__)

# Set untuk melacak user yang sedang dalam mode gdrive
user_gdrive_state = set()

# Handler untuk /gdrive command
command_handler = filters.command("gdrive") & filters.private

@Client.on_message(command_handler)
async def handle_gdrive_command(client: Client, message: Message):
    user_id = message.from_user.id
    user_gdrive_state.add(user_id)
    await message.reply_text("🔗 Silakan kirimkan link Google Drive yang ingin Anda unduh.")

# Handler untuk teks yang dikirim setelah /gdrive
link_handler = filters.private & filters.text

@Client.on_message(link_handler)
async def handle_gdrive_link(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id not in user_gdrive_state:
        return  # Bukan bagian dari sesi gdrive

    gdrive_url = message.text.strip()
    try:
        await message.reply_text("⏳ Mengunduh dari Google Drive...")
        downloaded_path = await download_from_gdrive(gdrive_url)

        if not downloaded_path or not os.path.exists(downloaded_path):
            raise Exception("❌ File gagal diunduh atau tidak ditemukan.")

        await message.reply_text("📦 Berhasil diunduh. Mengekstrak file...")
        extracted_files = extract_archive(downloaded_path)

        if not extracted_files:
            await message.reply_text("⚠️ Tidak ada file yang berhasil diekstrak.")
            return

        await message.reply_text(f"📤 Mengunggah {len(extracted_files)} file ke Telegram...")
        await upload_files(client, message, extracted_files)

    except Exception as e:
        logger.exception("❌ Terjadi kesalahan saat proses Google Drive")
        await message.reply_text(f"❌ Kesalahan: {e}")

    finally:
        user_gdrive_state.discard(user_id)
