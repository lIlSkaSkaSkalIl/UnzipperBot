from pyrogram import Client, filters
from pyrogram.types import Message
import logging

logger = logging.getLogger(__name__)

# Impor handler khusus
from handlers.start_handler import start_handler
from handlers import gdrive_handler  # Handler yang sudah tersedia

# Jika nanti ada handler tambahan, tinggal import di sini
# from handlers import mega_handler, terra_handler

def add_command_handlers(app: Client):
    # Tambahkan /start handler
    app.add_handler(start_handler)

    # Dictionary layanan yang ingin didukung
    source_handlers = {
        "gdrive": gdrive_handler,
        # "mega": mega_handler,
        # "terra": terra_handler,
    }

    # Daftarkan semua handler dari masing-masing layanan
    for name, module in source_handlers.items():
        if hasattr(module, "command_handler"):
            app.add_handler(module.command_handler)
            logger.info(f"📌 Handler /{name} ditambahkan.")
        if hasattr(module, "link_handler"):
            app.add_handler(module.link_handler)
            logger.info(f"📌 Handler link untuk {name} ditambahkan.")

    logger.info("✅ Semua command handler berhasil didaftarkan.")
