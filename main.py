import logging
import asyncio
from pyrogram import Client
from handlers.command_handler import add_command_handlers
from handlers.unzip_handler import add_unzip_handler
from config import API_ID, API_HASH, SESSION_STRING

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("UnzipperBot")

async def main():
    logger.info("🔧 Inisialisasi Unzipper Bot...")

    app = Client(
        name="UnzipperBot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING,
        workers=6,
        in_memory=True
    )

    # Tambahkan handler
    add_command_handlers(app)
    add_unzip_handler(app)

    await app.start()
    logger.info("✅ Pyrogram client berhasil dijalankan.")
    logger.info("🚀 Bot siap menerima perintah unzip!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    from pyrogram.idle import idle
    asyncio.run(main())
