from pyrogram import Client, filters
from pyrogram.types import Message
import logging

# Import handler untuk masing-masing layanan
from handlers.gdrive_handler import gdrive_command_handler, handle_gdrive_link
# from handlers.mega_handler import mega_command_handler, handle_mega_link
# from handlers.terra_handler import terra_command_handler, handle_terra_link

logger = logging.getLogger(__name__)

def add_command_handlers(app: Client):
    # /start
    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client: Client, message: Message):
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
            " - /terra  → (segera)\n"
        )

    # /gdrive
    app.add_handler(gdrive_command_handler)
    app.add_handler(handle_gdrive_link)

    # Handler lain siap ditambahkan
    # app.add_handler(mega_command_handler)
    # app.add_handler(handle_mega_link)

    # app.add_handler(terra_command_handler)
    # app.add_handler(handle_terra_link)

    logger.info("📌 Handler /start, /gdrive, /mega, dan /terra ditambahkan.")
