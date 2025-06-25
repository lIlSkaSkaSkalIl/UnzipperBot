from pyrogram import Client, filters
from pyrogram.types import Message
import logging

logger = logging.getLogger(__name__)

start_handler = filters.command("start") & filters.private

@Client.on_message(start_handler)
async def start(client: Client, message: Message):
    user = message.from_user
    logger.info(f"👤 /start dipanggil oleh {user.first_name} (id={user.id}, username=@{user.username})")

    await message.reply_text(
        "👋 Halo! Saya adalah Unzipper Bot.\n\n"
        "📁 Kirimkan link file (zip, tar, rar, dll)\n"
        "🔓 Bot akan mengekstraknya dan mengirim semua file ke Telegram.\n\n"
        "🎥 Video akan dikirim sebagai *streamable video*\n"
        "📄 File lain dikirim sebagai *dokumen*\n\n"
        "📌 Saat ini hanya mendukung:\n"
        " - /gdrive → Google Drive\n"
        " - /mega   → (segera)\n"
        " - /terra  → (segera)"
    )
