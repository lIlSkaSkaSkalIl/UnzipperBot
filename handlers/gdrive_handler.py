from pyrogram import Client, filters
from pyrogram.types import Message
import logging
import os

from download.gdrive import download_from_gdrive
from handlers.extract_handler import extract_archive
from handlers.upload_handler import upload_files

logger = logging.getLogger(__name__)

# Status user yang sedang menunggu link setelah /gdrive
user_gdrive_state = set()

# Handler command /gdrive
gdrive_command_handler = filters.command("gdrive") & filters.private

@Client.on_message(gdrive_command_handler)
async def gdrive_command(client: Client, message: Message):
    user_id = message.from_user.id
    user_gdrive_state.add(user_id)
    await message.reply_text("🔗 Silakan kirimkan link Google Drive yang ingin Anda unduh.")

# Handler saat user mengirimkan link Google Drive
@Client.on_message(filters.private & filters.text)
async def handle_gdrive_link(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_gdrive_state:
        return  # abaikan jika user belum memanggil /gdrive

    gdrive_url = message.text.strip()
    try:
        await message.reply_text("⏳ Sedang mengunduh dari Google Drive...")
        downloaded_path = await download_from_gdrive(gdrive_url)

        if not downloaded_path or not os.path.exists(downloaded_path):
            raise Exception("File gagal diunduh atau tidak ditemukan.")

        await message.reply_text("📦 Berhasil mengunduh. Mengekstrak file...")
        extracted_files = extract_archive(downloaded_path)

        if not extracted_files:
            await message.reply_text("❌ Tidak ada file yang berhasil diekstrak.")
            return

        await message.reply_text(f"📤 Mengupload {len(extracted_files)} file ke Telegram...")
        await upload_files(client, message, extracted_files)

    except Exception as e:
        logger.exception("❌ Terjadi kesalahan saat proses GDrive")
        await message.reply_text(f"❌ Terjadi kesalahan: {e}")

    finally:
        user_gdrive_state.discard(user_id)
